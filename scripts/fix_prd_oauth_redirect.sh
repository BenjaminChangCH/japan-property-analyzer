#!/bin/bash
# PRD 環境 Google OAuth 重定向 URI 修復腳本
# 修復 redirect_uri_mismatch 錯誤

echo "🔧 PRD 環境 Google OAuth 修復腳本"
echo "=================================="
echo

# 環境資訊
PRD_URL="https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app"
REDIRECT_URI="${PRD_URL}/auth/callback"

echo "📋 環境資訊："
echo "PRD URL: $PRD_URL"
echo "重定向 URI: $REDIRECT_URI"
echo

echo "🚨 問題診斷："
echo "錯誤：redirect_uri_mismatch (400)"
echo "原因：Google Console 中的授權重定向 URI 設定不正確"
echo

echo "🔧 修復步驟："
echo "1. 前往 Google Cloud Console"
echo "   https://console.cloud.google.com/apis/credentials"
echo

echo "2. 選擇專案：project-japan-462310"
echo

echo "3. 編輯 OAuth 2.0 用戶端 ID"
echo "   找到用於此專案的 OAuth 用戶端"
echo

echo "4. 在「已授權的重新導向 URI」中添加："
echo "   $REDIRECT_URI"
echo

echo "5. 確認現有的重定向 URI："
echo "   ✅ http://localhost:5000/auth/callback (本機開發)"
echo "   ✅ https://japan-property-analyzer-2dal3iq3qa-an.a.run.app/auth/callback (STG)"
echo "   ⚠️  $REDIRECT_URI (PRD - 需要添加)"
echo

echo "6. 儲存設定"
echo

echo "🧪 測試步驟："
echo "1. 等待 Google 設定生效（約 5-10 分鐘）"
echo "2. 前往 PRD 環境測試登入"
echo "3. 確認 OAuth 流程正常運作"
echo

echo "📱 完成後測試連結："
echo "PRD 環境: $PRD_URL"
echo

# 檢查當前 Google Cloud 專案
echo "🔍 當前 Google Cloud 專案："
gcloud config get-value project 2>/dev/null || echo "未設定"
echo

echo "💡 提示："
echo "- OAuth 設定變更可能需要 5-10 分鐘生效"
echo "- 如果仍有問題，請檢查 Client ID 和 Secret 是否正確"
echo "- 確保 PRD 環境的環境變數已正確設定"
echo

echo "✅ 修復腳本執行完成"
echo "請按照上述步驟在 Google Console 中添加重定向 URI" 