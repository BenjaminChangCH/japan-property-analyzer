#!/bin/bash
# 多環境版本同步檢查腳本

echo "🔍 檢查各環境版本同步狀況..."
echo "=================================="

# 本機版本
echo "📱 本機 DEV 環境:"
echo "Git 版本: $(git rev-parse --short HEAD)"
echo "程式版本: $(python3 -c "from version import get_version_info; print(get_version_info()['version'])")"
echo ""

# STG 環境檢查
echo "🧪 STG 測試環境:"
STG_URL="https://japan-property-analyzer-stg-366005894157.asia-east1.run.app"
curl -s "$STG_URL/version" | python3 -m json.tool || echo "❌ STG 環境無法連接"
echo ""

# PRD 環境檢查  
echo "🚀 PRD 生產環境:"
PRD_URL="https://japan-property-analyzer-366005894157.asia-east1.run.app"
curl -s "$PRD_URL/version" | python3 -m json.tool || echo "❌ PRD 環境無法連接"
echo ""

# 同步建議
echo "💡 同步建議:"
echo "1. 確保所有環境版本一致"
echo "2. 如有差異，按照 STG→PRD 流程部署"
echo "3. 本機開發前執行: git pull origin main" 