# 📚 Japan Property Analyzer - 文檔中心

歡迎來到日本不動產投資分析工具的文檔中心。這裡包含了完整的專案文檔、開發指南和技術資料。

## 🎯 快速導航

### 核心文檔
- [📋 PRD - 產品需求文檔](./PRD.md) - 完整的產品需求和功能規格
- [🚀 快速開始指南](./guides/QUICKSTART.md) - 5分鐘快速上手
- [📖 用戶手冊](./guides/USER_GUIDE.md) - 詳細使用說明

### 開發文檔
- [🏗️ 架構設計](./MODULAR_ARCHITECTURE_REPORT.md) - 系統架構和模組設計
- [🔐 認證系統](./GOOGLE_LOGIN_IMPLEMENTATION.md) - Google OAuth 登入實作
- [🚀 CI/CD 流程](./CI_CD_WORKFLOW.md) - 自動化部署流程
- [📝 變更日誌](./CHANGELOG.md) - 版本更新記錄

### 專案管理
- [📊 專案管理](./PROJECT_MANAGEMENT.md) - 開發流程和里程碑
- [🗺️ 產品路線圖](./PROPERTY_MANAGEMENT_ROADMAP.md) - 功能發展規劃

### 歷史文檔
- [📁 歸檔文件](./archive/) - 過往的完成報告和修復記錄

## 🔧 開發環境

### 系統需求
- Python 3.11+
- Flask 2.0+
- Node.js 16+ (用於前端工具)

### 快速啟動
```bash
# 1. 複製專案
git clone https://github.com/BenjaminChangCH/japan-property-analyzer.git
cd japan-property-analyzer

# 2. 設置環境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. 設置環境變數
cp env.example .env
# 編輯 .env 文件設置必要的變數

# 4. 啟動應用
python main.py
```

### 部署環境
- **STG**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app
- **PRD**: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app

## 📋 功能概覽

### 核心功能
- ✅ **財務分析計算** - 專業的不動產投資財務模型
- ✅ **多種投資策略** - 支援 Airbnb、一般租賃、商業租賃
- ✅ **風險評估** - 槓桿風險和投資健康度分析
- ✅ **報告生成** - PDF 格式的專業分析報告

### 用戶功能
- ✅ **Google OAuth 登入** - 安全的用戶認證
- ✅ **響應式設計** - 支援桌面和移動設備
- ✅ **多語言介面** - 繁體中文和英文

## 🤝 貢獻指南

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📞 支援與聯絡

- **問題回報**: [GitHub Issues](https://github.com/BenjaminChangCH/japan-property-analyzer/issues)
- **功能建議**: [GitHub Discussions](https://github.com/BenjaminChangCH/japan-property-analyzer/discussions)
- **開發者**: Benjamin Chang

## 📄 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](../LICENSE) 文件。

---

💡 **提示**: 如果您是第一次使用，建議從[快速開始指南](./guides/QUICKSTART.md)開始。 