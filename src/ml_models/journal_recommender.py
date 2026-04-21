"""
PaperSubmit AI - 期刊推荐器
"""
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class JournalRecommender:
    """期刊智能推荐器"""
    
    def __init__(self, journal_db_path=None):
        """
        初始化推荐器
        
        Args:
            journal_db_path: 期刊数据库JSON文件路径
        """
        if journal_db_path is None:
            # 默认路径
            journal_db_path = os.path.join(
                os.path.dirname(__file__),
                "../../config/journals/database.json"
            )
        
        # 加载期刊数据库
        self.journals = self._load_journals(journal_db_path)
        print(f"✅ 加载了 {len(self.journals)} 个期刊")
        
        # 初始化TF-IDF向量化器
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1
        )
        
        # 预处理期刊关键词
        self._prepare_journal_vectors()
    
    def _load_journals(self, path):
        """
        加载期刊数据库
        
        Args:
            path: JSON文件路径
        
        Returns:
            期刊列表
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                journals = json.load(f)
            return journals
        except Exception as e:
            print(f"❌ 加载期刊数据库失败: {e}")
            return []
    
    def _prepare_journal_vectors(self):
        """预处理期刊关键词向量"""
        if not self.journals:
            print("⚠️ 期刊数据库为空")
            return
        
        # 将每个期刊的关键词合并为文本
        journal_texts = []
        for journal in self.journals:
            # 合并关键词和期刊名称
            text = " ".join(journal['keywords'])
            text += " " + journal['name'].lower()
            journal_texts.append(text)
        
        # 生成TF-IDF向量
        self.journal_vectors = self.vectorizer.fit_transform(journal_texts)
        print(f"✅ 期刊向量化完成 (维度: {self.journal_vectors.shape})")
    
    def recommend(self, paper_keywords, top_k=5, filters=None):
        """
        推荐期刊
        
        Args:
            paper_keywords: 论文关键词列表
            top_k: 返回前K个推荐
            filters: 过滤条件字典，例如 {'min_impact_factor': 5.0}
        
        Returns:
            推荐期刊列表，每个包含期刊信息和评分
        """
        if not paper_keywords:
            print("⚠️ 论文关键词为空，返回默认推荐")
            return self._get_default_recommendations(top_k)
        
        print(f"🔍 基于关键词推荐期刊: {paper_keywords[:5]}...")
        
        # 将论文关键词转换为向量
        paper_text = " ".join(paper_keywords)
        paper_vector = self.vectorizer.transform([paper_text])
        
        # 计算相似度
        similarities = cosine_similarity(paper_vector, self.journal_vectors)[0]
        
        # 计算综合评分
        scores = []
        for i, journal in enumerate(self.journals):
            # 应用过滤条件
            if filters and not self._apply_filters(journal, filters):
                continue
            
            # 相似度得分 (40%)
            match_score = similarities[i] * 0.4
            
            # 影响因子得分 (30%)
            # 归一化：假设最高影响因子为200
            if_score = min(journal['impact_factor'] / 200.0, 1.0) * 0.3
            
            # 审稿速度得分 (20%)
            # 归一化：假设最快3天，最慢180天
            speed_score = (1 - min(journal['review_time_days'] / 180.0, 1.0)) * 0.2
            
            # 接收率得分 (10%)
            acceptance_score = journal['acceptance_rate'] * 0.1
            
            # 总分
            total_score = match_score + if_score + speed_score + acceptance_score
            
            scores.append({
                'journal': journal['name'],
                'score': total_score,
                'match_score': similarities[i],
                'impact_factor': journal['impact_factor'],
                'review_time_days': journal['review_time_days'],
                'acceptance_rate': journal['acceptance_rate'],
                'url': journal.get('url', ''),
                'submission_system': journal.get('submission_system', 'unknown'),
                'details': {
                    'match_contribution': match_score,
                    'if_contribution': if_score,
                    'speed_contribution': speed_score,
                    'acceptance_contribution': acceptance_score
                }
            })
        
        # 排序并返回Top K
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"✅ 生成了 {len(scores)} 个推荐，返回前 {top_k} 个")
        
        return scores[:top_k]
    
    def _apply_filters(self, journal, filters):
        """
        应用过滤条件
        
        Args:
            journal: 期刊信息
            filters: 过滤条件
        
        Returns:
            是否通过过滤
        """
        if 'min_impact_factor' in filters:
            if journal['impact_factor'] < filters['min_impact_factor']:
                return False
        
        if 'max_review_time' in filters:
            if journal['review_time_days'] > filters['max_review_time']:
                return False
        
        if 'min_acceptance_rate' in filters:
            if journal['acceptance_rate'] < filters['min_acceptance_rate']:
                return False
        
        if 'submission_system' in filters:
            if journal.get('submission_system') != filters['submission_system']:
                return False
        
        return True
    
    def _get_default_recommendations(self, top_k):
        """
        获取默认推荐（当没有关键词时）
        
        Args:
            top_k: 返回数量
        
        Returns:
            默认推荐列表
        """
        # 按影响因子排序
        sorted_journals = sorted(
            self.journals,
            key=lambda x: x['impact_factor'],
            reverse=True
        )
        
        return [
            {
                'journal': j['name'],
                'score': 0.5,
                'match_score': 0.0,
                'impact_factor': j['impact_factor'],
                'review_time_days': j['review_time_days'],
                'acceptance_rate': j['acceptance_rate'],
                'url': j.get('url', ''),
                'submission_system': j.get('submission_system', 'unknown')
            }
            for j in sorted_journals[:top_k]
        ]
    
    def get_journal_info(self, journal_name):
        """
        获取期刊详细信息
        
        Args:
            journal_name: 期刊名称
        
        Returns:
            期刊信息字典
        """
        for journal in self.journals:
            if journal['name'].lower() == journal_name.lower():
                return journal
        return None
    
    def search_journals(self, query, top_k=10):
        """
        搜索期刊
        
        Args:
            query: 搜索关键词
            top_k: 返回数量
        
        Returns:
            匹配的期刊列表
        """
        query = query.lower()
        results = []
        
        for journal in self.journals:
            # 在名称和关键词中搜索
            if query in journal['name'].lower():
                results.append(journal)
            elif any(query in kw.lower() for kw in journal['keywords']):
                results.append(journal)
        
        return results[:top_k]


# 测试代码
if __name__ == "__main__":
    print("🧪 测试期刊推荐器\n")
    
    recommender = JournalRecommender()
    
    # 测试1: 基于关键词推荐
    print("\n" + "="*60)
    print("测试1: 基于关键词推荐期刊")
    print("="*60)
    
    test_keywords = [
        "machine learning",
        "deep learning",
        "neural networks",
        "artificial intelligence",
        "computer vision",
        "pattern recognition"
    ]
    
    recommendations = recommender.recommend(test_keywords, top_k=5)
    
    print("\n📊 推荐结果:\n")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['journal']}")
        print(f"   综合评分: {rec['score']:.3f}")
        print(f"   匹配度: {rec['match_score']:.3f}")
        print(f"   影响因子: {rec['impact_factor']}")
        print(f"   审稿时间: {rec['review_time_days']} 天")
        print(f"   接收率: {rec['acceptance_rate']*100:.1f}%")
        print(f"   投稿系统: {rec['submission_system']}")
        print()
    
    # 测试2: 带过滤条件的推荐
    print("="*60)
    print("测试2: 带过滤条件的推荐 (影响因子 > 10)")
    print("="*60)
    
    filters = {'min_impact_factor': 10.0}
    recommendations = recommender.recommend(test_keywords, top_k=3, filters=filters)
    
    print("\n📊 推荐结果:\n")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['journal']} (IF: {rec['impact_factor']})")
    
    # 测试3: 搜索期刊
    print("\n" + "="*60)
    print("测试3: 搜索期刊 (关键词: 'nature')")
    print("="*60)
    
    results = recommender.search_journals("nature")
    print(f"\n找到 {len(results)} 个期刊:")
    for journal in results:
        print(f"  • {journal['name']}")
    
    # 测试4: 生物学领域推荐
    print("\n" + "="*60)
    print("测试4: 生物学领域推荐")
    print("="*60)
    
    bio_keywords = [
        "biology",
        "molecular biology",
        "genetics",
        "cell biology",
        "genomics"
    ]
    
    recommendations = recommender.recommend(bio_keywords, top_k=5)
    
    print("\n📊 推荐结果:\n")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['journal']} (评分: {rec['score']:.3f})")
    
    print("\n✅ 期刊推荐器测试完成！")
