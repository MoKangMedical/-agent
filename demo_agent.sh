#!/bin/bash

# PaperSubmit AI - 使用演示脚本

echo "🎓 PaperSubmit AI 桌面Agent - 使用演示"
echo "=========================================="
echo ""

# 设置监控文件夹
PAPERS_DIR="$HOME/Documents/Papers"

echo "📁 监控文件夹: $PAPERS_DIR"
echo ""

# 步骤1
echo "步骤 1️⃣: 创建测试论文"
echo "----------------------------------------"
cat > "$PAPERS_DIR/demo_paper.pdf" << 'EOF'
%PDF-1.4
Demo Paper: Deep Learning for Image Classification

Abstract:
This paper presents a novel deep learning approach for image classification
using convolutional neural networks and transfer learning. We achieve
state-of-the-art results on ImageNet dataset with 95% accuracy.

Keywords: deep learning, machine learning, computer vision, neural networks,
image classification, transfer learning, artificial intelligence
EOF

echo "✅ 已创建: demo_paper.pdf"
echo ""

# 步骤2
echo "步骤 2️⃣: 手动触发Agent扫描"
echo "----------------------------------------"
cd "$(dirname "$0")/src/backend"
source venv/bin/activate
python desktop_agent.py --folder "$PAPERS_DIR" --once
echo ""

# 步骤3
echo "步骤 3️⃣: 查看生成的推荐报告"
echo "----------------------------------------"
if [ -f "$PAPERS_DIR/demo_paper_推荐报告.txt" ]; then
    echo "✅ 推荐报告已生成！"
    echo ""
    echo "📊 报告内容预览："
    echo "----------------------------------------"
    head -30 "$PAPERS_DIR/demo_paper_推荐报告.txt"
    echo "..."
    echo "----------------------------------------"
else
    echo "⚠️ 推荐报告尚未生成"
fi
echo ""

# 步骤4
echo "步骤 4️⃣: 创建投稿信息（示例）"
echo "----------------------------------------"
cat > "$PAPERS_DIR/demo_paper_投稿信息.json" << 'EOF'
{
  "journal_name": "arXiv",
  "username": "demo_user",
  "password": "demo_password",
  "notes": "这是一个演示投稿"
}
EOF
echo "✅ 已创建: demo_paper_投稿信息.json"
echo ""

# 步骤5
echo "步骤 5️⃣: 再次触发Agent处理投稿"
echo "----------------------------------------"
python desktop_agent.py --folder "$PAPERS_DIR" --once
echo ""

# 步骤6
echo "步骤 6️⃣: 查看投稿确认"
echo "----------------------------------------"
if [ -f "$PAPERS_DIR/demo_paper_投稿确认.txt" ]; then
    echo "✅ 投稿确认已生成！"
    echo ""
    echo "📋 确认内容："
    echo "----------------------------------------"
    cat "$PAPERS_DIR/demo_paper_投稿确认.txt"
    echo "----------------------------------------"
else
    echo "⚠️ 投稿确认尚未生成"
fi
echo ""

# 步骤7
echo "步骤 7️⃣: 查看状态总览"
echo "----------------------------------------"
if [ -f "$PAPERS_DIR/投稿状态总览.txt" ]; then
    cat "$PAPERS_DIR/投稿状态总览.txt"
else
    echo "⚠️ 状态总览尚未生成"
fi
echo ""

# 总结
echo "=========================================="
echo "🎉 演示完成！"
echo ""
echo "📂 生成的文件："
ls -lh "$PAPERS_DIR" | grep demo_paper
echo ""
echo "💡 提示："
echo "  - 查看推荐报告: cat $PAPERS_DIR/demo_paper_推荐报告.txt"
echo "  - 查看投稿确认: cat $PAPERS_DIR/demo_paper_投稿确认.txt"
echo "  - 查看状态总览: cat $PAPERS_DIR/投稿状态总览.txt"
echo "  - 查看Agent日志: cat $PAPERS_DIR/.papersubmit/agent.log"
echo ""
echo "🚀 开始使用："
echo "  1. 将你的PDF放入: $PAPERS_DIR"
echo "  2. 启动Agent: ./start_agent.sh"
echo "  3. Agent会自动处理！"
echo ""
