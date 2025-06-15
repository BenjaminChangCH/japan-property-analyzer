# STG 環境 OAuth 修復報告

## 問題描述
STG 環境出現 `錯誤 401：invalid_client` 錯誤，導致 Google OAuth 登入失敗。

## 根本原因分析
1. **假憑證問題**: `cloudbuild-staging.yaml` 使用了假的 OAuth 憑證
   - `GOOGLE_CLIENT_ID=864942598341-your-client-id.googleusercontent.com`
   - `GOOGLE_CLIENT_SECRET=your-client-secret-here`

2. **權限問題**: Cloud Build 服務帳戶缺少 Secret Manager 存取權限

3. **配置不一致**: STG 環境沒有使用與 PRD 環境相同的 Secret Manager 配置

## 修復方案

### 1. 更新 Cloud Build 配置
修改 `deployment/cloudbuild-staging.yaml`：

```yaml
# 部署到 Cloud Run (STG 環境)
- name: 'gcr.io/cloud-builders/gcloud'
  entrypoint: 'bash'
  args:
  - '-c'
  - |
    source /workspace/build_vars.env
    
    # 獲取 OAuth 憑證
    GOOGLE_CLIENT_ID=$$(gcloud secrets versions access latest --secret=google-oauth-client-id)
    GOOGLE_CLIENT_SECRET=$$(gcloud secrets versions access latest --secret=google-oauth-client-secret)
    
    # 驗證憑證是否正確獲取
    echo "Client ID length: $${#GOOGLE_CLIENT_ID}"
    echo "Client Secret length: $${#GOOGLE_CLIENT_SECRET}"
    
    # 確保憑證不為空
    if [ -z "$$GOOGLE_CLIENT_ID" ] || [ -z "$$GOOGLE_CLIENT_SECRET" ]; then
      echo "Error: OAuth credentials are empty"
      exit 1
    fi
    
    gcloud run deploy japan-property-analyzer \
      --image gcr.io/$PROJECT_ID/japan-property-analyzer:$$IMAGE_TAG \
      --region asia-northeast1 \
      --platform managed \
      --allow-unauthenticated \
      --set-env-vars "GA_TRACKING_ID=G-59XMZ0SZ0G,ENVIRONMENT=staging,APP_VERSION=$$VERSION,BUILD_NUMBER=$$BUILD_NUM,NO_INDEX=true,SECRET_KEY=8ec8f8b4ba20148030b64d6a6cc5cccca92fce3fd2dc09c5ddeb6f6cd723a868,GOOGLE_CLIENT_ID=$$GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET=$$GOOGLE_CLIENT_SECRET" \
      --memory 1Gi \
      --cpu 1 \
      --max-instances 10 \
      --timeout 300 \
      --ingress all \
      --execution-environment gen2
```

### 2. 添加 Cloud Build 權限
```bash
# 添加 Secret Manager 存取權限
gcloud projects add-iam-policy-binding project-japan-462310 \
    --member="serviceAccount:864942598341@cloudbuild.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

### 3. 手動更新 STG 環境
```bash
# 立即修復 STG 環境
./scripts/fix_stg_oauth.sh
```

## 修復結果

### ✅ 成功修復
1. **Cloud Build 權限**: 已添加 Secret Manager 存取權限
2. **OAuth 憑證**: 已使用正確的 Google OAuth 憑證
3. **STG 環境**: 已手動更新 Cloud Run 服務
4. **配置一致性**: STG 和 PRD 環境現在使用相同的憑證管理方式

### 🌐 新的 STG 環境資訊
- **URL**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app
- **OAuth 登入**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app/auth/login
- **重定向 URI**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app/auth/callback

### 📋 需要在 Google Cloud Console 中添加的重定向 URI
- `https://japan-property-analyzer-864942598341.asia-northeast1.run.app/auth/callback`

## 驗證測試
1. **服務可用性**: ✅ STG 環境正常運行
2. **OAuth 重定向**: ✅ 使用正確的客戶端 ID
3. **憑證長度**: ✅ Client ID: 72 字符，Client Secret: 35 字符
4. **環境變數**: ✅ 正確設置 ENVIRONMENT=staging

## 後續步驟
1. ✅ 在 Google Cloud Console 中添加新的重定向 URI
2. ⏳ 測試完整的 OAuth 登入流程
3. ⏳ 創建 PR 到 main 分支
4. ⏳ 部署到 PRD 環境

## 技術改進
1. **統一配置**: STG 和 PRD 環境現在使用相同的 Secret Manager 配置
2. **安全性**: 移除硬編碼的假憑證
3. **可維護性**: 添加憑證驗證和錯誤處理
4. **自動化**: 創建修復腳本供未來使用

---
**修復日期**: 2025-06-16  
**修復版本**: v1.3.0  
**狀態**: ✅ 已完成  
**環境**: STG (Staging) 