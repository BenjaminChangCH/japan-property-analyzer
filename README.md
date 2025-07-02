# 🏢 Japan Property Analyzer

**專業的日本不動產投資分析平台**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](./version.py)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

> 為台灣投資者量身打造的日本不動產投資財務分析工具，支援多種投資策略和專業風險評估。

## ✨ 核心功能

- 🏠 **多元投資策略** - Airbnb、一般租賃、商業租賃
- 💰 **專業財務分析** - IRR、現金回報率、投資回收期
- 📊 **風險評估** - 槓桿比率、債務覆蓋率、健康度評級
- 📋 **專業報告** - 一鍵生成 PDF 投資分析報告
- 🔐 **安全登入** - Google OAuth 用戶認證
- 📱 **響應式設計** - 支援桌面和移動設備

## 🚀 快速開始

### 📋 系統需求
- Python 3.11+
- 現代瀏覽器 (Chrome, Firefox, Safari, Edge)

### ⚡ 5分鐘安裝
```bash
# 1. 下載專案
git clone https://github.com/BenjaminChangCH/japan-property-analyzer.git
cd japan-property-analyzer

# 2. 建立環境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 安裝套件
pip install -r requirements.txt

# 4. 設定環境
cp env.example .env

# 5. 啟動應用
python main.py
```

🌐 **開啟瀏覽器**: http://localhost:8080

## 📖 完整文檔

- 📚 [文檔中心](./docs/README.md) - 完整的專案文檔
- 🚀 [快速開始](./docs/guides/QUICKSTART.md) - 詳細安裝指南
- 📋 [產品規格](./docs/PRD.md) - 完整功能規格
- 🏗️ [系統架構](./docs/MODULAR_ARCHITECTURE_REPORT.md) - 技術架構說明

## 🎯 使用範例

### 基本投資分析
```python
# 範例：分析一個 5500萬円的 Airbnb 物件
投資參數 = {
    "物件價格": "5500萬円",
    "自備款比例": "20%", 
    "投資策略": "Airbnb短租",
    "入住率": "80%",
    "日租金": "18000円"
}

# 系統自動計算
結果 = {
    "現金回報率": "6.2%",
    "IRR": "8.5%", 
    "投資回收期": "12.3年",
    "風險等級": "中等"
}
```

## 🛠️ 專案結構

```
japan-property-analyzer/
├── 📄 main.py              # 主應用程式
├── 📄 auth.py              # 認證系統
├── 📄 models.py            # 資料模型
├── 📁 config/              # 配置模組
├── 📁 static/              # 前端資源
├── 📁 templates/           # 網頁模板
├── 📁 scripts/             # 工具腳本
├── 📁 tests/               # 測試程式
├── 📁 docs/                # 專案文檔
└── 📁 deployment/          # 部署配置
```

## 🌍 部署環境

- **🧪 STG 測試環境**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app
- **🚀 PRD 正式環境**: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app

## 🤝 參與貢獻

我們歡迎各種形式的貢獻！

1. 🍴 Fork 專案
2. 🌿 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 💾 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 📤 推送分支 (`git push origin feature/AmazingFeature`)
5. 🔀 開啟 Pull Request

## 📊 技術棧

- **後端**: Python 3.11, Flask 2.0+
- **前端**: HTML5, CSS3, JavaScript ES6+
- **資料庫**: SQLite (開發), PostgreSQL (生產)
- **認證**: Google OAuth 2.0
- **部署**: Google Cloud Run, Docker
- **CI/CD**: GitHub Actions

## 📞 聯絡與支援

- 🐛 **問題回報**: [GitHub Issues](https://github.com/BenjaminChangCH/japan-property-analyzer/issues)
- 💬 **功能建議**: [GitHub Discussions](https://github.com/BenjaminChangCH/japan-property-analyzer/discussions)
- 👨‍💻 **開發者**: Benjamin Chang
- 📧 **聯絡信箱**: [benjamin.chang.ch@gmail.com](mailto:benjamin.chang.ch@gmail.com)

## 📄 授權條款

本專案採用 [MIT 授權條款](./LICENSE)。

---

<div align="center">

**🏢 專為台灣投資者設計的日本不動產分析工具**

[開始使用](./docs/guides/QUICKSTART.md) • [查看文檔](./docs/README.md) • [報告問題](https://github.com/BenjaminChangCH/japan-property-analyzer/issues)

</div>

 