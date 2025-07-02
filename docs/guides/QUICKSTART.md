# 🚀 快速開始指南

歡迎使用 Japan Property Analyzer！這個指南將幫助您在 5 分鐘內快速上手。

## 📋 系統需求

### 最低需求
- Python 3.11+
- 2GB RAM
- 1GB 硬碟空間
- 現代瀏覽器 (Chrome, Firefox, Safari, Edge)

### 推薦需求
- Python 3.11+
- 4GB RAM
- 2GB 硬碟空間
- Chrome 或 Firefox 最新版本

## ⚡ 快速安裝

### 1. 下載專案
```bash
git clone https://github.com/BenjaminChangCH/japan-property-analyzer.git
cd japan-property-analyzer
```

### 2. 建立虛擬環境
```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### 3. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 4. 設定環境變數
```bash
# 複製環境變數範本
cp env.example .env

# 編輯 .env 文件 (使用任意文字編輯器)
nano .env  # 或使用 vim、vscode 等
```

### 5. 啟動應用程式
```bash
python main.py
```

### 6. 開啟瀏覽器
在瀏覽器中開啟：http://localhost:8080

## 🎯 核心功能快速體驗

### 1. 基本財務分析
1. 在首頁點擊「開始分析」
2. 選擇投資策略（建議先試試 Airbnb 模式）
3. 輸入基本參數：
   - 物件價格：5500 萬円
   - 自備款比例：20%
   - 匯率：0.22
4. 點擊「計算投資報酬」

### 2. 查看分析報告
- 📊 **投資回報指標**：現金回報率、IRR、回收期
- 📈 **風險評估**：槓桿比率、債務覆蓋率
- 💰 **現金流分析**：年度預測、收支明細
- 📋 **投資建議**：系統自動生成的建議

### 3. 下載 PDF 報告
1. 滾動到頁面底部
2. 點擊「下載 PDF 報告」
3. 獲得專業格式的分析報告

## 🔧 進階設定

### Google OAuth 登入 (可選)
如果需要用戶登入功能：

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 Google OAuth API
4. 設定 OAuth 同意畫面
5. 建立 OAuth 2.0 用戶端 ID
6. 在 `.env` 文件中設定：
   ```env
   GOOGLE_CLIENT_ID=你的客戶端ID
   GOOGLE_CLIENT_SECRET=你的客戶端密鑰
   ```

### Google Analytics (可選)
如果需要網站分析：

1. 建立 Google Analytics 帳戶
2. 取得追蹤 ID
3. 在 `.env` 文件中設定：
   ```env
   GA_TRACKING_ID=你的追蹤ID
   ```

## 🛠️ 常見問題

### Q: 應用程式無法啟動
**A:** 檢查以下項目：
1. Python 版本是否為 3.11+
2. 虛擬環境是否已啟動
3. 相依套件是否已安裝
4. 端口 8080 是否被占用

### Q: 計算結果不準確
**A:** 請確認：
1. 輸入的數值格式正確
2. 匯率設定合理
3. 投資策略參數符合實際情況

### Q: 無法生成 PDF 報告
**A:** 可能原因：
1. 瀏覽器版本過舊
2. JavaScript 被停用
3. 網路連線問題

### Q: Google 登入無法使用
**A:** 檢查：
1. OAuth 設定是否正確
2. 回調 URL 是否設定正確
3. 環境變數是否已設定

## 📚 後續學習

完成快速體驗後，建議閱讀：

1. [📖 用戶手冊](./USER_GUIDE.md) - 詳細功能說明
2. [📋 PRD 文檔](../PRD.md) - 完整產品規格
3. [🏗️ 架構文檔](../MODULAR_ARCHITECTURE_REPORT.md) - 技術架構

## 🆘 獲得幫助

- 📖 [文檔中心](../README.md)
- 🐛 [問題回報](https://github.com/BenjaminChangCH/japan-property-analyzer/issues)
- 💬 [討論區](https://github.com/BenjaminChangCH/japan-property-analyzer/discussions)

---

🎉 **恭喜！** 您已經成功設定 Japan Property Analyzer。開始探索日本不動產投資的財務分析吧！ 