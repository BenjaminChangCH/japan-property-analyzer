# Google OAuth 重定向 URI 清理檢查清單

## 🎯 清理目標
從 11 個重定向 URI 清理到 7 個核心 URI，移除過時和多餘的配置。

## 🗑️ 需要刪除的 URI (4 個)

### ❌ URI 2
```
https://japan-property-analyzer-864942598341.asia-northeast1.run.app
```
**原因**: 舊的錯誤 STG URL，已被 URI 7 取代

### ❌ URI 8  
```
https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app
```
**原因**: 舊的錯誤 PRD URL，已被 URI 11 取代

### ❌ URI 9
```
https://www.benjamin-changch.com/oauth2callback
```
**原因**: 個人網站 URI，與此專案無關

### ❌ URI 10
```
https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app
```
**原因**: 與 URI 8 重複的錯誤 PRD URL

## ✅ 保留的核心 URI (7 個)

### 本機開發環境 (5 個)
- ✓ URI 1: `http://localhost:5000/auth/callback`
- ✓ URI 3: `http://localhost:8080/auth/callback`
- ✓ URI 4: `http://localhost:5001/auth/callback`
- ✓ URI 5: `http://127.0.0.1:5000/auth/callback`
- ✓ URI 6: `http://127.0.0.1:5001/auth/callback`

### 雲端環境 (2 個)
- ✓ URI 7: `https://japan-property-analyzer-2dal3iq3qa-an.a.run.app/auth/callback` (STG)
- ✓ URI 11: `https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app/auth/callback` (PRD)

## 🔧 清理步驟

1. **前往 Google Cloud Console**
   ```
   https://console.cloud.google.com/apis/credentials
   ```

2. **選擇專案**: `project-japan-462310`

3. **編輯 OAuth 2.0 用戶端 ID**

4. **刪除 4 個多餘的 URI** (URI 2, 8, 9, 10)

5. **確認保留 7 個核心 URI**

6. **儲存設定**

## 🧪 清理後測試

- [ ] 本機開發環境登入測試
- [ ] STG 環境登入測試  
- [ ] PRD 環境登入測試

## 💡 清理效益

- 🎯 **配置更清晰**: 移除混淆的舊 URL
- 🔒 **提升安全性**: 減少無用的授權端點
- 🧹 **易於維護**: 簡化配置管理
- 📋 **避免錯誤**: 防止未來的 URL 混淆

## ⚠️ 注意事項

- 清理不會影響現有功能
- 所有環境的 OAuth 登入仍然正常
- 建議在非高峰時間進行
- 清理後立即測試各環境

---

**清理狀態**: 🟡 待執行  
**預計時間**: 5-10 分鐘  
**風險等級**: 🟢 低風險 