#!/bin/bash

# OAuth 重定向 URI 修復指南腳本
# 用於修復 Google Cloud Console 中的 OAuth 客戶端重定向 URI 配置

set -e

echo "🔧 OAuth 重定向 URI 修復指南"
echo "================================"

# 配置變數
PROJECT_ID="project-japan-462310"

# 需要添加的重定向 URI
REDIRECT_URIS=(
    "http://localhost:5001/oauth2callback"
    "https://japan-property-analyzer-864942598341.asia-northeast1.run.app/oauth2callback"
    "https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app/oauth2callback"
    "https://www.benjamin-changch.com/oauth2callback"
)

# 需要添加的 JavaScript 來源
JAVASCRIPT_ORIGINS=(
    "http://localhost:5001"
    "https://japan-property-analyzer-864942598341.asia-northeast1.run.app"
    "https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app"
    "https://www.benjamin-changch.com"
)

echo "📋 PRD Google 登入失敗診斷結果"
echo "================================"
echo ""
echo "🚨 根本原因: OAuth 客戶端缺少 PRD 環境的重定向 URI"
echo ""
echo "✅ STG 環境正常工作"
echo "❌ PRD 環境登入失敗"
echo ""

echo "🛠️ 修復步驟 (需要手動執行)"
echo "================================"
echo ""

echo "1️⃣ 前往 Google Cloud Console"
echo "   網址: https://console.cloud.google.com/apis/credentials?project=$PROJECT_ID"
echo ""

echo "2️⃣ 找到並編輯 OAuth 客戶端"
echo "   Client ID: 864942598341-[實際的客戶端ID]"
echo "   名稱: 日本不動產投資分析工具"
echo ""

echo "3️⃣ 檢查「已授權的重新導向 URI」"
echo "   確保包含以下所有 URI:"
for uri in "${REDIRECT_URIS[@]}"; do
    echo "   ✓ $uri"
done
echo ""

echo "4️⃣ 檢查「已授權的 JavaScript 來源」"
echo "   確保包含以下所有來源:"
for origin in "${JAVASCRIPT_ORIGINS[@]}"; do
    echo "   ✓ $origin"
done
echo ""

echo "5️⃣ 儲存設定並等待生效"
echo "   - 點擊「儲存」按鈕"
echo "   - 等待 5-10 分鐘讓設定生效"
echo ""

echo "6️⃣ 測試修復結果"
echo "   - 前往: https://www.benjamin-changch.com"
echo "   - 點擊「使用 Google 登入」"
echo "   - 確認登入流程正常完成"
echo ""

echo "📊 環境狀態檢查"
echo "================================"
echo ""

# 檢查各環境的可訪問性
echo "🔍 檢查各環境狀態..."
echo ""

# 檢查 STG 環境
echo -n "STG 環境: "
if curl -s -o /dev/null -w "%{http_code}" https://japan-property-analyzer-864942598341.asia-northeast1.run.app | grep -q "200"; then
    echo "✅ 可訪問"
else
    echo "❌ 無法訪問"
fi

# 檢查 PRD 環境 (原始 URL)
echo -n "PRD 環境 (原始): "
if curl -s -o /dev/null -w "%{http_code}" https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app | grep -q "200"; then
    echo "✅ 可訪問"
else
    echo "❌ 無法訪問"
fi

# 檢查 PRD 環境 (自定義域名)
echo -n "PRD 環境 (自定義域名): "
if curl -s -o /dev/null -w "%{http_code}" https://www.benjamin-changch.com | grep -q "200"; then
    echo "✅ 可訪問"
else
    echo "❌ 無法訪問"
fi

echo ""
echo "⚠️  請手動檢查 Google Cloud Console 中的 OAuth 客戶端設定："
echo "   1. 前往: https://console.cloud.google.com/apis/credentials?project=$PROJECT_ID"
echo "   2. 找到 OAuth 客戶端 ID: 864942598341-[實際的客戶端ID]"
echo "   3. 點擊編輯"
echo "   4. 確認所有重定向 URI 和 JavaScript 來源都已正確設定"
echo "   5. 儲存設定"
echo ""

echo "🎯 修復完成後的預期結果："
echo "   ✅ 本機開發環境 (http://localhost:5001) - Google 登入正常"
echo "   ✅ STG 測試環境 - Google 登入正常"
echo "   ✅ PRD 生產環境 - Google 登入正常"
echo ""

echo "📝 如果修復後仍有問題，請檢查："
echo "   1. OAuth 客戶端設定是否已儲存"
echo "   2. 是否等待了足夠的時間讓設定生效 (5-10 分鐘)"
echo "   3. 瀏覽器是否有快取問題 (嘗試無痕模式)"
echo "   4. 檢查瀏覽器開發者工具的錯誤訊息"
echo ""

echo "✅ 修復指南完成！"
echo "請按照上述步驟手動修復 Google Cloud Console 中的 OAuth 設定。" 