#!/bin/bash

# PRD 環境 OAuth 修復腳本
# 修復 PRD 環境的 OAuth invalid_client 錯誤

set -e

echo "🚀 開始修復 PRD 環境 OAuth 配置..."

# 設定專案 ID
PROJECT_ID="project-japan-462310"
SERVICE_NAME="japan-property-analyzer-prod"
REGION="asia-northeast1"

echo "📋 專案資訊:"
echo "  - 專案 ID: $PROJECT_ID"
echo "  - 服務名稱: $SERVICE_NAME"
echo "  - 區域: $REGION"

# 檢查 gcloud 認證
echo "🔐 檢查 gcloud 認證狀態..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ 請先執行 gcloud auth login"
    exit 1
fi

# 設定專案
echo "🎯 設定 gcloud 專案..."
gcloud config set project $PROJECT_ID

# 檢查 Secret Manager 憑證
echo "🔍 檢查 Secret Manager 憑證..."
echo "檢查 google-oauth-client-id..."
CLIENT_ID=$(gcloud secrets versions access latest --secret=google-oauth-client-id 2>/dev/null || echo "")
if [ -z "$CLIENT_ID" ]; then
    echo "❌ 無法獲取 google-oauth-client-id"
    exit 1
fi

echo "檢查 google-oauth-client-secret..."
CLIENT_SECRET=$(gcloud secrets versions access latest --secret=google-oauth-client-secret 2>/dev/null || echo "")
if [ -z "$CLIENT_SECRET" ]; then
    echo "❌ 無法獲取 google-oauth-client-secret"
    exit 1
fi

echo "✅ Secret Manager 憑證檢查通過"
echo "  - Client ID 長度: ${#CLIENT_ID}"
echo "  - Client Secret 長度: ${#CLIENT_SECRET}"

# 檢查 Cloud Build 服務帳戶權限
echo "🔑 檢查 Cloud Build 服務帳戶權限..."
BUILD_SA="864942598341@cloudbuild.gserviceaccount.com"

# 添加 Secret Manager 權限
echo "添加 Secret Manager 存取權限..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$BUILD_SA" \
    --role="roles/secretmanager.secretAccessor" \
    --quiet

echo "✅ Cloud Build 權限設定完成"

# 手動更新 PRD 環境 Cloud Run 服務
echo "🔄 手動更新 PRD 環境 Cloud Run 服務..."

# 獲取當前服務資訊
echo "獲取當前服務資訊..."
CURRENT_IMAGE=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(spec.template.spec.template.spec.containers[0].image)" 2>/dev/null || echo "")

if [ -z "$CURRENT_IMAGE" ]; then
    echo "❌ 無法獲取當前服務映像，請檢查服務是否存在"
    exit 1
fi

echo "當前映像: $CURRENT_IMAGE"

# 更新服務環境變數
echo "更新服務環境變數..."
gcloud run services update $SERVICE_NAME \
    --region=$REGION \
    --set-env-vars "GA_TRACKING_ID=G-94SVDFL5YN,ENVIRONMENT=production,NO_INDEX=false,SECRET_KEY=ecd48ef5097e192fd1a9c27bd04e3fe66910f9feac345df64753747064087c6f,GOOGLE_CLIENT_ID=$CLIENT_ID,GOOGLE_CLIENT_SECRET=$CLIENT_SECRET" \
    --quiet

echo "✅ PRD 環境服務更新完成"

# 驗證服務狀態
echo "🔍 驗證服務狀態..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
echo "服務網址: $SERVICE_URL"

# 測試服務健康狀態
echo "測試服務健康狀態..."
if curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL" | grep -q "200"; then
    echo "✅ 服務健康檢查通過"
else
    echo "⚠️  服務可能需要幾分鐘才能完全啟動"
fi

echo ""
echo "🎉 PRD 環境 OAuth 修復完成！"
echo ""
echo "📋 修復摘要:"
echo "  ✅ Secret Manager 憑證驗證通過"
echo "  ✅ Cloud Build 服務帳戶權限已設定"
echo "  ✅ PRD 環境服務已更新真實 OAuth 憑證"
echo ""
echo "🔗 測試網址:"
echo "  PRD: $SERVICE_URL"
echo ""
echo "⚠️  注意事項:"
echo "  1. 請在 Google Cloud Console 中添加 PRD 重定向 URI"
echo "  2. 服務可能需要 2-3 分鐘才能完全生效"
echo "  3. 如果仍有問題，請檢查 Cloud Run 日誌"
echo "" 