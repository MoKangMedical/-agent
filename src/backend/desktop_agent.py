"""
PaperSubmit AI - 桌面Agent主程序
本地运行，直接访问文件系统，自动管理论文投稿
"""
import os
import json
import time
from datetime import datetime
from pathlib import Path
import sys

# 添加模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../ml_models'))
from keyword_extractor import KeywordExtractor
from journal_recommender import JournalRecommender


class PaperSubmitAgent:
    """论文投稿桌面Agent"""
    
    def __init__(self, watch_folder=None, config_file=None):
        """
        初始化Agent
        
        Args:
            watch_folder: 监控的论文文件夹路径
            config_file: 配置文件路径
        """
        # 默认监控文件夹
        if watch_folder is None:
            watch_folder = os.path.expanduser("~/Documents/Papers")
        
        self.watch_folder = Path(watch_folder)
        self.watch_folder.mkdir(parents=True, exist_ok=True)
        
        # 配置文件
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), "agent_config.json")
        self.config_file = config_file
        
        # 数据文件
        self.data_dir = self.watch_folder / ".papersubmit"
        self.data_dir.mkdir(exist_ok=True)
        
        self.papers_db = self.data_dir / "papers.json"
        self.submissions_db = self.data_dir / "submissions.json"
        self.log_file = self.data_dir / "agent.log"
        
        # 初始化ML模块
        self.keyword_extractor = KeywordExtractor(max_keywords=15)
        self.journal_recommender = JournalRecommender()
        
        # 加载配置
        self.config = self.load_config()
        
        # 加载数据
        self.papers = self.load_papers()
        self.submissions = self.load_submissions()
        
        self.log("✅ Agent初始化完成")
        self.log(f"📁 监控文件夹: {self.watch_folder}")
    
    def load_config(self):
        """加载配置"""
        default_config = {
            "auto_recommend": True,
            "auto_backup": True,
            "check_interval": 300,  # 5分钟
            "file_extensions": [".pdf"],
            "user_email": "",
            "default_authors": []
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                default_config.update(config)
        else:
            # 创建默认配置
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        return default_config
    
    def load_papers(self):
        """加载论文数据库"""
        if self.papers_db.exists():
            with open(self.papers_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_papers(self):
        """保存论文数据库"""
        with open(self.papers_db, 'w', encoding='utf-8') as f:
            json.dump(self.papers, f, indent=2, ensure_ascii=False)
    
    def load_submissions(self):
        """加载投稿数据库"""
        if self.submissions_db.exists():
            with open(self.submissions_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_submissions(self):
        """保存投稿数据库"""
        with open(self.submissions_db, 'w', encoding='utf-8') as f:
            json.dump(self.submissions, f, indent=2, ensure_ascii=False)
    
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def scan_folder(self):
        """扫描文件夹，发现新论文"""
        self.log("🔍 扫描文件夹...")
        
        new_papers = []
        
        for ext in self.config['file_extensions']:
            for pdf_file in self.watch_folder.glob(f"*{ext}"):
                # 跳过隐藏文件和已处理的文件
                if pdf_file.name.startswith('.'):
                    continue
                
                file_path = str(pdf_file.absolute())
                
                # 检查是否已经处理过
                if file_path not in self.papers:
                    self.log(f"📄 发现新论文: {pdf_file.name}")
                    new_papers.append(pdf_file)
        
        return new_papers
    
    def process_paper(self, pdf_file):
        """
        处理新论文
        
        Args:
            pdf_file: PDF文件路径
        """
        self.log(f"📝 处理论文: {pdf_file.name}")
        
        file_path = str(pdf_file.absolute())
        
        try:
            # 提取关键词
            self.log("   提取关键词...")
            keywords = self.keyword_extractor.extract_from_pdf(file_path)
            
            # 推荐期刊
            self.log("   推荐期刊...")
            recommendations = self.journal_recommender.recommend(keywords, top_k=5)
            
            # 保存论文信息
            paper_info = {
                "file_path": file_path,
                "file_name": pdf_file.name,
                "keywords": keywords,
                "recommendations": recommendations,
                "discovered_at": datetime.now().isoformat(),
                "status": "discovered"
            }
            
            self.papers[file_path] = paper_info
            self.save_papers()
            
            # 生成推荐报告
            self.generate_recommendation_report(pdf_file, paper_info)
            
            self.log(f"✅ 论文处理完成: {pdf_file.name}")
            
        except Exception as e:
            self.log(f"❌ 处理失败: {e}")
    
    def generate_recommendation_report(self, pdf_file, paper_info):
        """
        生成期刊推荐报告
        
        Args:
            pdf_file: PDF文件路径
            paper_info: 论文信息
        """
        report_file = pdf_file.parent / f"{pdf_file.stem}_推荐报告.txt"
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          PaperSubmit AI - 期刊推荐报告                      ║
╚══════════════════════════════════════════════════════════════╝

论文文件: {pdf_file.name}
分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

【提取的关键词】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{', '.join(paper_info['keywords'][:15])}

【推荐期刊 Top 5】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for i, rec in enumerate(paper_info['recommendations'], 1):
            report += f"""
{i}. {rec['journal']}
   综合评分: {rec['score']:.3f}
   匹配度:   {rec['match_score']:.3f}
   影响因子: {rec['impact_factor']}
   审稿时间: {rec['review_time_days']} 天
   接收率:   {rec['acceptance_rate']*100:.1f}%
   投稿系统: {rec['submission_system']}
   网址:     {rec.get('url', 'N/A')}
"""
        
        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【下一步操作】
1. 查看推荐期刊，选择合适的目标期刊
2. 在同目录下创建 {论文名}_投稿信息.json 文件
3. Agent会自动读取并创建投稿记录

【投稿信息文件格式】
{
  "journal_name": "期刊名称",
  "username": "投稿系统账号",
  "password": "投稿系统密码",
  "notes": "备注信息"
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.log(f"📊 推荐报告已生成: {report_file.name}")
    
    def check_submission_requests(self):
        """检查是否有新的投稿请求"""
        for pdf_file in self.watch_folder.glob("*.pdf"):
            submission_file = pdf_file.parent / f"{pdf_file.stem}_投稿信息.json"
            
            if submission_file.exists():
                file_path = str(pdf_file.absolute())
                
                # 检查是否已经处理过
                if file_path not in self.submissions:
                    self.log(f"📤 发现投稿请求: {pdf_file.name}")
                    self.process_submission_request(pdf_file, submission_file)
    
    def process_submission_request(self, pdf_file, submission_file):
        """
        处理投稿请求
        
        Args:
            pdf_file: PDF文件
            submission_file: 投稿信息文件
        """
        try:
            # 读取投稿信息
            with open(submission_file, 'r', encoding='utf-8') as f:
                submission_info = json.load(f)
            
            file_path = str(pdf_file.absolute())
            
            # 创建投稿记录
            submission_record = {
                "paper_file": file_path,
                "journal_name": submission_info['journal_name'],
                "username": submission_info['username'],
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "notes": submission_info.get('notes', '')
            }
            
            # 保存投稿记录
            submission_id = f"{pdf_file.stem}_{int(time.time())}"
            self.submissions[submission_id] = submission_record
            self.save_submissions()
            
            # 更新论文状态
            if file_path in self.papers:
                self.papers[file_path]['status'] = 'submitted'
                self.papers[file_path]['submission_id'] = submission_id
                self.save_papers()
            
            self.log(f"✅ 投稿记录已创建: {submission_id}")
            
            # 生成投稿确认报告
            self.generate_submission_report(pdf_file, submission_record, submission_id)
            
            # 重命名投稿信息文件（标记为已处理）
            processed_file = submission_file.parent / f"{submission_file.stem}_已处理.json"
            submission_file.rename(processed_file)
            
        except Exception as e:
            self.log(f"❌ 处理投稿请求失败: {e}")
    
    def generate_submission_report(self, pdf_file, submission_record, submission_id):
        """生成投稿确认报告"""
        report_file = pdf_file.parent / f"{pdf_file.stem}_投稿确认.txt"
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          PaperSubmit AI - 投稿确认报告                      ║
╚══════════════════════════════════════════════════════════════╝

投稿ID: {submission_id}
论文文件: {pdf_file.name}
投稿期刊: {submission_record['journal_name']}
投稿账号: {submission_record['username']}
创建时间: {submission_record['created_at']}
当前状态: {submission_record['status']}

备注: {submission_record['notes']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【下一步】
Agent将自动跟踪投稿状态，有更新会生成新的报告。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.log(f"📋 投稿确认报告已生成: {report_file.name}")
    
    def generate_status_report(self):
        """生成状态总览报告"""
        report_file = self.watch_folder / "投稿状态总览.txt"
        
        total_papers = len(self.papers)
        total_submissions = len(self.submissions)
        
        # 统计状态
        status_counts = {}
        for sub in self.submissions.values():
            status = sub['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          PaperSubmit AI - 投稿状态总览                      ║
╚══════════════════════════════════════════════════════════════╝

更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

【总体统计】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  论文总数:     {total_papers:>6} 篇
  投稿总数:     {total_submissions:>6} 次

【投稿状态】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for status, count in status_counts.items():
            report += f"  {status:<15} {count:>6} 次\n"
        
        report += "\n【论文列表】\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        for file_path, paper in self.papers.items():
            report += f"\n📄 {paper['file_name']}\n"
            report += f"   状态: {paper['status']}\n"
            report += f"   发现时间: {paper['discovered_at']}\n"
            if 'submission_id' in paper:
                report += f"   投稿ID: {paper['submission_id']}\n"
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.log(f"📊 状态总览已更新: {report_file.name}")
    
    def run_once(self):
        """运行一次扫描"""
        self.log("\n" + "="*60)
        self.log("🚀 开始新一轮扫描")
        
        # 扫描新论文
        new_papers = self.scan_folder()
        for pdf_file in new_papers:
            self.process_paper(pdf_file)
        
        # 检查投稿请求
        self.check_submission_requests()
        
        # 生成状态报告
        self.generate_status_report()
        
        self.log("✅ 扫描完成")
        self.log("="*60 + "\n")
    
    def run(self):
        """持续运行Agent"""
        self.log("🤖 Agent开始运行...")
        self.log(f"⏰ 扫描间隔: {self.config['check_interval']} 秒")
        
        try:
            while True:
                self.run_once()
                time.sleep(self.config['check_interval'])
        
        except KeyboardInterrupt:
            self.log("\n🛑 Agent停止运行")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PaperSubmit AI - 桌面Agent')
    parser.add_argument('--folder', type=str, help='监控的文件夹路径')
    parser.add_argument('--once', action='store_true', help='只运行一次')
    parser.add_argument('--config', type=str, help='配置文件路径')
    
    args = parser.parse_args()
    
    # 创建Agent
    agent = PaperSubmitAgent(
        watch_folder=args.folder,
        config_file=args.config
    )
    
    if args.once:
        # 只运行一次
        agent.run_once()
    else:
        # 持续运行
        agent.run()


if __name__ == "__main__":
    main()
