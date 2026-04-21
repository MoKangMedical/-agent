"""
测试期刊推荐API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_journal_recommendation():
    """测试期刊推荐功能"""
    print("\n" + "="*60)
    print("🧪 测试期刊推荐API")
    print("="*60)
    
    # 首先上传一篇论文
    print("\n1️⃣ 上传测试论文...")
    
    test_file_path = "/tmp/test_ml_paper.pdf"
    with open(test_file_path, "w") as f:
        f.write("%PDF-1.4\nTest PDF for machine learning paper")
    
    files = {
        'file': ('ml_paper.pdf', open(test_file_path, 'rb'), 'application/pdf')
    }
    data = {
        'title': 'Deep Neural Networks for Image Classification',
        'authors': 'Alice Zhang, Bob Li',
        'abstract': '''This paper presents a novel deep learning approach for image classification 
        using convolutional neural networks. We propose a new architecture that combines 
        residual connections with attention mechanisms to improve classification accuracy. 
        Our method achieves state-of-the-art results on ImageNet dataset with 95.2% top-1 
        accuracy. We also demonstrate the effectiveness of our approach on medical image 
        analysis, computer vision tasks, and pattern recognition problems. The proposed 
        model is trained using transfer learning and shows excellent performance in 
        artificial intelligence applications.'''
    }
    
    response = requests.post(f"{BASE_URL}/api/papers/upload", files=files, data=data)
    
    if response.status_code != 200:
        print(f"❌ 论文上传失败: {response.text}")
        return
    
    paper_id = response.json()['paper_id']
    print(f"✅ 论文上传成功 (ID: {paper_id})")
    
    # 测试期刊推荐
    print("\n2️⃣ 获取期刊推荐...")
    
    response = requests.post(
        f"{BASE_URL}/api/journals/recommend",
        params={"paper_id": paper_id, "top_k": 5}
    )
    
    if response.status_code != 200:
        print(f"❌ 推荐失败: {response.text}")
        return
    
    result = response.json()
    
    print(f"\n✅ 推荐成功！")
    print(f"\n📝 论文: {result['paper_title']}")
    print(f"🔑 提取的关键词: {', '.join(result['keywords'][:10])}")
    print(f"\n📊 推荐期刊 (Top {len(result['recommendations'])}):\n")
    
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"{i}. {rec['journal']}")
        print(f"   ├─ 综合评分: {rec['score']:.3f}")
        print(f"   ├─ 匹配度: {rec['match_score']:.3f}")
        print(f"   ├─ 影响因子: {rec['impact_factor']}")
        print(f"   ├─ 审稿时间: {rec['review_time_days']} 天")
        print(f"   ├─ 接收率: {rec['acceptance_rate']*100:.1f}%")
        print(f"   └─ 投稿系统: {rec['submission_system']}")
        print()
    
    # 测试期刊搜索
    print("="*60)
    print("3️⃣ 测试期刊搜索...")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/api/journals/search",
        params={"query": "machine learning", "top_k": 3}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ 找到 {result['total']} 个相关期刊:")
        for journal in result['journals']:
            print(f"  • {journal['name']} (IF: {journal['impact_factor']})")
    else:
        print(f"❌ 搜索失败: {response.text}")
    
    # 测试获取期刊详情
    print("\n" + "="*60)
    print("4️⃣ 测试获取期刊详情...")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/journals/arXiv")
    
    if response.status_code == 200:
        journal = response.json()
        print(f"\n✅ 期刊详情:")
        print(f"  名称: {journal['name']}")
        print(f"  影响因子: {journal['impact_factor']}")
        print(f"  审稿时间: {journal['review_time_days']} 天")
        print(f"  接收率: {journal['acceptance_rate']*100:.1f}%")
        print(f"  关键词: {', '.join(journal['keywords'])}")
        print(f"  网址: {journal['url']}")
    else:
        print(f"❌ 获取失败: {response.text}")
    
    print("\n" + "="*60)
    print("🎉 期刊推荐功能测试完成！")
    print("="*60)


if __name__ == "__main__":
    test_journal_recommendation()
