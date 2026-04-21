"""
PaperSubmit AI - arXiv自动投稿器（示例实现）
"""
from browser_manager import BrowserManager
from selenium.webdriver.common.by import By
import time
import os


class ArxivSubmitter:
    """arXiv自动投稿器"""
    
    def __init__(self, headless=True):
        """
        初始化投稿器
        
        Args:
            headless: 是否使用无头模式
        """
        self.base_url = "https://arxiv.org"
        self.browser = BrowserManager(headless=headless)
        print("🤖 arXiv投稿器已初始化")
    
    def login(self, username, password):
        """
        登录arXiv
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            是否登录成功
        """
        try:
            print("🔐 正在登录arXiv...")
            
            # 访问登录页面
            self.browser.get(f"{self.base_url}/login")
            time.sleep(2)
            
            # 填写用户名
            if not self.browser.input_text(By.NAME, "username", username):
                print("❌ 未找到用户名输入框")
                return False
            
            # 填写密码
            if not self.browser.input_text(By.NAME, "password", password):
                print("❌ 未找到密码输入框")
                return False
            
            # 点击登录按钮
            if not self.browser.click(By.CSS_SELECTOR, "button[type='submit']"):
                print("❌ 未找到登录按钮")
                return False
            
            time.sleep(3)
            
            # 检查是否登录成功（简单判断：URL是否改变）
            current_url = self.browser.driver.current_url
            if "login" not in current_url:
                print("✅ 登录成功")
                return True
            else:
                print("❌ 登录失败")
                return False
                
        except Exception as e:
            print(f"❌ 登录过程出错: {e}")
            return False
    
    def submit_paper(self, paper_data):
        """
        提交论文
        
        Args:
            paper_data: 论文数据字典，包含：
                - title: 标题
                - authors: 作者列表
                - abstract: 摘要
                - file_path: PDF文件路径
                - categories: 分类（可选）
        
        Returns:
            稿件编号（如果成功）
        """
        try:
            print("📤 开始提交论文...")
            
            # 访问投稿页面
            self.browser.get(f"{self.base_url}/submit")
            time.sleep(2)
            
            # 填写标题
            print("✍️ 填写标题...")
            if not self.browser.input_text(By.NAME, "title", paper_data['title']):
                print("⚠️ 标题输入失败")
            
            # 填写作者
            print("✍️ 填写作者...")
            authors_str = ", ".join(paper_data['authors'])
            if not self.browser.input_text(By.NAME, "authors", authors_str):
                print("⚠️ 作者输入失败")
            
            # 填写摘要
            print("✍️ 填写摘要...")
            if not self.browser.input_text(By.NAME, "abstract", paper_data['abstract']):
                print("⚠️ 摘要输入失败")
            
            # 上传PDF文件
            print("📎 上传PDF文件...")
            file_input = self.browser.find_element(By.CSS_SELECTOR, "input[type='file']")
            if file_input:
                file_input.send_keys(os.path.abspath(paper_data['file_path']))
                print("✅ 文件上传成功")
            else:
                print("❌ 未找到文件上传控件")
                return None
            
            time.sleep(2)
            
            # 提交表单
            print("🚀 提交表单...")
            if not self.browser.click(By.CSS_SELECTOR, "button[type='submit']"):
                print("❌ 未找到提交按钮")
                return None
            
            time.sleep(5)
            
            # 获取稿件编号（示例：从页面提取）
            submission_id = self.extract_submission_id()
            
            if submission_id:
                print(f"✅ 论文提交成功！稿件编号: {submission_id}")
                return submission_id
            else:
                print("⚠️ 提交完成，但未能获取稿件编号")
                return "UNKNOWN"
                
        except Exception as e:
            print(f"❌ 提交过程出错: {e}")
            return None
    
    def extract_submission_id(self):
        """
        从页面提取稿件编号
        
        Returns:
            稿件编号
        """
        try:
            # 尝试多种方式查找稿件编号
            # 方式1: 通过class查找
            id_element = self.browser.find_element(By.CLASS_NAME, "submission-id")
            if id_element:
                return id_element.text.strip()
            
            # 方式2: 通过URL提取
            current_url = self.browser.driver.current_url
            if "/submit/" in current_url:
                parts = current_url.split("/")
                return parts[-1]
            
            return None
            
        except Exception as e:
            print(f"⚠️ 提取稿件编号失败: {e}")
            return None
    
    def check_status(self, submission_id):
        """
        检查投稿状态
        
        Args:
            submission_id: 稿件编号
        
        Returns:
            状态字符串
        """
        try:
            print(f"🔍 检查稿件 {submission_id} 的状态...")
            
            # 访问稿件状态页面
            self.browser.get(f"{self.base_url}/user/submissions/{submission_id}")
            time.sleep(2)
            
            # 查找状态元素
            status_element = self.browser.find_element(By.CLASS_NAME, "status")
            if status_element:
                status = status_element.text.strip()
                print(f"📊 当前状态: {status}")
                return status
            else:
                print("⚠️ 未找到状态信息")
                return "unknown"
                
        except Exception as e:
            print(f"❌ 检查状态出错: {e}")
            return "error"
    
    def close(self):
        """关闭浏览器"""
        self.browser.quit()


# 测试代码
if __name__ == "__main__":
    print("🧪 测试arXiv投稿器...")
    print("⚠️ 注意: 这是一个示例实现，实际arXiv网站结构可能不同")
    print("⚠️ 需要根据实际网站调整选择器和逻辑\n")
    
    # 创建投稿器（非无头模式，方便观察）
    submitter = ArxivSubmitter(headless=False)
    
    # 测试访问arXiv首页
    print("📄 访问arXiv首页...")
    submitter.browser.get("https://arxiv.org")
    time.sleep(3)
    
    print("✅ 基础功能测试完成")
    print("💡 提示: 实际使用时需要提供真实的账号和论文数据")
    
    submitter.close()
