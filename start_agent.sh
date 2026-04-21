#!/bin/bash

# PaperSubmit AI - 桌面Agent启动脚本

echo "🤖 PaperSubmit AI - 桌面Agent"
echo ""

# 默认监控文件夹
DEFAULT_FOLDER="$HOME/Documents/Papers"

# 检查参数
if [ "$1" != "" ]; then
    WATCH_FOLDER="$1"
else
    WATCH_FOLDER="$DEFAULT_FOLDER"
fi

# 创建监控文件夹
mkdir -p "$WATCH_FOLDER"

echo "📁 监控文件夹: $WATCH_FOLDER"
echo ""

# 进入项目目录
cd "$(dirname "$0")/src/backend"

# 激活虚拟环境
source venv/bin/activate

# 启动Agent
echo "🚀 启动Agent..."
echo ""
python desktop_agent.py --folder "$WATCH_FOLDER"
