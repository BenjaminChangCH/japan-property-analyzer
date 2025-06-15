# OAuth 重定向 URI 修復報告

## 問題描述

### 原始錯誤
```
錯誤 400：redirect_uri_mismatch
這個應用程式不符合 Google 的 OAuth 2.0 政策規定，因此您無法登入。
要求詳情： redirect_uri=https://japan-property-analyzer-2dal3iq3qa-an.a.run.app/auth/callback
```

### 根本原因
1. **Cloud Run URL 變更**：最新的 Cloud Build 部署產生了新的 Cloud Run URL
   - 舊 URL：`https://japan-property-analyzer-864942598341.asia-northeast1.run.app`
   - 新 URL：`https://japan-property-analyzer-2dal3iq3qa-an.a.run.app`

2. **Cloud Build 權限問題**：Cloud Build 服務帳戶缺少 Secret Manager 訪問權限
   - 錯誤：`PERMISSION_DENIED: Permission 'secretmanager.versions.access' denied`

3. **變數語法錯誤**：Cloud Build YAML 中的變數引用語法錯誤
   - 錯誤：`invalid value for 'build.substitutions': key in the template "GOOGLE_CLIENT_ID" is not a valid built-in substitution`

## 修復步驟

### 1. 修復 Cloud Build 配置
- **修正變數語法**：將 `$GOOGLE_CLIENT_ID` 改為 `$$GOOGLE_CLIENT_ID`
- **添加憑證驗證**：確保 OAuth 憑證不為空
- **文件**：`deployment/cloudbuild-staging.yaml` 和 `deployment/cloudbuild-production.yaml`

### 2. 修復 Secret Manager 權限
```bash
gcloud projects add-iam-policy-binding project-japan-462310 \
  --member="serviceAccount:864942598341-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 3. 更新 Google Cloud Console OAuth 配置
**需要手動執行**：
1. 前往：https://console.cloud.google.com/apis/credentials?project=project-japan-462310
2. 編輯 OAuth 2.0 用戶端 ID：`864942598341-9mo8q9571hmbkj8eabhjcesgq44ddsul.apps.googleusercontent.com`
3. 在「授權重新導向 URI」中添加：
   ```
   https://japan-property-analyzer-2dal3iq3qa-an.a.run.app/auth/callback
   ```

## 修復結果

### Build 狀態
- ✅ **最新 Build**：`b58c04ae-3403-4e15-9b9d-e7c3e1050c90` - SUCCESS
- ✅ **Secret Manager 權限**：已修復
- ✅ **OAuth 憑證**：正確從 Secret Manager 獲取

### 當前環境狀態
- **STG URL**：https://japan-property-analyzer-2dal3iq3qa-an.a.run.app
- **OAuth 憑證**：已正確設置環境變數
- **待完成**：Google Cloud Console 重定向 URI 配置

## 立即行動項目

### 🚨 用戶需要立即執行
1. **更新 Google Cloud Console OAuth 配置**
   - 添加新的重定向 URI：`https://japan-property-analyzer-2dal3iq3qa-an.a.run.app/auth/callback`
   - 保留現有的 URI

2. **測試 OAuth 登入功能**
   - 訪問：https://japan-property-analyzer-2dal3iq3qa-an.a.run.app
   - 測試 Google OAuth 登入

## 預防措施

### 1. Cloud Run URL 穩定性
- **問題**：Cloud Run URL 可能會因為重新部署而改變
- **解決方案**：考慮使用自定義域名或 Cloud Run 服務的穩定 URL

### 2. 自動化重定向 URI 管理
- **建議**：未來可考慮使用 Google Cloud API 自動管理重定向 URI
- **文檔**：記錄所有有效的重定向 URI

### 3. 監控和警報
- **建議**：設置 OAuth 錯誤監控
- **工具**：Cloud Monitoring 和 Error Reporting

## 技術改進

### 1. Cloud Build 優化
- ✅ 添加憑證驗證邏輯
- ✅ 改進錯誤處理
- ✅ 修復變數語法

### 2. 安全性增強
- ✅ 使用 Secret Manager 管理敏感資訊
- ✅ 適當的 IAM 權限設置
- ✅ 環境變數保護

## 總結

OAuth 重定向 URI 問題已基本修復，主要原因是 Cloud Run URL 變更導致的重定向 URI 不匹配。通過修復 Cloud Build 配置、Secret Manager 權限和更新 Google Cloud Console OAuth 配置，問題將完全解決。

**下一步**：用戶完成 Google Cloud Console 配置後，OAuth 登入功能將完全恢復正常。 