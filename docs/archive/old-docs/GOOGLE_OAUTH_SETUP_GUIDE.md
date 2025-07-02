# Google OAuth 設定完整指南
**專案**: NIPPON PROPERTY ANALYTICS  
**日期**: 2025-07-02  
**狀態**: 🔧 需要立即設定  

## 🚨 緊急修復指南

### 當前問題
- **錯誤**: "The OAuth client was not found" (401: invalid_client)
- **原因**: Google Cloud Console 中缺少授權的 JavaScript 來源
- **影響**: 無法使用 Google 登入功能

### 🎯 立即解決方案

#### 步驟 1: 訪問 Google Cloud Console
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 確保登入正確的 Google 帳戶 (`benjamin.chang10@gmail.com`)
3. 選擇正確的專案

#### 步驟 2: 找到 OAuth 設定
1. 點擊左側選單 → **APIs & Services** → **Credentials**
2. 找到 OAuth 2.0 Client ID:
   ```
   Client ID: 864942598341-9mo8q9571hmbkj8eabhjcesqq44ddsul.apps.googleusercontent.com
   ```
3. 點擊該 Client ID 進入編輯頁面

#### 步驟 3: 添加授權的 JavaScript 來源
在 **Authorized JavaScript origins** 區域，添加以下 URI：

```
http://localhost:5001
http://localhost:5007
http://localhost:8080
http://localhost:3000
http://localhost:4000
http://localhost:5000
```

⚠️ **重要**: 每個 URI 都要單獨添加，不要遺漏 `http://` 前綴

#### 步驟 4: 保存設定
1. 點擊 **SAVE** 按鈕
2. 等待設定生效（通常需要 5-30 分鐘）

## 📋 詳細設定清單

### OAuth 2.0 Client ID 配置

#### 基本信息
- **應用程式類型**: Web application
- **名稱**: NIPPON PROPERTY ANALYTICS (或您偏好的名稱)

#### 授權的 JavaScript 來源 (必須)
```
http://localhost:5001    ← 主要開發端口
http://localhost:5007    ← 備用開發端口
http://localhost:8080    ← 生產端口
http://localhost:3000    ← React 開發端口 (如有)
http://localhost:4000    ← 備用端口
http://localhost:5000    ← 備用端口 (注意: macOS 系統佔用)
```

#### 授權的重定向 URI (可選)
對於純前端 JavaScript OAuth，通常不需要設定重定向 URI。
如果需要，可以添加：
```
http://localhost:5001/auth/callback
http://localhost:5007/auth/callback
```

### OAuth 同意畫面設定

#### 必要信息
- **應用程式名稱**: NIPPON PROPERTY ANALYTICS
- **用戶支援電子郵件**: benjamin.chang10@gmail.com
- **應用程式標誌**: (可選) 上傳專案標誌
- **應用程式首頁連結**: http://localhost:5001
- **隱私權政策連結**: (可選)
- **服務條款連結**: (可選)

#### 範圍 (Scopes)
基本範圍 (預設已包含)：
- `openid`
- `email`
- `profile`

## 🔧 本地開發環境設定

### 1. 端口管理
```bash
# 清理佔用的端口
./scripts/clean_ports.sh

# 啟動應用程式
PORT=5001 python main.py
```

### 2. 環境變數設定 (可選)
創建 `.env` 檔案：
```bash
GOOGLE_CLIENT_ID=864942598341-9mo8q9571hmbkj8eabhjcesqq44ddsul.apps.googleusercontent.com
FLASK_ENV=development
PORT=5001
```

### 3. HTML 配置檢查
確保 `templates/index.html` 中的設定正確：
```html
<meta name="google-client-id" content="864942598341-9mo8q9571hmbkj8eabhjcesqq44ddsul.apps.googleusercontent.com">
```

## 🧪 測試與驗證

### 測試步驟
1. **啟動應用程式**:
   ```bash
   PORT=5001 python main.py
   ```

2. **訪問應用程式**:
   - 開啟瀏覽器
   - 前往 `http://localhost:5001`

3. **測試登入功能**:
   - 點擊 "使用 Google 登入" 按鈕
   - 檢查是否出現 Google 登入彈窗
   - 完成登入流程

### 錯誤排除

#### 常見錯誤 1: origin_mismatch
```
錯誤訊息: "Error 403: redirect_uri_mismatch"
解決方案: 檢查 JavaScript 來源是否包含當前使用的 localhost 端口
```

#### 常見錯誤 2: invalid_client
```
錯誤訊息: "Error 401: invalid_client"
解決方案: 
1. 檢查 Client ID 是否正確
2. 確認 JavaScript 來源已正確設定
3. 等待 Google 設定生效 (5-30 分鐘)
```

#### 常見錯誤 3: popup_blocked
```
錯誤訊息: 登入彈窗被阻擋
解決方案: 
1. 允許瀏覽器彈窗
2. 檢查瀏覽器設定
3. 嘗試不同瀏覽器
```

## 🔒 安全性考量

### 開發環境
- 使用 `http://localhost` (開發環境例外)
- 不要在生產環境使用 localhost

### 生產環境
- 必須使用 HTTPS
- 設定正確的網域名稱
- 定期輪換 Client Secret (如有)

### Client ID 保護
- Client ID 可以公開 (前端使用)
- Client Secret 必須保密 (後端使用)
- 不要將憑證提交到版本控制

## 📞 支援與聯絡

### 如果仍有問題
1. **檢查 Google Cloud Console 狀態頁面**
2. **查看瀏覽器開發者工具的 Console**
3. **確認網路連接正常**
4. **嘗試無痕模式**

### 聯絡信息
- **開發者**: Benjamin Chang
- **專案**: NIPPON PROPERTY ANALYTICS
- **GitHub**: (如有)
- **電子郵件**: benjamin.chang10@gmail.com

## 📝 設定檢查清單

完成設定後，請確認以下項目：

- [ ] Google Cloud Console 中的 OAuth Client ID 已建立
- [ ] 授權的 JavaScript 來源包含 `http://localhost:5001`
- [ ] OAuth 同意畫面已設定
- [ ] HTML 模板中的 Client ID 正確
- [ ] 應用程式可以在 port 5001 正常啟動
- [ ] 瀏覽器可以訪問 `http://localhost:5001`
- [ ] Google 登入按鈕可以正常點擊
- [ ] 登入彈窗可以正常顯示
- [ ] 可以完成完整的登入流程

---

**最後更新**: 2025-07-02  
**狀態**: 等待 Google Cloud Console 設定生效  
**預估修復時間**: 5-30 分鐘 