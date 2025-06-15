# Google OAuth 修復報告

## 問題描述
STG 環境出現 Google OAuth 登入錯誤：
- 錯誤訊息：「已封鎖存取權：授權錯誤」
- 錯誤代碼：401 invalid_client
- 原因：使用了佔位符憑證而非真實的 Google OAuth 憑證

## 解決方案

### 1. 獲取真實 OAuth 憑證
- 從 Google Cloud Console 獲取真實的 Client ID 和 Client Secret
- Client ID: `864942598341-[REDACTED].apps.googleusercontent.com`
- 重定向 URI 已正確配置：
  - `http://localhost:5000/auth/callback` (本地開發)
  - `https://japan-property-analyzer-864942598341.asia-northeast1.run.app/auth/callback` (STG)

### 2. 使用 Google Cloud Secret Manager
為了安全性，將敏感憑證存儲在 Secret Manager 中：
```bash
# 創建密鑰
gcloud secrets create google-oauth-client-id --data-file=-
gcloud secrets create google-oauth-client-secret --data-file=-
```

### 3. 更新 Cloud Run 環境變數
直接更新現有服務的環境變數：

#### STG 環境
```bash
gcloud run services update japan-property-analyzer \
  --region=asia-northeast1 \
  --set-env-vars="GOOGLE_CLIENT_ID=[REDACTED],GOOGLE_CLIENT_SECRET=[REDACTED],SECRET_KEY=[REDACTED]"
```

#### PRD 環境
```bash
gcloud run services update japan-property-analyzer-prod \
  --region=asia-northeast1 \
  --set-env-vars="GOOGLE_CLIENT_ID=[REDACTED],GOOGLE_CLIENT_SECRET=[REDACTED],SECRET_KEY=[REDACTED]"
```

### 4. 更新 Cloud Build 配置
修改 `deployment/cloudbuild-staging.yaml` 和 `deployment/cloudbuild-production.yaml`：
- 使用 Secret Manager 獲取憑證：`$$(gcloud secrets versions access latest --secret=google-oauth-client-id)`
- 避免在代碼庫中硬編碼敏感資訊

## 測試結果

### STG 環境測試
- ✅ 服務正常運行：HTTP 200
- ✅ OAuth 重定向正常：成功重定向到 `accounts.google.com`
- ✅ 環境變數已更新：包含正確的 Client ID 和 Secret
- 🔗 STG URL: https://japan-property-analyzer-864942598341.asia-northeast1.run.app

### PRD 環境測試
- ✅ 服務正常運行：HTTP 200
- ✅ 環境變數已更新：包含正確的 Client ID 和 Secret
- 🔗 PRD URL: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app

## 安全性改進

### 1. Secret Manager 整合
- 敏感憑證不再存儲在代碼庫中
- 符合 GitHub 安全掃描要求
- 支援憑證輪換和版本管理

### 2. 環境隔離
- STG 和 PRD 使用不同的 SECRET_KEY
- 各環境獨立的 Google Analytics 追蹤 ID
- 適當的 NO_INDEX 設定

### 3. 權限管理
- Cloud Build 服務帳戶具有 Secret Manager 存取權限
- 最小權限原則

## 後續建議

### 1. 定期憑證輪換
建議每 90 天輪換一次 OAuth 憑證：
```bash
# 更新憑證
echo -n "NEW_CLIENT_SECRET" | gcloud secrets versions add google-oauth-client-secret --data-file=-
```

### 2. 監控和警報
- 設定 OAuth 登入失敗的監控警報
- 追蹤憑證過期時間
- 監控 Secret Manager 存取日誌

### 3. 文檔維護
- 更新部署文檔包含 Secret Manager 設定步驟
- 記錄憑證輪換流程
- 維護故障排除指南

## 修復時間軸
- **2024-12-19 15:30**: 識別問題 - STG 環境 OAuth 401 錯誤
- **2024-12-19 15:45**: 獲取真實 OAuth 憑證
- **2024-12-19 16:00**: 設定 Secret Manager
- **2024-12-19 16:15**: 更新 STG 和 PRD 環境變數
- **2024-12-19 16:30**: 測試確認修復成功
- **2024-12-19 16:45**: 更新 Cloud Build 配置使用 Secret Manager

## 結論
Google OAuth 登入問題已完全解決：
- ✅ STG 環境可正常進行 Google 登入
- ✅ PRD 環境已預先配置正確憑證
- ✅ 安全性大幅提升，符合最佳實踐
- ✅ CI/CD 流程支援自動化部署

用戶現在可以在 STG 環境正常測試 Google OAuth 登入功能。 