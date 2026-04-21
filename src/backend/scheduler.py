"""
PaperSubmit AI - 定时任务调度器
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
import sys
import os

# 添加路径以导入模块
sys.path.append(os.path.dirname(__file__))
from models import Submission, get_session

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SubmissionScheduler:
    """投稿状态检查调度器"""
    
    def __init__(self):
        """初始化调度器"""
        self.scheduler = BackgroundScheduler()
        logger.info("📅 调度器初始化完成")
    
    def check_all_submissions(self):
        """
        检查所有活跃投稿的状态
        
        这个函数会被定时调用，检查所有处于以下状态的投稿：
        - submitted: 已提交
        - under_review: 审稿中
        """
        logger.info("🔍 开始检查所有投稿状态...")
        
        db = get_session()
        
        try:
            # 查询所有活跃的投稿
            active_submissions = db.query(Submission).filter(
                Submission.status.in_(['submitted', 'under_review', 'pending'])
            ).all()
            
            logger.info(f"   找到 {len(active_submissions)} 个活跃投稿")
            
            for submission in active_submissions:
                try:
                    # 这里应该调用对应期刊的状态检查器
                    # 目前只是示例代码
                    logger.info(f"   检查投稿 #{submission.id} ({submission.journal_name})")
                    
                    # TODO: 根据期刊类型调用相应的检查器
                    # if submission.journal_name.lower() == 'arxiv':
                    #     new_status = check_arxiv_status(submission)
                    # elif submission.journal_name.lower() == 'nature':
                    #     new_status = check_nature_status(submission)
                    
                    # 示例：模拟状态变化
                    # if submission.status == 'pending':
                    #     submission.status = 'submitted'
                    #     logger.info(f"   ✅ 投稿 #{submission.id} 状态更新: pending -> submitted")
                    
                except Exception as e:
                    logger.error(f"   ❌ 检查投稿 #{submission.id} 失败: {e}")
            
            db.commit()
            logger.info("✅ 投稿状态检查完成")
            
        except Exception as e:
            logger.error(f"❌ 检查过程出错: {e}")
            db.rollback()
        finally:
            db.close()
    
    def send_notifications(self):
        """
        发送通知
        
        检查是否有状态变更需要通知用户
        """
        logger.info("📧 检查待发送通知...")
        
        # TODO: 实现通知逻辑
        # 1. 查询最近状态变更的投稿
        # 2. 发送邮件/微信通知
        # 3. 更新通知状态
        
        logger.info("✅ 通知检查完成")
    
    def cleanup_old_data(self):
        """
        清理旧数据
        
        定期清理过期的数据，如：
        - 已完成的投稿（超过6个月）
        - 临时文件
        """
        logger.info("🧹 开始清理旧数据...")
        
        # TODO: 实现清理逻辑
        
        logger.info("✅ 数据清理完成")
    
    def start(self):
        """启动调度器"""
        logger.info("🚀 启动定时任务调度器...")
        
        # 任务1: 每天早上9点检查投稿状态
        self.scheduler.add_job(
            self.check_all_submissions,
            CronTrigger(hour=9, minute=0),
            id='check_submissions',
            name='检查投稿状态',
            replace_existing=True
        )
        logger.info("   ✓ 任务已添加: 每天 09:00 检查投稿状态")
        
        # 任务2: 每天下午6点发送通知
        self.scheduler.add_job(
            self.send_notifications,
            CronTrigger(hour=18, minute=0),
            id='send_notifications',
            name='发送通知',
            replace_existing=True
        )
        logger.info("   ✓ 任务已添加: 每天 18:00 发送通知")
        
        # 任务3: 每周日凌晨2点清理旧数据
        self.scheduler.add_job(
            self.cleanup_old_data,
            CronTrigger(day_of_week='sun', hour=2, minute=0),
            id='cleanup_data',
            name='清理旧数据',
            replace_existing=True
        )
        logger.info("   ✓ 任务已添加: 每周日 02:00 清理旧数据")
        
        # 启动调度器
        self.scheduler.start()
        logger.info("✅ 调度器已启动")
        
        # 打印所有任务
        self.print_jobs()
    
    def stop(self):
        """停止调度器"""
        logger.info("🛑 停止调度器...")
        self.scheduler.shutdown()
        logger.info("✅ 调度器已停止")
    
    def print_jobs(self):
        """打印所有定时任务"""
        logger.info("\n📋 已配置的定时任务:")
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            logger.info(f"   • {job.name} (ID: {job.id})")
            logger.info(f"     下次运行: {job.next_run_time}")
    
    def run_now(self, job_id):
        """
        立即运行指定任务（用于测试）
        
        Args:
            job_id: 任务ID
        """
        logger.info(f"▶️ 手动触发任务: {job_id}")
        job = self.scheduler.get_job(job_id)
        if job:
            job.func()
        else:
            logger.error(f"❌ 任务不存在: {job_id}")


# 全局调度器实例
scheduler = None


def init_scheduler():
    """初始化全局调度器"""
    global scheduler
    if scheduler is None:
        scheduler = SubmissionScheduler()
        scheduler.start()
    return scheduler


def get_scheduler():
    """获取调度器实例"""
    global scheduler
    if scheduler is None:
        scheduler = init_scheduler()
    return scheduler


# 测试代码
if __name__ == "__main__":
    print("🧪 测试定时任务调度器\n")
    
    # 创建调度器
    test_scheduler = SubmissionScheduler()
    
    # 启动调度器
    test_scheduler.start()
    
    # 立即运行一次检查（测试）
    print("\n" + "="*60)
    print("立即运行一次投稿状态检查（测试）")
    print("="*60)
    test_scheduler.run_now('check_submissions')
    
    print("\n" + "="*60)
    print("调度器将在后台运行...")
    print("按 Ctrl+C 停止")
    print("="*60)
    
    try:
        # 保持运行
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n收到停止信号")
        test_scheduler.stop()
        print("✅ 测试完成")
