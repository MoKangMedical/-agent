"""
PaperSubmit AI - 安全模块（凭证加密管理）
"""
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class CredentialManager:
    """凭证加密管理器"""
    
    def __init__(self):
        """初始化加密管理器"""
        # 从环境变量读取密钥
        key = os.getenv('ENCRYPTION_KEY')
        
        if not key:
            # 如果不存在，生成新密钥并保存
            key = Fernet.generate_key().decode()
            env_path = os.path.join(os.path.dirname(__file__), "../../.env")
            
            with open(env_path, 'a') as f:
                f.write(f"\nENCRYPTION_KEY={key}\n")
            
            print(f"🔑 已生成新的加密密钥并保存到 .env 文件")
        
        self.cipher = Fernet(key.encode())
    
    def encrypt_password(self, password: str) -> str:
        """
        加密密码
        
        Args:
            password: 明文密码
            
        Returns:
            加密后的密码（字符串格式）
        """
        encrypted = self.cipher.encrypt(password.encode())
        return encrypted.decode()
    
    def decrypt_password(self, encrypted_password: str) -> str:
        """
        解密密码
        
        Args:
            encrypted_password: 加密后的密码
            
        Returns:
            明文密码
        """
        decrypted = self.cipher.decrypt(encrypted_password.encode())
        return decrypted.decode()


# 测试代码
if __name__ == "__main__":
    manager = CredentialManager()
    
    # 测试加密解密
    test_password = "my_secret_password_123"
    print(f"原始密码: {test_password}")
    
    encrypted = manager.encrypt_password(test_password)
    print(f"加密后: {encrypted}")
    
    decrypted = manager.decrypt_password(encrypted)
    print(f"解密后: {decrypted}")
    
    assert test_password == decrypted, "加密解密测试失败！"
    print("✅ 加密解密测试通过！")
