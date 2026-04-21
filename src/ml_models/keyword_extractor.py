"""
PaperSubmit AI - 关键词提取器
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import PyPDF2
import re
import os


class KeywordExtractor:
    """论文关键词提取器"""
    
    def __init__(self, max_keywords=10):
        """
        初始化提取器
        
        Args:
            max_keywords: 最大关键词数量
        """
        self.max_keywords = max_keywords
        self.vectorizer = TfidfVectorizer(
            max_features=max_keywords,
            stop_words='english',
            ngram_range=(1, 2)  # 支持1-2个词的短语
        )
        print(f"✅ 关键词提取器初始化完成 (最多提取{max_keywords}个关键词)")
    
    def extract_from_pdf(self, pdf_path):
        """
        从PDF文件提取关键词
        
        Args:
            pdf_path: PDF文件路径
        
        Returns:
            关键词列表
        """
        try:
            print(f"📄 正在读取PDF: {os.path.basename(pdf_path)}")
            
            # 读取PDF文本
            text = self._read_pdf(pdf_path)
            
            if not text or len(text.strip()) < 100:
                print("⚠️ PDF文本内容过少，使用默认关键词")
                return ["machine learning", "artificial intelligence", "research"]
            
            # 提取关键词
            keywords = self.extract_from_text(text)
            
            print(f"✅ 成功提取 {len(keywords)} 个关键词")
            return keywords
            
        except Exception as e:
            print(f"❌ PDF读取失败: {e}")
            return ["research", "science", "study"]
    
    def _read_pdf(self, pdf_path):
        """
        读取PDF文件内容
        
        Args:
            pdf_path: PDF文件路径
        
        Returns:
            文本内容
        """
        text = ""
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                
                # 只读取前5页（通常包含摘要和引言）
                pages_to_read = min(5, num_pages)
                print(f"   读取前 {pages_to_read} 页...")
                
                for i in range(pages_to_read):
                    page = reader.pages[i]
                    text += page.extract_text()
            
            # 清理文本
            text = self._clean_text(text)
            print(f"   提取文本长度: {len(text)} 字符")
            
            return text
            
        except Exception as e:
            print(f"   ⚠️ PDF解析错误: {e}")
            return ""
    
    def _clean_text(self, text):
        """
        清理文本
        
        Args:
            text: 原始文本
        
        Returns:
            清理后的文本
        """
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符（保留字母、数字、空格）
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # 转换为小写
        text = text.lower()
        
        return text.strip()
    
    def extract_from_text(self, text):
        """
        从文本提取关键词
        
        Args:
            text: 文本内容
        
        Returns:
            关键词列表
        """
        try:
            # 使用TF-IDF提取关键词
            tfidf_matrix = self.vectorizer.fit_transform([text])
            feature_names = self.vectorizer.get_feature_names_out()
            
            # 获取TF-IDF分数
            scores = tfidf_matrix.toarray()[0]
            
            # 按分数排序
            keyword_scores = list(zip(feature_names, scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            # 返回关键词（不含分数）
            keywords = [kw for kw, score in keyword_scores if score > 0]
            
            return keywords[:self.max_keywords]
            
        except Exception as e:
            print(f"⚠️ 关键词提取失败: {e}")
            return []
    
    def extract_from_abstract(self, abstract):
        """
        从摘要提取关键词（快速方法）
        
        Args:
            abstract: 摘要文本
        
        Returns:
            关键词列表
        """
        # 清理文本
        clean_abstract = self._clean_text(abstract)
        
        # 提取关键词
        return self.extract_from_text(clean_abstract)


# 测试代码
if __name__ == "__main__":
    print("🧪 测试关键词提取器\n")
    
    extractor = KeywordExtractor(max_keywords=10)
    
    # 测试1: 从摘要提取
    print("\n" + "="*50)
    print("测试1: 从摘要提取关键词")
    print("="*50)
    
    test_abstract = """
    This paper presents a novel deep learning approach for automated paper submission 
    in academic publishing. We propose a system that combines natural language processing, 
    machine learning, and browser automation to streamline the journal selection and 
    submission process. Our method achieves 95% accuracy in journal recommendation 
    and reduces submission time by 80%. Experimental results on a dataset of 10,000 
    papers demonstrate the effectiveness of our approach in computer science, 
    artificial intelligence, and machine learning domains.
    """
    
    keywords = extractor.extract_from_abstract(test_abstract)
    print(f"\n提取的关键词: {keywords}")
    
    # 测试2: 从PDF提取（如果存在测试文件）
    print("\n" + "="*50)
    print("测试2: 从PDF提取关键词")
    print("="*50)
    
    test_pdf = "../../data/papers/test_paper.pdf"
    if os.path.exists(test_pdf):
        keywords = extractor.extract_from_pdf(test_pdf)
        print(f"\n提取的关键词: {keywords}")
    else:
        print("⚠️ 测试PDF文件不存在，跳过此测试")
    
    print("\n✅ 关键词提取器测试完成！")
