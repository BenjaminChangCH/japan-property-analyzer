# 自定義網域 Google OAuth 修復報告

## 🚨 問題描述

**發生時間**: 2025-07-01  
**環境**: PRD 生產環境（自定義網域）  
**網域**: https://www.benjamin-changch.com  
**問題**: Google OAuth 登入失敗  
**錯誤**: `redirect_uri_mismatch` (錯誤代碼 400)  

### 錯誤詳情
- 用戶嘗試登入時出現「已封鎖存取權：這個應用程式的要求無效」
- Google 顯示錯誤代碼 400: redirect_uri_mismatch
- 用戶帳號：benjamin.chang10@gmail.com

## 🔍 問題診斷

### 根本原因
Google Cloud Console 中的 OAuth 2.0 用戶端設定缺少自定義網域的重定向 URI。

### 環境狀態檢查
| 環境 | URL | 狀態 | OAuth 重定向 URI |
|------|-----|------|-----------------|
| 自定義網域 | https://www.benjamin-changch.com | ✅ 正常運行 | ❌ 缺少 |
| STG 測試 | https://japan-property-analyzer-2dal3iq3qa-an.a.run.app | ✅ 正常運行 | ✅ 已設定 |
| PRD 生產 | https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app | ✅ 正常運行 | ✅ 已設定 |

### OAuth 配置分析
從用戶提供的截圖可以看到，Google Cloud Console 中目前有 11 個重定向 URI，但缺少關鍵的自定義網域 URI：

**缺少的 URI**:
- `https://www.benjamin-changch.com/auth/callback`

## 🔧 修復方案

### 立即修復步驟

1. **前往 Google Cloud Console**
   ```
   https://console.cloud.google.com/apis/credentials?project=project-japan-462310
   ```

2. **編輯 OAuth 2.0 用戶端 ID**
   - Client ID: `864942598341-9mo8q9571hmbkj8eabhjcesgq44ddsul.apps.googleusercontent.com`
   - 名稱: 日本不動產投資分析工具

3. **添加自定義網域重定向 URI**
   在「已授權的重新導向 URI」中添加：
   ```
   https://www.benjamin-changch.com/auth/callback
   ```

4. **確認完整的核心重定向 URI 清單**
   ```
   ✅ http://localhost:5000/auth/callback (本機開發)
   ✅ http://localhost:5001/auth/callback (本機開發備用)
   ✅ https://japan-property-analyzer-2dal3iq3qa-an.a.run.app/auth/callback (STG)
   ✅ https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app/auth/callback (PRD)
   ✅ https://www.benjamin-changch.com/auth/callback (自定義網域) ⭐ 新增
   ```

5. **清理建議（可選）**
   可以刪除以下過時的 URI：
   ```
   ❌ https://japan-property-analyzer-864942598341.asia-northeast1.run.app (舊 STG)
   ❌ https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app (舊 PRD)
   ❌ https://www.benjamin-changch.com/oauth2callback (錯誤路徑)
   ```

6. **儲存設定**
   - 點擊「儲存」按鈕
   - 等待 5-10 分鐘讓設定生效

### 驗證步驟

1. **等待設定生效** (5-10 分鐘)
2. **測試登入功能**
   - 前往：https://www.benjamin-changch.com
   - 點擊「使用 Google 登入」
   - 確認能正常重定向到 Google 登入頁面
   - 完成登入後確認能正常返回應用程式

## 📊 技術分析

### 網域配置
- ✅ **自定義網域正常運行**: https://www.benjamin-changch.com 回應 HTTP 200
- ✅ **SSL 憑證有效**: 使用 HTTPS 協議
- ✅ **應用程式正常載入**: 可以看到完整的登入介面

### OAuth 流程分析
1. **用戶點擊登入** → 重定向到 `/auth/login`
2. **應用程式處理** → 重定向到 Google OAuth
3. **Google 驗證** → 檢查 redirect_uri 是否在允許清單中
4. **❌ 失敗點**: `https://www.benjamin-changch.com/auth/callback` 不在允許清單中

### 環境對比
| 配置項目 | STG 環境 | PRD 環境 (原始) | PRD 環境 (自定義網域) |
|----------|----------|----------------|-------------------|
| **基礎 URL** | japan-property-analyzer-2dal3iq3qa-an.a.run.app | japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app | www.benjamin-changch.com |
| **OAuth 狀態** | ✅ 正常 | ✅ 正常 | ❌ 失敗 |
| **重定向 URI** | ✅ 已設定 | ✅ 已設定 | ❌ 缺少 |

## 🎯 修復完成後的預期結果

- ✅ 自定義網域 Google 登入功能正常
- ✅ 所有環境的 OAuth 功能都正常運作
- ✅ 用戶可以在 https://www.benjamin-changch.com 正常登入
- ✅ 統一的用戶體驗

## 📝 後續建議

### 1. OAuth 配置優化
建議清理過時的重定向 URI，保持配置簡潔：
- 保留 5 個核心 URI
- 刪除 6 個過時 URI
- 總數從 11 個減少到 5 個

### 2. 監控和測試
- 定期測試所有環境的 OAuth 功能
- 監控登入錯誤率
- 設置自動化測試

### 3. 文檔更新
- 更新 OAuth 設定文檔
- 記錄所有有效的重定向 URI
- 建立變更管理流程

## 🔧 自動化腳本

已創建修復腳本：`scripts/fix_custom_domain_oauth.sh`

執行方式：
```bash
./scripts/fix_custom_domain_oauth.sh
```

## ⚠️ 重要提醒

1. **必須手動操作**: 重定向 URI 配置必須在 Google Cloud Console 中手動添加
2. **生效時間**: 設定變更需要 5-10 分鐘生效
3. **快取問題**: 如果仍有問題，請清除瀏覽器快取
4. **測試確認**: 修復後請在不同瀏覽器中測試

## 📞 支援資訊

如果修復後仍有問題，請提供：
- 錯誤訊息截圖
- 瀏覽器開發者工具的 Network 標籤
- 確認是否已在 Google Console 中添加了正確的 URI

---

**修復狀態**: 🟡 等待用戶在 Google Cloud Console 中添加重定向 URI  
**預期完成時間**: 立即（用戶操作後 5-10 分鐘生效） 