# Google OAuth 2.0 設定指南

## 📋 概述
本指南將協助您設定 Google OAuth 2.0 認證，讓用戶能夠使用 Google 帳號登入日本不動產投資分析工具。

## 🔧 Google Cloud Console 設定

### 步驟 1: 創建 Google Cloud 專案
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 點擊「選取專案」→「新增專案」
3. 輸入專案名稱：`japan-property-analyzer`
4. 點擊「建立」

### 步驟 2: 啟用 Google+ API
1. 在左側選單選擇「API 和服務」→「程式庫」
2. 搜尋「Google+ API」
3. 點擊「啟用」

### 步驟 3: 設定 OAuth 同意畫面
1. 選擇「API 和服務」→「OAuth 同意畫面」
2. 選擇「外部」用戶類型
3. 填寫應用程式資訊：
   - **應用程式名稱**: 日本不動產投資分析工具
   - **用戶支援電子郵件**: 您的電子郵件
   - **應用程式標誌**: (可選) 上傳應用程式圖示
   - **應用程式首頁連結**: `https://your-domain.com`
   - **應用程式隱私權政策連結**: `https://your-domain.com/privacy`
   - **應用程式服務條款連結**: `https://your-domain.com/terms`

4. 在「範圍」頁面，新增以下範圍：
   - `openid`
   - `email`
   - `profile`

5. 在「測試使用者」頁面，新增您的測試帳號

### 步驟 4: 創建 OAuth 2.0 憑證
1. 選擇「API 和服務」→「憑證」
2. 點擊「建立憑證」→「OAuth 2.0 用戶端 ID」
3. 選擇應用程式類型：「網路應用程式」
4. 設定名稱：`Japan Property Analyzer Web Client`
5. 新增授權重新導向 URI：
   - 開發環境: `http://localhost:5000/auth/callback`
   - STG 環境: `https://japan-property-analyzer-864942598341.asia-northeast1.run.app/auth/callback`
   - 生產環境: `https://japan-property-analyzer-864942598341.asia-northeast1.run.app/auth/callback`

6. 點擊「建立」
7. 複製「用戶端 ID」和「用戶端密鑰」

## 🔐 環境變數設定

### 本地開發環境
1. 複製 `env.example` 為 `.env`
2. 填入 Google OAuth 憑證：

```bash
# Google OAuth 2.0 設定
GOOGLE_CLIENT_ID=your-client-id.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# Flask 應用程式密鑰
SECRET_KEY=your-generated-secret-key

# 資料庫設定
DATABASE_URL=sqlite:///app.db
```

### 生成 SECRET_KEY
使用以下命令生成安全的密鑰：
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 生產環境設定
在 Google Cloud Run 中設定環境變數：

```bash
gcloud run services update japan-property-analyzer \
  --set-env-vars="GOOGLE_CLIENT_ID=your-client-id.googleusercontent.com" \
  --set-env-vars="GOOGLE_CLIENT_SECRET=your-client-secret" \
  --set-env-vars="SECRET_KEY=your-generated-secret-key" \
  --region=asia-northeast1
```

## 🧪 測試設定

### 本地測試
1. 啟動開發伺服器：
```bash
python main.py
```

2. 訪問 `http://localhost:5000/auth/login`
3. 應該會重定向到 Google 登入頁面
4. 登入後應該會回到應用程式首頁

### 功能測試
- ✅ 登入流程正常
- ✅ 用戶資料正確儲存
- ✅ 會話管理正常
- ✅ 登出功能正常

## 🔒 安全性考量

### HTTPS 要求
- 生產環境必須使用 HTTPS
- Google OAuth 要求安全連線

### CSRF 保護
- 使用 `state` 參數防止 CSRF 攻擊
- 驗證回調中的 state 值

### 會話安全
- 使用強密鑰加密會話
- 設定適當的會話過期時間

## 🚨 常見問題

### 錯誤：redirect_uri_mismatch
**原因**: 回調 URL 不匹配
**解決**: 確認 Google Console 中的重定向 URI 與應用程式設定一致

### 錯誤：invalid_client
**原因**: 用戶端 ID 或密鑰錯誤
**解決**: 檢查環境變數中的 Google OAuth 憑證

### 錯誤：access_denied
**原因**: 用戶拒絕授權或應用程式未通過驗證
**解決**: 確認 OAuth 同意畫面設定正確

## 📝 開發注意事項

### 測試用戶限制
- 未發布的應用程式只能有 100 個測試用戶
- 需要在 OAuth 同意畫面中新增測試用戶

### 發布應用程式
- 完成開發後需要提交 Google 審核
- 審核通過後才能供所有用戶使用

### 監控和日誌
- 記錄認證相關的錯誤和異常
- 監控登入成功率和失敗原因

## 🔄 更新和維護

### 定期檢查
- 監控 Google OAuth API 的變更
- 更新相關依賴套件
- 檢查安全性最佳實踐

### 備份策略
- 備份 OAuth 憑證
- 記錄重要的設定參數 