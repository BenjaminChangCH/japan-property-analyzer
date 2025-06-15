#!/bin/bash

# 修復 STG 環境 OAuth 配置腳本
# 確保 Cloud Build 服務帳戶有 Secret Manager 權限

set -e

PROJECT_ID="project-japan-462310"
PROJECT_NUMBER="864942598341"
REGION="asia-northeast1"

echo "🔧 修復 STG 環境 OAuth 配置..."

# 1. 確保 Cloud Build 服務帳戶有 Secret Manager 權限
echo "📋 檢查 Cloud Build 服務帳戶權限..."
CLOUD_BUILD_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

echo "🔑 添加 Secret Manager 權限..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${CLOUD_BUILD_SA}" \
    --role="roles/secretmanager.secretAccessor" \
    --quiet

# 2. 驗證 Secret Manager 中的憑證
echo "🔍 驗證 Secret Manager 憑證..."
CLIENT_ID=$(gcloud secrets versions access latest --secret=google-oauth-client-id)
CLIENT_SECRET=$(gcloud secrets versions access latest --secret=google-oauth-client-secret)

echo "Client ID length: ${#CLIENT_ID}"
echo "Client Secret length: ${#CLIENT_SECRET}"

if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ]; then
    echo "❌ 錯誤：OAuth 憑證為空"
    exit 1
fi

# 3. 手動更新 STG 環境的 Cloud Run 服務
echo "🚀 手動更新 STG 環境 Cloud Run 服務..."
gcloud run services update japan-property-analyzer \
    --region=$REGION \
    --update-env-vars "GOOGLE_CLIENT_ID=${CLIENT_ID},GOOGLE_CLIENT_SECRET=${CLIENT_SECRET}" \
    --quiet

echo "✅ STG 環境 OAuth 配置修復完成！"
echo "🌐 STG 環境網址: https://japan-property-analyzer-2dal3iq3qa-an.a.run.app"
echo "🔗 測試登入: https://japan-property-analyzer-2dal3iq3qa-an.a.run.app/auth/login" 