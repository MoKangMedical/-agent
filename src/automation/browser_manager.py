"""
PaperSubmit AI - 浏览器管理器
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class BrowserManager:
    """浏览器自动化管理器"""
    
    def __init__(self, headless=True):
        """
        初始化浏览器
        
        Args:
            headless: 是否使用无头模式（不显示浏览器窗口）
        """
        options = webdriver.ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        # 常用配置
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
            print("✅ 浏览器初始化成功")
        except Exception as e:
            print(f"❌ 浏览器初始化失败: {e}")
            print("💡 提示: 请确保已安装 Chrome 浏览器和 ChromeDriver")
            raise
    
    def get(self, url):
        """访问URL"""
        self.driver.get(url)
        time.sleep(1)  # 等待页面加载
    
    def find_element(self, by, value, timeout=10):
        """
        查找元素（带等待）
        
        Args:
            by: 查找方式（By.ID, By.XPATH等）
            value: 查找值
            timeout: 超时时间（秒）
        
        Returns:
            WebElement对象
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            print(f"⚠️ 元素未找到: {by}={value}")
            return None
    
    def find_elements(self, by, value):
        """查找多个元素"""
        return self.driver.find_elements(by, value)
    
    def click(self, by, value):
        """点击元素"""
        element = self.find_element(by, value)
        if element:
            element.click()
            time.sleep(0.5)
            return True
        return False
    
    def input_text(self, by, value, text):
        """输入文本"""
        element = self.find_element(by, value)
        if element:
            element.clear()
            element.send_keys(text)
            return True
        return False
    
    def get_text(self, by, value):
        """获取元素文本"""
        element = self.find_element(by, value)
        return element.text if element else None
    
    def screenshot(self, filename):
        """截图"""
        self.driver.save_screenshot(filename)
        print(f"📸 截图已保存: {filename}")
    
    def quit(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("🔒 浏览器已关闭")


# 测试代码
if __name__ == "__main__":
    print("🧪 测试浏览器管理器...")
    
    try:
        browser = BrowserManager(headless=False)
        
        # 测试访问网页
        print("📄 访问测试页面...")
        browser.get("https://www.baidu.com")
        
        # 测试查找元素
        print("🔍 查找搜索框...")
        search_box = browser.find_element(By.ID, "kw")
        if search_box:
            print("✅ 搜索框找到了")
        
        # 等待3秒观察
        time.sleep(3)
        
        browser.quit()
        print("✅ 浏览器管理器测试通过！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
