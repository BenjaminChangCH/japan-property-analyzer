#!/bin/bash

# 本地開發環境啟動腳本
# 確保使用 5001 端口

set -e

echo "🚀 啟動日本不動產投資分析工具 - 本地開發環境"
echo "═══════════════════════════════════════════════"

# 檢查並清理端口
if lsof -ti :5001 >/dev/null 2>&1; then
    echo "⚠️  5001 端口被占用，正在清理..."
    lsof -ti :5001 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# 確認端口已釋放
if lsof -ti :5001 >/dev/null 2>&1; then
    echo "❌ 無法清理 5001 端口，請手動檢查"
    exit 1
fi

echo "✅ 5001 端口已準備就緒"

# 啟動開發伺服器
echo "🔧 啟動 Flask 開發伺服器..."
echo "📍 本地網址: http://localhost:5001"
echo "🛑 按 Ctrl+C 停止伺服器"
echo "═══════════════════════════════════════════════"

# 啟動伺服器
python main.py 