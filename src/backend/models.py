"""
PaperSubmit AI - 数据库模型定义
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Paper(Base):
    """论文表"""
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    authors = Column(Text)  # JSON格式存储作者列表
    abstract = Column(Text)
    keywords = Column(Text)  # JSON格式存储关键词
    file_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Paper(id={self.id}, title='{self.title}')>"


class Submission(Base):
    """投稿记录表"""
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_id = Column(Integer, nullable=False)
    journal_name = Column(String(200), nullable=False)
    status = Column(String(50), default="pending")  # pending, submitting, submitted, under_review, accepted, rejected
    submission_id = Column(String(100))  # 期刊系统返回的稿件编号
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Submission(id={self.id}, journal='{self.journal_name}', status='{self.status}')>"


class Credential(Base):
    """凭证表（加密存储）"""
    __tablename__ = "credentials"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    journal_name = Column(String(200), nullable=False, unique=True)
    username = Column(String(100), nullable=False)
    encrypted_password = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Credential(journal='{self.journal_name}', username='{self.username}')>"


# 数据库初始化
def init_db():
    """初始化数据库"""
    db_path = os.path.join(os.path.dirname(__file__), "../../data/papersubmit.db")
    db_dir = os.path.dirname(db_path)
    
    # 确保data目录存在
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_session():
    """获取数据库会话"""
    engine = init_db()
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


if __name__ == "__main__":
    # 测试数据库创建
    engine = init_db()
    print("✅ 数据库初始化成功！")
    print(f"📁 数据库位置: {os.path.abspath('../../data/papersubmit.db')}")
