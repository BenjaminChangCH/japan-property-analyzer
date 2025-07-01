# PRD 環境 Google 登入失敗診斷報告

## 📋 問題摘要

**發生時間**: 2025-06-16  
**問題**: PRD 環境 (https://www.benjamin-changch.com/) Google 登入功能失敗  
**狀態**: 🔍 已識別根本原因，待修復  

## 🔍 完整環境配置對比分析

### STG vs PRD 環境變數對比

| 配置項目 | STG 環境 | PRD 環境 | 差異分析 |
|----------|----------|----------|----------|
| **服務名稱** | japan-property-analyzer | japan-property-analyzer-prod | ✅ 正常 |
| **映像版本** | gcr.io/.../analyzer:1.3.0.-stg | gcr.io/.../analyzer:latest | ✅ 都是最新版本 |
| **ENVIRONMENT** | staging | production | ✅ 正常 |
| **GA_TRACKING_ID** | G-59XMZ0SZ0G | G-94SVDFL5YN | ✅ 不同追蹤 ID |
| **NO_INDEX** | true | false | ✅ 正常 |
| **SECRET_KEY** | [不同的密鑰] | [不同的密鑰] | ✅ 不同密鑰 |
| **GOOGLE_CLIENT_ID** | [相同的客戶端ID] | [相同的客戶端ID] | ⚠️ **相同** |
| **GOOGLE_CLIENT_SECRET** | [相同的客戶端密鑰] | [相同的客戶端密鑰] | ⚠️ **相同** |
| **APP_VERSION** | 1.3.0 | (未設定) | ⚠️ PRD 缺少版本號 |

## 🚨 發現的關鍵問題

### 1. OAuth 憑證完全相同
**問題**: STG 和 PRD 環境使用相同的 OAuth Client ID 和 Client Secret

**影響**: 這本身不是問題，但需要確保 OAuth 客戶端配置支援所有環境的重定向 URI

### 2. 重定向 URI 配置問題 ⭐ **根本原因**
**問題**: Google Cloud Console 中的 OAuth 客戶端可能缺少 PRD 環境的重定向 URI

**需要檢查的重定向 URI**:
- ✅ `http://localhost:5001/oauth2callback` (本機開發)
- ✅ `https://japan-property-analyzer-864942598341.asia-northeast1.run.app/oauth2callback` (STG)
- ❓ `https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app/oauth2callback` (PRD 原始)
- ❓ `https://www.benjamin-changch.com/oauth2callback` (PRD 自定義域名)

### 3. JavaScript 來源配置問題
**問題**: OAuth 客戶端可能缺少 PRD 環境的 JavaScript 來源

**需要檢查的 JavaScript 來源**:
- ✅ `http://localhost:5001` (本機開發)
- ✅ `https://japan-property-analyzer-864942598341.asia-northeast1.run.app` (STG)
- ❓ `https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app` (PRD 原始)
- ❓ `https://www.benjamin-changch.com` (PRD 自定義域名)

## 🛠️ 修復步驟

### 步驟 1: 檢查 Google Cloud Console OAuth 設定
1. 前往: https://console.cloud.google.com/apis/credentials?project=project-japan-462310
2. 找到 OAuth 客戶端 ID (名稱: 日本不動產投資分析工具)
3. 點擊編輯

### 步驟 2: 確認重定向 URI 設定
確保以下 URI 都已添加到「已授權的重新導向 URI」:
```
http://localhost:5001/oauth2callback
https://japan-property-analyzer-864942598341.asia-northeast1.run.app/oauth2callback
https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app/oauth2callback
https://www.benjamin-changch.com/oauth2callback
```

### 步驟 3: 確認 JavaScript 來源設定
確保以下來源都已添加到「已授權的 JavaScript 來源」:
```
http://localhost:5001
https://japan-property-analyzer-864942598341.asia-northeast1.run.app
https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app
https://www.benjamin-changch.com
```

### 步驟 4: 測試修復
1. 儲存 OAuth 客戶端設定
2. 等待 5-10 分鐘讓設定生效
3. 測試 PRD 環境登入功能

## 📊 環境狀態總結

| 環境 | OAuth 狀態 | 網址 | 備註 |
|------|------------|------|------|
| **本機** | ✅ 正常 | http://localhost:5001 | HTTP 協議 |
| **STG** | ✅ 正常 | https://japan-property-analyzer-864942598341.asia-northeast1.run.app | HTTPS 協議 |
| **PRD** | ❌ 失敗 | https://www.benjamin-changch.com | 需要修復重定向 URI |

## 🔧 自動化修復腳本

已創建 `scripts/fix_oauth_redirect_uris.sh` 腳本，提供詳細的修復步驟指南。

## 📝 後續行動

1. **立即**: 手動檢查並修復 Google Cloud Console OAuth 設定
2. **測試**: 驗證 PRD 環境 Google 登入功能
3. **文檔**: 更新修復結果到此報告
4. **部署**: 如需要，重新部署 PRD 環境

## 🎯 預期結果

修復完成後，所有三個環境的 Google OAuth 登入功能都應該正常工作：
- 本機開發環境 (HTTP)
- STG 測試環境 (HTTPS)
- PRD 生產環境 (HTTPS，自定義域名) 