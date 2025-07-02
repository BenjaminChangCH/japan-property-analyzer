#!/bin/bash

# NIPPON PROPERTY ANALYTICS - 開發環境啟動腳本
# 統一使用 port 5001 進行本地開發

echo "🚀 啟動 NIPPON PROPERTY ANALYTICS 開發環境..."
echo "📍 本地地址: http://localhost:5001"
echo "🔧 Google OAuth 已配置使用 port 5001"
echo ""

# 設定環境變數
export ENVIRONMENT=development
export PORT=5001

# 啟動應用程式
python main.py 