#!/bin/bash

# PaperSubmit AI - 停止脚本

echo "🛑 正在停止 PaperSubmit AI 服务..."
echo ""

# 停止后端（端口8000）
echo "📡 停止后端服务..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ 后端服务已停止"
else
    echo "   ℹ️  后端服务未运行"
fi

# 停止前端（端口3001）
echo "🌐 停止前端服务..."
lsof -ti:3001 | xargs kill -9 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ 前端服务已停止"
else
    echo "   ℹ️  前端服务未运行"
fi

# 清理PID文件
rm -f .backend.pid .frontend.pid 2>/dev/null

echo ""
echo "✅ 所有服务已停止"
