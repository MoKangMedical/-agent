#!/bin/bash

# PaperSubmit AI - 一键启动脚本

echo "🚀 PaperSubmit AI - 启动中..."
echo ""

# 检查是否在正确的目录
if [ ! -d "src/backend" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    echo "   cd ~/Desktop/论文投稿Agent"
    exit 1
fi

# 启动后端
echo "📡 启动后端服务..."
cd src/backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ../..

# 等待后端启动
sleep 3

# 启动前端
echo "🌐 启动前端服务..."
cd src/frontend/web
python3 server.py &
FRONTEND_PID=$!
cd ../../..

# 等待服务启动
sleep 2

echo ""
echo "✅ 服务启动成功！"
echo ""
echo "📊 访问地址:"
echo "   前端界面: http://localhost:3001"
echo "   后端API:  http://localhost:8000"
echo "   API文档:  http://localhost:8000/docs"
echo ""
echo "💡 提示:"
echo "   - 按 Ctrl+C 停止所有服务"
echo "   - 查看日志: tail -f ~/Documents/*.log"
echo ""

# 保存PID
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# 等待用户中断
trap "echo ''; echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f .backend.pid .frontend.pid; echo '✅ 服务已停止'; exit 0" INT

# 保持脚本运行
wait
