#!/bin/bash

# 修復 STG 環境 OAuth Redirect URI 配置
# 確保 Google Cloud Console 中包含正確的 redirect URI

echo "🔧 修復 STG 環境 OAuth Redirect URI 配置"
echo "════════════════════════════════════════════"

# 正確的 STG 環境 URLs
STG_URL_PRIMARY="https://japan-property-analyzer-2dal3iq3qa-an.a.run.app"
STG_URL_ALTERNATIVE="https://japan-property-analyzer-864942598341.asia-northeast1.run.app"

echo "✅ 正確的 STG 環境: $STG_URL_PRIMARY"
echo "⚠️  備用 URL (如果存在): $STG_URL_ALTERNATIVE"
echo ""

echo "📋 需要在 Google Cloud Console 中配置的 Redirect URIs:"
echo "   1. ${STG_URL_PRIMARY}/auth/callback"
echo "   2. ${STG_URL_ALTERNATIVE}/auth/callback (備用)"
echo ""

echo "📍 配置步驟:"
echo "   1. 前往 Google Cloud Console"
echo "   2. 選擇專案: project-japan-462310"
echo "   3. 前往 APIs & Services > Credentials"
echo "   4. 編輯 OAuth 2.0 Client ID"
echo "   5. 在 'Authorized redirect URIs' 中添加:"
echo "      - ${STG_URL_PRIMARY}/auth/callback"
echo "      - ${STG_URL_ALTERNATIVE}/auth/callback"
echo ""

# 測試當前的 OAuth 配置
echo "🧪 測試當前 OAuth 配置..."

echo "測試主要 STG 環境:"
curl -s "${STG_URL_PRIMARY}/auth/login" -w "\nHTTP 狀態碼: %{http_code}\n" | head -5

echo -e "\n測試備用環境:"
curl -s "${STG_URL_ALTERNATIVE}/auth/login" -w "\nHTTP 狀態碼: %{http_code}\n" | head -5

echo ""
echo "🌐 請在瀏覽器中訪問以下 URL 測試 OAuth:"
echo "   主要: ${STG_URL_PRIMARY}"
echo "   備用: ${STG_URL_ALTERNATIVE}"
echo ""

echo "📚 完整說明文件: docs/archive/oauth-fixes/" 