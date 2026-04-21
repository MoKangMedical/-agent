"""
PaperSubmit AI - FastAPI主应用
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import json
from datetime import datetime

from models import Paper, Submission, Credential, get_session
from security import CredentialManager
from scheduler import init_scheduler
from email_notifier import EmailNotifier
from data_exporter import DataExporter

# 导入ML模块
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../ml_models'))
from keyword_extractor import KeywordExtractor
from journal_recommender import JournalRecommender

# 创建FastAPI应用
app = FastAPI(
    title="PaperSubmit AI API",
    description="论文自动投稿系统API",
    version="1.0.0"
)

# CORS配置（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化凭证管理器
credential_manager = CredentialManager()

# 初始化ML模块
keyword_extractor = KeywordExtractor(max_keywords=15)
journal_recommender = JournalRecommender()

# 初始化调度器
task_scheduler = init_scheduler()

# 初始化邮件通知器
email_notifier = EmailNotifier()

# 初始化数据导出器
data_exporter = DataExporter()

# ==================== 数据模型 ====================

class PaperUploadResponse(BaseModel):
    paper_id: int
    filename: str
    message: str


class SubmissionCreate(BaseModel):
    paper_id: int
    journal_name: str
    username: str
    password: str


class SubmissionResponse(BaseModel):
    submission_id: int
    paper_id: int
    journal_name: str
    status: str
    created_at: datetime


class StatusResponse(BaseModel):
    submission_id: int
    journal_name: str
    status: str
    updated_at: datetime


# ==================== API端点 ====================

@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "欢迎使用 PaperSubmit AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/papers/upload", response_model=PaperUploadResponse)
async def upload_paper(
    file: UploadFile = File(...),
    title: str = Form(...),
    authors: str = Form(...),
    abstract: str = Form(...)
):
    """
    上传论文
    
    Args:
        file: PDF文件
        title: 论文标题
        authors: 作者列表（逗号分隔）
        abstract: 摘要
    
    Returns:
        上传结果
    """
    try:
        # 验证文件类型
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="仅支持PDF格式文件")
        
        # 保存文件
        papers_dir = os.path.join(os.path.dirname(__file__), "../../data/papers")
        os.makedirs(papers_dir, exist_ok=True)
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(papers_dir, safe_filename)
        
        # 写入文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 保存到数据库
        db = get_session()
        paper = Paper(
            title=title,
            authors=json.dumps(authors.split(',')),  # 转换为JSON
            abstract=abstract,
            file_path=file_path
        )
        db.add(paper)
        db.commit()
        db.refresh(paper)
        
        paper_id = paper.id
        db.close()
        
        return PaperUploadResponse(
            paper_id=paper_id,
            filename=safe_filename,
            message="论文上传成功"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


@app.get("/api/papers/{paper_id}")
async def get_paper(paper_id: int):
    """
    获取论文详情
    
    Args:
        paper_id: 论文ID
    
    Returns:
        论文信息
    """
    db = get_session()
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    db.close()
    
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    return {
        "id": paper.id,
        "title": paper.title,
        "authors": json.loads(paper.authors),
        "abstract": paper.abstract,
        "file_path": paper.file_path,
        "created_at": paper.created_at.isoformat()
    }


@app.get("/api/papers")
async def list_papers():
    """
    获取所有论文列表
    
    Returns:
        论文列表
    """
    db = get_session()
    papers = db.query(Paper).order_by(Paper.created_at.desc()).all()
    db.close()
    
    return {
        "total": len(papers),
        "papers": [
            {
                "id": p.id,
                "title": p.title,
                "authors": json.loads(p.authors),
                "created_at": p.created_at.isoformat()
            }
            for p in papers
        ]
    }


@app.post("/api/journals/recommend")
async def recommend_journals(paper_id: int, top_k: int = 5):
    """
    推荐期刊
    
    Args:
        paper_id: 论文ID
        top_k: 返回推荐数量
    
    Returns:
        推荐期刊列表
    """
    db = get_session()
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    db.close()
    
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    try:
        # 方法1: 从摘要提取关键词（快速）
        keywords = keyword_extractor.extract_from_abstract(paper.abstract)
        
        # 方法2: 如果文件存在，从PDF提取（更准确）
        if paper.file_path and os.path.exists(paper.file_path):
            try:
                pdf_keywords = keyword_extractor.extract_from_pdf(paper.file_path)
                if pdf_keywords:
                    keywords = pdf_keywords
            except Exception as e:
                print(f"⚠️ PDF关键词提取失败，使用摘要关键词: {e}")
        
        # 推荐期刊
        recommendations = journal_recommender.recommend(keywords, top_k=top_k)
        
        return {
            "paper_id": paper_id,
            "paper_title": paper.title,
            "keywords": keywords,
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐失败: {str(e)}")


@app.get("/api/journals/search")
async def search_journals(query: str, top_k: int = 10):
    """
    搜索期刊
    
    Args:
        query: 搜索关键词
        top_k: 返回数量
    
    Returns:
        匹配的期刊列表
    """
    try:
        results = journal_recommender.search_journals(query, top_k=top_k)
        return {
            "query": query,
            "total": len(results),
            "journals": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@app.get("/api/journals/{journal_name}")
async def get_journal_info(journal_name: str):
    """
    获取期刊详细信息
    
    Args:
        journal_name: 期刊名称
    
    Returns:
        期刊信息
    """
    try:
        journal = journal_recommender.get_journal_info(journal_name)
        if journal:
            return journal
        else:
            raise HTTPException(status_code=404, detail="期刊不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@app.post("/api/submissions/create", response_model=SubmissionResponse)
async def create_submission(submission: SubmissionCreate):
    """
    创建投稿任务
    
    Args:
        submission: 投稿信息
    
    Returns:
        投稿记录
    """
    db = get_session()
    
    # 验证论文是否存在
    paper = db.query(Paper).filter(Paper.id == submission.paper_id).first()
    if not paper:
        db.close()
        raise HTTPException(status_code=404, detail="论文不存在")
    
    # 加密并保存凭证
    encrypted_pwd = credential_manager.encrypt_password(submission.password)
    
    # 检查是否已存在该期刊的凭证
    existing_cred = db.query(Credential).filter(
        Credential.journal_name == submission.journal_name
    ).first()
    
    if existing_cred:
        # 更新现有凭证
        existing_cred.username = submission.username
        existing_cred.encrypted_password = encrypted_pwd
    else:
        # 创建新凭证
        credential = Credential(
            journal_name=submission.journal_name,
            username=submission.username,
            encrypted_password=encrypted_pwd
        )
        db.add(credential)
    
    # 创建投稿记录
    new_submission = Submission(
        paper_id=submission.paper_id,
        journal_name=submission.journal_name,
        status="pending"
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    
    result = SubmissionResponse(
        submission_id=new_submission.id,
        paper_id=new_submission.paper_id,
        journal_name=new_submission.journal_name,
        status=new_submission.status,
        created_at=new_submission.created_at
    )
    
    db.close()
    
    return result


@app.get("/api/submissions/{submission_id}/status", response_model=StatusResponse)
async def get_submission_status(submission_id: int):
    """
    查询投稿状态
    
    Args:
        submission_id: 投稿ID
    
    Returns:
        投稿状态
    """
    db = get_session()
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    db.close()
    
    if not submission:
        raise HTTPException(status_code=404, detail="投稿记录不存在")
    
    return StatusResponse(
        submission_id=submission.id,
        journal_name=submission.journal_name,
        status=submission.status,
        updated_at=submission.updated_at
    )


@app.get("/api/submissions")
async def list_submissions():
    """
    获取所有投稿列表
    
    Returns:
        投稿列表
    """
    db = get_session()
    submissions = db.query(Submission).order_by(Submission.created_at.desc()).all()
    
    result = []
    for s in submissions:
        paper = db.query(Paper).filter(Paper.id == s.paper_id).first()
        result.append({
            "id": s.id,
            "paper_id": s.paper_id,
            "paper_title": paper.title if paper else "未知",
            "journal_name": s.journal_name,
            "status": s.status,
            "submission_id": s.submission_id,
            "created_at": s.created_at.isoformat(),
            "updated_at": s.updated_at.isoformat()
        })
    
    db.close()
    
    return {
        "total": len(result),
        "submissions": result
    }


@app.get("/api/export/papers")
async def export_papers():
    """
    导出论文数据（CSV格式）
    
    Returns:
        文件路径
    """
    try:
        filepath = data_exporter.export_papers_to_csv()
        return {
            "success": True,
            "filepath": filepath,
            "message": "论文数据导出成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@app.get("/api/export/submissions")
async def export_submissions():
    """
    导出投稿数据（CSV格式）
    
    Returns:
        文件路径
    """
    try:
        filepath = data_exporter.export_submissions_to_csv()
        return {
            "success": True,
            "filepath": filepath,
            "message": "投稿数据导出成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@app.get("/api/export/all")
async def export_all_data():
    """
    导出所有数据（CSV + JSON + 统计报告）
    
    Returns:
        导出的文件列表
    """
    try:
        files = data_exporter.export_all()
        return {
            "success": True,
            "files": files,
            "message": f"成功导出 {len(files)} 个文件"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@app.get("/api/statistics")
async def get_statistics():
    """
    获取系统统计数据
    
    Returns:
        统计信息
    """
    db = get_session()
    
    try:
        # 基础统计
        total_papers = db.query(Paper).count()
        total_submissions = db.query(Submission).count()
        
        # 按状态统计
        status_counts = {}
        for status in ['pending', 'submitted', 'under_review', 'accepted', 'rejected']:
            count = db.query(Submission).filter(Submission.status == status).count()
            status_counts[status] = count
        
        # 按期刊统计
        journal_counts = {}
        submissions = db.query(Submission).all()
        for sub in submissions:
            journal_counts[sub.journal_name] = journal_counts.get(sub.journal_name, 0) + 1
        
        return {
            "total_papers": total_papers,
            "total_submissions": total_submissions,
            "status_distribution": status_counts,
            "journal_distribution": journal_counts,
            "average_submissions_per_paper": total_submissions / max(total_papers, 1)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计失败: {str(e)}")
    finally:
        db.close()


# ==================== 启动服务 ====================

if __name__ == "__main__":
    print("🚀 启动 PaperSubmit AI API 服务...")
    print("📖 API文档: http://localhost:8000/docs")
    print("🔍 健康检查: http://localhost:8000/health")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
