#!/bin/bash
# 百问即查 启动脚本
# 用法: bash start.sh

PORT=${SERVER_PORT:-9010}

echo ">>> 百问即查 v1.0.4 <<<"
echo ">>> 停止旧进程..."
taskkill //f //im python.exe 2>/dev/null
sleep 2

echo ">>> 启动服务: http://localhost:${PORT}"
cd "$(dirname "$0")"
python main.py
