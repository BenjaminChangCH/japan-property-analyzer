# 測試套件總覽
## 日本不動產投資分析工具測試框架

**最後更新:** 2024年12月  
**環境:** STG & PRD

---

## 📁 檔案結構重新整理

### 🔄 檔案重新命名對照表

| 舊檔名 | 新檔名 | 用途 |
|--------|--------|------|
| `test_stg_simple.py` | `test_stg_api.py` | STG 環境 API 測試 |
| `test_stg_automation.py` | `test_stg_browser.py` | STG 環境瀏覽器測試 |
| `test_ga_simple.py` | `test_stg_ga.py` | STG 環境 GA 測試 |
| - | `test_prd_api.py` | PRD 環境 API 測試 |
| - | `test_prd_ga.py` | PRD 環境 GA 測試 |

---

## 🧪 測試檔案詳細說明

### STG 環境測試

#### 1. `test_stg_api.py` - STG API 測試
- **用途:** 測試 STG 環境的基本 API 功能
- **測試項目:**
  - 首頁載入檢查
  - Airbnb 模式 API
  - 長租模式 API  
  - 法人購買模式 API
  - 錯誤處理機制
- **執行命令:** `python test_stg_api.py`

#### 2. `test_stg_browser.py` - STG 瀏覽器測試
- **用途:** 使用 Selenium 進行完整的瀏覽器自動化測試
- **測試項目:**
  - 頁面載入和 GA 追蹤
  - 表單元素檢查
  - 表單互動測試
  - 計算功能驗證
  - PDF 下載功能
- **執行命令:** `python test_stg_browser.py`
- **需求:** Chrome 瀏覽器和 ChromeDriver

#### 3. `test_stg_ga.py` - STG GA 測試
- **用途:** 專門測試 STG 環境的 Google Analytics 配置
- **測試項目:**
  - HTML 中的 GA 追蹤碼檢查
  - GA 事件發送機制
  - API 調用測試
  - 實時數據檢查說明
- **執行命令:** `python test_stg_ga.py`

### PRD 環境測試

#### 4. `test_prd_api.py` - PRD API 測試
- **用途:** 測試 PRD 環境的基本 API 功能
- **特點:** 與 STG 測試類似，但針對生產環境
- **執行命令:** `python test_prd_api.py`
- **注意:** 這是生產環境測試，請謹慎使用

#### 5. `test_prd_ga.py` - PRD GA 測試
- **用途:** 測試 PRD 環境的 Google Analytics 配置
- **特點:** 
  - 包含 STG vs PRD 環境比較
  - 生產環境特定的檢查
  - 除錯模式驗證
- **執行命令:** `python test_prd_ga.py`
- **注意:** 生產環境 GA 事件會被實際記錄

---

## 🛠️ 輔助工具

### 1. `config.py` - 環境配置管理
- **用途:** 統一管理不同環境的配置參數
- **功能:**
  - 環境配置定義
  - GA 追蹤 ID 管理
  - 環境對比功能
- **執行命令:** `python config.py`

### 2. `setup_prd_ga.py` - PRD GA 設定助手
- **用途:** 協助設定 PRD 環境的獨立 GA 追蹤 ID
- **功能:**
  - 互動式設定介面
  - 自動更新相關檔案
  - 部署步驟指引
- **執行命令:** `python setup_prd_ga.py`

### 3. `test-requirements.txt` - 測試依賴
- **用途:** 定義測試所需的 Python 套件
- **包含:** Selenium, requests, webdriver-manager

---

## 🌍 環境配置對照

| 環境 | URL | GA 追蹤 ID | 環境標識 | 除錯模式 |
|------|-----|------------|----------|----------|
| **DEV** | `http://localhost:5000` | 未設定 | development | 啟用 |
| **STG** | `https://japan-property-analyzer-864942598341.asia-northeast1.run.app` | G-59XMZ0SZ0G | staging | 啟用 |
| **PRD** | `https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app` | G-59XMZ0SZ0G* | production | 關閉 |

*\* 建議設定獨立的 PRD GA 追蹤 ID*

---

## 🚀 快速測試指令

### 全環境基本測試
```bash
# STG 環境基本測試
python test_stg_api.py

# PRD 環境基本測試  
python test_prd_api.py
```

### GA 追蹤測試
```bash
# STG 環境 GA 測試
python test_stg_ga.py

# PRD 環境 GA 測試
python test_prd_ga.py
```

### 完整瀏覽器測試
```bash
# 安裝測試依賴
pip install -r test-requirements.txt

# STG 瀏覽器測試
python test_stg_browser.py
```

### 環境管理
```bash
# 查看環境配置
python config.py

# 設定 PRD GA 追蹤
python setup_prd_ga.py
```

---

## 📊 測試報告

### 自動生成的報告檔案
- `STG_TEST_REPORT.md` - STG 環境測試報告
- `GA_TEST_REPORT.md` - GA 追蹤測試報告

### 測試成功率目標
- **API 測試:** ≥ 100% (5/5)
- **GA 測試:** ≥ 100% (4/4)
- **瀏覽器測試:** ≥ 80% (由於 UI 變動可能影響)

---

## ⚠️  重要注意事項

### STG 環境
- ✅ 可以自由測試
- ✅ 資料不會影響生產
- ✅ 適合開發和驗證

### PRD 環境  
- 🚨 **謹慎操作**
- 🚨 所有 GA 事件會被實際記錄
- 🚨 建議在非高峰時段測試
- 🚨 測試前確認目的和影響

---

## 🔧 故障排除

### 常見問題

1. **Chrome 驅動問題**
   ```bash
   # 重新安裝 webdriver-manager
   pip uninstall webdriver-manager
   pip install webdriver-manager
   ```

2. **網路連線問題**
   - 檢查 VPN 設定
   - 確認防火牆設定
   - 驗證 DNS 解析

3. **GA 資料未出現**
   - 檢查廣告攔截器設定
   - 驗證 GA 追蹤 ID 正確性
   - 等待資料處理延遲（最多 48 小時）

### 聯絡支援
- 技術問題：檢查錯誤日誌
- GA 問題：參考 `GA_TEST_REPORT.md`
- 環境問題：使用 `config.py` 驗證設定

---

## 📈 未來改進計劃

1. **測試自動化**
   - GitHub Actions 整合
   - 定期健康檢查
   - 自動測試報告

2. **效能監控**
   - 回應時間測試
   - 負載測試
   - 可用性監控

3. **安全性測試**
   - 輸入驗證測試
   - XSS 防護驗證
   - CSRF 保護檢查 