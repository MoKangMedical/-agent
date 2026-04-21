"""
PaperSubmit AI - 数据导出模块
"""
import csv
import json
from datetime import datetime
import os
from models import Paper, Submission, get_session


class DataExporter:
    """数据导出器"""
    
    def __init__(self, export_dir='../../data/exports'):
        """
        初始化导出器
        
        Args:
            export_dir: 导出文件保存目录
        """
        self.export_dir = os.path.join(os.path.dirname(__file__), export_dir)
        os.makedirs(self.export_dir, exist_ok=True)
        print(f"📁 导出目录: {self.export_dir}")
    
    def export_papers_to_csv(self, filename=None):
        """
        导出论文数据到CSV
        
        Args:
            filename: 文件名（可选）
        
        Returns:
            导出的文件路径
        """
        if filename is None:
            filename = f"papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        db = get_session()
        papers = db.query(Paper).all()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 写入表头
            writer.writerow(['ID', '标题', '作者', '摘要', '关键词', '文件路径', '创建时间'])
            
            # 写入数据
            for paper in papers:
                writer.writerow([
                    paper.id,
                    paper.title,
                    paper.authors,
                    paper.abstract,
                    paper.keywords or '',
                    paper.file_path,
                    paper.created_at.strftime('%Y-%m-%d %H:%M:%S')
                ])
        
        db.close()
        
        print(f"✅ 论文数据已导出: {filepath}")
        print(f"   共 {len(papers)} 条记录")
        
        return filepath
    
    def export_submissions_to_csv(self, filename=None):
        """
        导出投稿数据到CSV
        
        Args:
            filename: 文件名（可选）
        
        Returns:
            导出的文件路径
        """
        if filename is None:
            filename = f"submissions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        db = get_session()
        submissions = db.query(Submission).all()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 写入表头
            writer.writerow([
                'ID', '论文ID', '期刊名称', '状态', '稿件编号', 
                '创建时间', '更新时间'
            ])
            
            # 写入数据
            for sub in submissions:
                writer.writerow([
                    sub.id,
                    sub.paper_id,
                    sub.journal_name,
                    sub.status,
                    sub.submission_id or '',
                    sub.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    sub.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                ])
        
        db.close()
        
        print(f"✅ 投稿数据已导出: {filepath}")
        print(f"   共 {len(submissions)} 条记录")
        
        return filepath
    
    def export_all_to_json(self, filename=None):
        """
        导出所有数据到JSON
        
        Args:
            filename: 文件名（可选）
        
        Returns:
            导出的文件路径
        """
        if filename is None:
            filename = f"all_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.export_dir, filename)
        
        db = get_session()
        
        # 获取所有数据
        papers = db.query(Paper).all()
        submissions = db.query(Submission).all()
        
        # 构建数据结构
        data = {
            'export_time': datetime.now().isoformat(),
            'statistics': {
                'total_papers': len(papers),
                'total_submissions': len(submissions)
            },
            'papers': [
                {
                    'id': p.id,
                    'title': p.title,
                    'authors': json.loads(p.authors) if p.authors else [],
                    'abstract': p.abstract,
                    'keywords': json.loads(p.keywords) if p.keywords else [],
                    'file_path': p.file_path,
                    'created_at': p.created_at.isoformat()
                }
                for p in papers
            ],
            'submissions': [
                {
                    'id': s.id,
                    'paper_id': s.paper_id,
                    'journal_name': s.journal_name,
                    'status': s.status,
                    'submission_id': s.submission_id,
                    'created_at': s.created_at.isoformat(),
                    'updated_at': s.updated_at.isoformat()
                }
                for s in submissions
            ]
        }
        
        # 写入JSON文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        db.close()
        
        print(f"✅ 所有数据已导出: {filepath}")
        print(f"   论文: {len(papers)} 条")
        print(f"   投稿: {len(submissions)} 条")
        
        return filepath
    
    def export_statistics_report(self, filename=None):
        """
        导出统计报告
        
        Args:
            filename: 文件名（可选）
        
        Returns:
            导出的文件路径
        """
        if filename is None:
            filename = f"statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = os.path.join(self.export_dir, filename)
        
        db = get_session()
        
        # 统计数据
        total_papers = db.query(Paper).count()
        total_submissions = db.query(Submission).count()
        
        status_counts = {}
        for status in ['pending', 'submitted', 'under_review', 'accepted', 'rejected']:
            count = db.query(Submission).filter(Submission.status == status).count()
            status_counts[status] = count
        
        # 按期刊统计
        journal_counts = {}
        submissions = db.query(Submission).all()
        for sub in submissions:
            journal_counts[sub.journal_name] = journal_counts.get(sub.journal_name, 0) + 1
        
        db.close()
        
        # 生成报告
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          PaperSubmit AI - 统计报告                          ║
╚══════════════════════════════════════════════════════════════╝

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

【总体统计】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  论文总数:     {total_papers:>6} 篇
  投稿总数:     {total_submissions:>6} 次
  平均投稿次数: {total_submissions/max(total_papers, 1):>6.2f} 次/篇

【投稿状态分布】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  待处理:       {status_counts.get('pending', 0):>6} 次  ({status_counts.get('pending', 0)/max(total_submissions, 1)*100:>5.1f}%)
  已提交:       {status_counts.get('submitted', 0):>6} 次  ({status_counts.get('submitted', 0)/max(total_submissions, 1)*100:>5.1f}%)
  审稿中:       {status_counts.get('under_review', 0):>6} 次  ({status_counts.get('under_review', 0)/max(total_submissions, 1)*100:>5.1f}%)
  已接收:       {status_counts.get('accepted', 0):>6} 次  ({status_counts.get('accepted', 0)/max(total_submissions, 1)*100:>5.1f}%)
  已拒稿:       {status_counts.get('rejected', 0):>6} 次  ({status_counts.get('rejected', 0)/max(total_submissions, 1)*100:>5.1f}%)

【期刊投稿分布】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # 按投稿次数排序
        sorted_journals = sorted(journal_counts.items(), key=lambda x: x[1], reverse=True)
        for journal, count in sorted_journals:
            report += f"  {journal:<40} {count:>4} 次\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【系统信息】
  数据库: SQLite
  导出目录: {self.export_dir}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
报告结束
"""
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 统计报告已生成: {filepath}")
        
        # 同时打印到控制台
        print(report)
        
        return filepath
    
    def export_all(self):
        """
        导出所有数据（CSV + JSON + 统计报告）
        
        Returns:
            导出的文件路径列表
        """
        print("📊 开始导出所有数据...\n")
        
        files = []
        
        # 导出论文CSV
        files.append(self.export_papers_to_csv())
        print()
        
        # 导出投稿CSV
        files.append(self.export_submissions_to_csv())
        print()
        
        # 导出JSON
        files.append(self.export_all_to_json())
        print()
        
        # 导出统计报告
        files.append(self.export_statistics_report())
        
        print(f"\n✅ 所有数据导出完成！共 {len(files)} 个文件")
        print(f"📁 导出目录: {self.export_dir}")
        
        return files


# 测试代码
if __name__ == "__main__":
    print("🧪 测试数据导出模块\n")
    
    exporter = DataExporter()
    
    # 导出所有数据
    exporter.export_all()
    
    print("\n✅ 数据导出测试完成！")
