#!/usr/bin/env python3
"""
PaperSubmit AI - 完整功能演示脚本
展示系统的所有核心功能
"""
import requests
import time
import os

BASE_URL = "http://localhost:8000"

def print_header(title):
    """打印标题"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_success(message):
    """打印成功消息"""
    print(f"✅ {message}")

def print_info(message):
    """打印信息"""
    print(f"ℹ️  {message}")

def print_result(data, indent=3):
    """打印结果"""
    spaces = " " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f"{spaces}{key}:")
                print_result(value, indent + 3)
            else:
                print(f"{spaces}{key}: {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data, 1):
            print(f"{spaces}[{i}]")
            print_result(item, indent + 3)
    else:
        print(f"{spaces}{data}")

def demo_system_health():
    """演示1: 系统健康检查"""
    print_header("演示1: 系统健康检查")
    
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print_success("API服务运行正常")
        print_result(response.json())
    else:
        print("❌ API服务异常")
        return False
    
    return True

def demo_paper_upload():
    """演示2: 论文上传"""
    print_header("演示2: 论文上传")
    
    # 创建测试PDF
    test_file = "/tmp/demo_paper.pdf"
    with open(test_file, "w") as f:
        f.write("%PDF-1.4\nDemo paper for PaperSubmit AI")
    
    print_info("上传论文: 'Transformer Architecture for NLP Tasks'")
    
    files = {'file': ('demo_paper.pdf', open(test_file, 'rb'), 'application/pdf')}
    data = {
        'title': 'Attention Is All You Need: Transformer Architecture for NLP Tasks',
        'authors': 'Ashish Vaswani, Noam Shazeer, Niki Parmar',
        'abstract': '''We propose a new simple network architecture, the Transformer, 
        based solely on attention mechanisms, dispensing with recurrence and convolutions 
        entirely. Experiments on machine translation tasks show these models to be superior 
        in quality while being more parallelizable and requiring significantly less time 
        to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation 
        task and 41.8 BLEU on the WMT 2014 English-to-French translation task. We demonstrate 
        that the Transformer generalizes well to other tasks by applying it successfully to 
        English constituency parsing with large and limited training data. The architecture 
        uses self-attention to compute representations of its input and output without using 
        sequence-aligned RNNs or convolution. This allows for more parallelization and has 
        become the foundation for models like BERT, GPT, and many other natural language 
        processing breakthroughs.'''
    }
    
    response = requests.post(f"{BASE_URL}/api/papers/upload", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print_success(f"论文上传成功 (ID: {result['paper_id']})")
        print_result(result)
        return result['paper_id']
    else:
        print(f"❌ 上传失败: {response.text}")
        return None

def demo_journal_recommendation(paper_id):
    """演示3: 智能期刊推荐"""
    print_header("演示3: 智能期刊推荐")
    
    print_info(f"为论文 #{paper_id} 推荐期刊...")
    
    response = requests.post(
        f"{BASE_URL}/api/journals/recommend",
        params={"paper_id": paper_id, "top_k": 5}
    )
    
    if response.status_code == 200:
        result = response.json()
        print_success("推荐成功！")
        
        print(f"\n   📝 论文: {result['paper_title']}")
        print(f"   🔑 关键词: {', '.join(result['keywords'][:8])}")
        print(f"\n   📊 推荐期刊 (Top {len(result['recommendations'])}):\n")
        
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"   {i}. {rec['journal']}")
            print(f"      ├─ 综合评分: {rec['score']:.3f}")
            print(f"      ├─ 匹配度: {rec['match_score']:.3f}")
            print(f"      ├─ 影响因子: {rec['impact_factor']}")
            print(f"      ├─ 审稿时间: {rec['review_time_days']} 天")
            print(f"      ├─ 接收率: {rec['acceptance_rate']*100:.1f}%")
            print(f"      └─ 投稿系统: {rec['submission_system']}")
            print()
        
        return result['recommendations'][0]['journal']
    else:
        print(f"❌ 推荐失败: {response.text}")
        return None

def demo_journal_search():
    """演示4: 期刊搜索"""
    print_header("演示4: 期刊搜索")
    
    queries = ["machine learning", "biology", "physics"]
    
    for query in queries:
        print_info(f"搜索关键词: '{query}'")
        
        response = requests.get(
            f"{BASE_URL}/api/journals/search",
            params={"query": query, "top_k": 3}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   找到 {result['total']} 个相关期刊:")
            for journal in result['journals']:
                print(f"      • {journal['name']} (IF: {journal['impact_factor']})")
        print()

def demo_submission_create(paper_id, journal_name):
    """演示5: 创建投稿"""
    print_header("演示5: 创建投稿")
    
    print_info(f"创建投稿: 论文 #{paper_id} -> {journal_name}")
    
    data = {
        'paper_id': paper_id,
        'journal_name': journal_name,
        'username': 'demo_user@example.com',
        'password': 'secure_password_123'
    }
    
    response = requests.post(f"{BASE_URL}/api/submissions/create", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print_success(f"投稿创建成功 (ID: {result['submission_id']})")
        print_result(result)
        return result['submission_id']
    else:
        print(f"❌ 创建失败: {response.text}")
        return None

def demo_submission_status(submission_id):
    """演示6: 查询投稿状态"""
    print_header("演示6: 查询投稿状态")
    
    print_info(f"查询投稿 #{submission_id} 的状态...")
    
    response = requests.get(f"{BASE_URL}/api/submissions/{submission_id}/status")
    
    if response.status_code == 200:
        result = response.json()
        print_success("查询成功")
        print_result(result)
    else:
        print(f"❌ 查询失败: {response.text}")

def demo_list_all():
    """演示7: 列出所有数据"""
    print_header("演示7: 列出所有数据")
    
    # 列出所有论文
    print_info("所有论文:")
    response = requests.get(f"{BASE_URL}/api/papers")
    if response.status_code == 200:
        result = response.json()
        print(f"   总数: {result['total']}")
        for paper in result['papers']:
            print(f"      • [{paper['id']}] {paper['title']}")
    
    print()
    
    # 列出所有投稿
    print_info("所有投稿:")
    response = requests.get(f"{BASE_URL}/api/submissions")
    if response.status_code == 200:
        result = response.json()
        print(f"   总数: {result['total']}")
        for sub in result['submissions']:
            print(f"      • [{sub['id']}] {sub['paper_title']} -> {sub['journal_name']} ({sub['status']})")

def demo_api_docs():
    """演示8: API文档"""
    print_header("演示8: API文档")
    
    print_info("API文档地址:")
    print(f"   📖 Swagger UI: {BASE_URL}/docs")
    print(f"   📖 ReDoc: {BASE_URL}/redoc")
    print(f"   📖 OpenAPI JSON: {BASE_URL}/openapi.json")

def main():
    """主函数"""
    print("\n" + "🚀"*35)
    print("  PaperSubmit AI - 完整功能演示")
    print("  论文自动投稿系统 v1.0")
    print("🚀"*35)
    
    # 检查API服务
    if not demo_system_health():
        print("\n❌ API服务未运行，请先启动后端服务")
        print("   运行命令: cd src/backend && python main.py")
        return
    
    time.sleep(1)
    
    # 演示论文上传
    paper_id = demo_paper_upload()
    if not paper_id:
        return
    
    time.sleep(1)
    
    # 演示期刊推荐
    journal_name = demo_journal_recommendation(paper_id)
    if not journal_name:
        return
    
    time.sleep(1)
    
    # 演示期刊搜索
    demo_journal_search()
    time.sleep(1)
    
    # 演示创建投稿
    submission_id = demo_submission_create(paper_id, journal_name)
    if not submission_id:
        return
    
    time.sleep(1)
    
    # 演示查询状态
    demo_submission_status(submission_id)
    time.sleep(1)
    
    # 演示列出所有数据
    demo_list_all()
    time.sleep(1)
    
    # API文档
    demo_api_docs()
    
    # 总结
    print("\n" + "="*70)
    print("  🎉 演示完成！")
    print("="*70)
    print("\n✅ 已演示的功能:")
    print("   1. ✓ 系统健康检查")
    print("   2. ✓ 论文上传")
    print("   3. ✓ 智能期刊推荐")
    print("   4. ✓ 期刊搜索")
    print("   5. ✓ 创建投稿")
    print("   6. ✓ 查询投稿状态")
    print("   7. ✓ 列出所有数据")
    print("   8. ✓ API文档")
    
    print("\n📊 系统状态:")
    print(f"   • API服务: {BASE_URL}")
    print(f"   • API文档: {BASE_URL}/docs")
    print(f"   • 数据库: ~/Desktop/论文投稿Agent/data/papersubmit.db")
    
    print("\n🎯 下一步:")
    print("   • 访问 API 文档查看所有端点")
    print("   • 开发前端界面")
    print("   • 完善自动化投稿功能")
    
    print("\n" + "🚀"*35 + "\n")

if __name__ == "__main__":
    main()
