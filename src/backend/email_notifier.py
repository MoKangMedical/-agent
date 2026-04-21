"""
PaperSubmit AI - 邮件通知模块
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class EmailNotifier:
    """邮件通知器"""
    
    def __init__(self):
        """初始化邮件配置"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        
        if not self.sender_email or not self.sender_password:
            print("⚠️ 邮件配置未设置，请在.env文件中配置SENDER_EMAIL和SENDER_PASSWORD")
    
    def send_notification(self, to_email, subject, message, html_content=None):
        """
        发送邮件通知
        
        Args:
            to_email: 收件人邮箱
            subject: 邮件主题
            message: 邮件内容（纯文本）
            html_content: HTML格式内容（可选）
        
        Returns:
            是否发送成功
        """
        if not self.sender_email or not self.sender_password:
            print("❌ 邮件配置未设置，无法发送通知")
            return False
        
        try:
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # 添加纯文本内容
            text_part = MIMEText(message, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # 添加HTML内容
            if html_content:
                html_part = MIMEText(html_content, 'html', 'utf-8')
                msg.attach(html_part)
            
            # 连接SMTP服务器并发送
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ 邮件已发送到: {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
            return False
    
    def send_submission_created(self, to_email, paper_title, journal_name, submission_id):
        """
        发送投稿创建通知
        
        Args:
            to_email: 收件人邮箱
            paper_title: 论文标题
            journal_name: 期刊名称
            submission_id: 投稿ID
        """
        subject = f"📤 投稿已创建 - {paper_title}"
        
        message = f"""
您好！

您的论文投稿已成功创建：

论文标题：{paper_title}
投稿期刊：{journal_name}
投稿ID：{submission_id}
创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

系统将自动跟踪投稿状态，有任何更新会及时通知您。

祝投稿顺利！

---
PaperSubmit AI
让学术发表更简单
        """
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                <h2 style="color: #667eea;">📤 投稿已创建</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #667eea; margin-top: 0;">{paper_title}</h3>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>投稿期刊：</strong></td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">{journal_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>投稿ID：</strong></td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">{submission_id}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;"><strong>创建时间：</strong></td>
                            <td style="padding: 10px;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                        </tr>
                    </table>
                </div>
                
                <p style="color: #666;">系统将自动跟踪投稿状态，有任何更新会及时通知您。</p>
                
                <p style="color: #999; font-size: 0.9em; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
                    PaperSubmit AI - 让学术发表更简单<br>
                    访问系统：<a href="http://localhost:3001" style="color: #667eea;">http://localhost:3001</a>
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_notification(to_email, subject, message, html_content)
    
    def send_status_update(self, to_email, paper_title, journal_name, old_status, new_status):
        """
        发送状态更新通知
        
        Args:
            to_email: 收件人邮箱
            paper_title: 论文标题
            journal_name: 期刊名称
            old_status: 旧状态
            new_status: 新状态
        """
        status_map = {
            'pending': '待处理',
            'submitted': '已提交',
            'under_review': '审稿中',
            'revision_required': '需要修改',
            'accepted': '已接收',
            'rejected': '已拒稿'
        }
        
        old_status_text = status_map.get(old_status, old_status)
        new_status_text = status_map.get(new_status, new_status)
        
        subject = f"🔔 投稿状态更新 - {paper_title}"
        
        message = f"""
您好！

您的论文投稿状态已更新：

论文标题：{paper_title}
投稿期刊：{journal_name}
状态变更：{old_status_text} → {new_status_text}
更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

请登录系统查看详细信息。

---
PaperSubmit AI
        """
        
        # 根据状态选择颜色
        status_colors = {
            'pending': '#ffc107',
            'submitted': '#17a2b8',
            'under_review': '#28a745',
            'revision_required': '#fd7e14',
            'accepted': '#28a745',
            'rejected': '#dc3545'
        }
        
        color = status_colors.get(new_status, '#667eea')
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                <h2 style="color: #667eea;">🔔 投稿状态更新</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #667eea; margin-top: 0;">{paper_title}</h3>
                    
                    <p><strong>投稿期刊：</strong>{journal_name}</p>
                    
                    <div style="background: #f8f9ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0;">
                            <span style="color: #999;">{old_status_text}</span>
                            <span style="margin: 0 10px;">→</span>
                            <span style="color: {color}; font-weight: bold; font-size: 1.2em;">{new_status_text}</span>
                        </p>
                    </div>
                    
                    <p style="color: #666; font-size: 0.9em;">更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <a href="http://localhost:3001" style="display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">
                    查看详情
                </a>
                
                <p style="color: #999; font-size: 0.9em; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
                    PaperSubmit AI - 让学术发表更简单
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_notification(to_email, subject, message, html_content)


# 测试代码
if __name__ == "__main__":
    print("🧪 测试邮件通知模块\n")
    
    notifier = EmailNotifier()
    
    # 测试投稿创建通知
    print("测试1: 投稿创建通知")
    test_email = "test@example.com"  # 替换为真实邮箱测试
    
    result = notifier.send_submission_created(
        to_email=test_email,
        paper_title="Deep Learning for Image Classification",
        journal_name="IEEE TPAMI",
        submission_id=1
    )
    
    if result:
        print("✅ 测试通过")
    else:
        print("⚠️ 测试失败（可能是邮件配置未设置）")
    
    print("\n💡 提示：")
    print("   要启用邮件通知，请在.env文件中添加：")
    print("   SMTP_SERVER=smtp.gmail.com")
    print("   SMTP_PORT=587")
    print("   SENDER_EMAIL=your_email@gmail.com")
    print("   SENDER_PASSWORD=your_app_password")
