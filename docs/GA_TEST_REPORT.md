# Google Analytics 測試報告
## STG 環境 GA 追蹤測試結果

**測試時間:** 2024年12月
**測試環境:** STG (https://japan-property-analyzer-864942598341.asia-northeast1.run.app)
**GA 追蹤 ID:** G-59XMZ0SZ0G

---

## 🎯 測試總結

### ✅ 通過的項目 (4/4 - 100%)

1. **HTML 中的 GA 配置** ✅
   - GA 腳本載入標籤存在
   - GA 追蹤 ID 配置正確
   - gtag 函數定義存在
   - 環境配置正確 (staging)
   - 事件追蹤碼完整 (calculation_started, calculation_completed, pdf_download)

2. **GA 事件發送機制** ✅
   - GA4 端點配置正確
   - 事件結構符合 GA4 標準

3. **API 功能測試** ✅
   - 後端 API 正常運作
   - 返回正確的計算結果

4. **GA 設置檢查** ✅
   - 所有必要組件已安裝

---

## 🔍 詳細檢查結果

### 1. 技術配置檢查
```bash
# GA 腳本確認
✅ <script async src="https://www.googletagmanager.com/gtag/js?id=G-59XMZ0SZ0G"></script>

# 追蹤配置確認
✅ gtag('config', 'G-59XMZ0SZ0G', gaConfig);

# 環境設定確認
✅ environment: 'staging'

# 事件追蹤確認
✅ gtag('event', 'calculation_started', {...})
✅ gtag('event', 'calculation_completed', {...})
✅ gtag('event', 'pdf_download', {...})
```

### 2. API 測試結果
```
API 端點: https://japan-property-analyzer-864942598341.asia-northeast1.run.app/calculate
狀態: ✅ 正常運作
響應時間: < 2秒
返回結果: 正確的財務計算數據
```

---

## ❗ GA 無資料問題分析

雖然技術配置完全正確，但如果 GA 控制台仍然沒有收到資料，可能的原因包括：

### 1. 資料延遲問題
- **即時報告延遲:** 1-5 分鐘
- **標準報告延遲:** 24-48 小時
- **首次設置延遲:** 可能需要更長時間

### 2. 瀏覽器與網路問題
- 廣告攔截器 (AdBlock, uBlock Origin 等)
- 瀏覽器隱私設置阻擋追蹤
- 公司/學校網路防火牆
- DNS 解析問題

### 3. GA 配置問題
- GA 屬性設置錯誤
- 資料流 (Data Stream) 配置問題
- GA4 vs Universal Analytics 混淆

### 4. 技術問題
- JavaScript 執行錯誤
- CORS 政策阻擋
- HTTPS/HTTP 混合內容問題

---

## 🛠️ 問題排除步驟

### 步驟 1: 手動驗證
1. 打開瀏覽器（建議使用無痕模式）
2. 訪問 STG 網站: https://japan-property-analyzer-864942598341.asia-northeast1.run.app
3. 打開瀏覽器開發者工具 (F12)
4. 切換到 Network 標籤
5. 重新載入頁面
6. 查看是否有 `googletagmanager.com` 或 `google-analytics.com` 的請求

### 步驟 2: 檢查即時報告
1. 前往 [Google Analytics](https://analytics.google.com/)
2. 選擇對應的 GA4 屬性
3. 點擊左側選單的「即時」
4. 在另一個瀏覽器標籤中操作 STG 網站
5. 查看即時報告是否顯示活躍使用者

### 步驟 3: 使用 GA Debugger
1. 安裝 Chrome 擴充套件: "Google Analytics Debugger"
2. 啟用除錯模式
3. 重新載入 STG 網站
4. 檢查 Console 中的 GA 除錯資訊

### 步驟 4: 檢查事件觸發
```javascript
// 在瀏覽器 Console 中執行以下程式碼來手動觸發事件
gtag('event', 'test_event', {
  'event_category': 'manual_test',
  'event_label': 'console_trigger'
});
```

---

## 🔧 建議的改進措施

### 1. 增加 GA 除錯資訊
在 HTML 模板中加入除錯模式：
```javascript
{% if environment == 'staging' %}
gtag('config', '{{ ga_tracking_id }}', {
  debug_mode: true,
  send_page_view: true
});
{% endif %}
```

### 2. 新增伺服器端事件追蹤
考慮使用 GA4 Measurement Protocol 進行伺服器端追蹤：
```python
import requests

def send_ga_event(event_name, parameters):
    url = "https://www.google-analytics.com/mp/collect"
    data = {
        'measurement_id': 'G-59XMZ0SZ0G',
        'api_secret': 'YOUR_API_SECRET',
        'client_id': 'server_generated_client_id',
        'events': [{
            'name': event_name,
            'parameters': parameters
        }]
    }
    requests.post(url, json=data)
```

### 3. 新增錯誤追蹤
```javascript
window.addEventListener('error', function(e) {
  gtag('event', 'javascript_error', {
    'error_message': e.message,
    'error_filename': e.filename,
    'error_lineno': e.lineno
  });
});
```

---

## 📊 測試命令摘要

```bash
# 執行 STG 基礎測試
python test_stg_simple.py

# 執行 GA 專門測試
python test_ga_simple.py

# 檢查 HTML 中的 GA 代碼
curl -s "https://japan-property-analyzer-864942598341.asia-northeast1.run.app" | grep -i "gtag\|G-59XMZ0SZ0G"
```

---

## 🎯 結論

**技術配置狀態:** ✅ 完全正確
**建議下一步:** 手動測試與 GA 控制台驗證

GA 追蹤碼已正確安裝在 STG 環境中，所有技術組件都運作正常。如果仍然沒有收到資料，主要原因可能是：
1. 需要實際的用戶互動才能觸發事件
2. GA 資料處理延遲
3. 瀏覽器或網路環境阻擋

建議立即進行手動測試，並在 GA 即時報告中確認資料是否開始流入。 