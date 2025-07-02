# 🏯 Japan Property Analyzer

*Professional Investment Intelligence - 日本不動產投資專業分析平台*

[![Version](https://img.shields.io/badge/version-v1.3.0-blue)](version.py)
[![Python](https://img.shields.io/badge/python-3.11+-green)](requirements.txt)
[![Flask](https://img.shields.io/badge/flask-2.0+-orange)](requirements.txt)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)

## 🌟 專案概述

Japan Property Analyzer 是一個專業的日本不動產投資財務分析 Web 應用程式，幫助投資者進行精確的投資回報分析和風險評估。

### 核心特色
- 🧮 **專業財務分析**：IRR、NPV、現金流預測
- 📊 **多元變現模式**：Airbnb、長租、店鋪經營分析
- 📱 **響應式設計**：支援桌面和行動裝置
- 📄 **PDF 報告生成**：專業投資分析報告
- 🔐 **安全部署**：Google Cloud Platform 託管

## 🚀 快速開始

### 環境需求
- Python 3.11+
- Flask 2.0+
- Google Cloud SDK (部署用)

### 本地開發
```bash
# 1. 克隆專案
git clone <repository-url>
cd Project\ Japan

# 2. 設置虛擬環境
python -m venv .venv
source .venv/bin/activate

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 啟動應用程式
python main.py
```

訪問 `http://localhost:5001` 開始使用

## 🏗️ 專案架構

```
Japan Property Analyzer/
├── 📋 main.py              # 主應用程式入口
├── 🔐 auth.py              # 用戶認證模組
├── 📊 models.py            # 資料模型
├── 📁 config/              # 配置管理
├── 🎨 templates/           # HTML 模板
├── 📦 static/              # 靜態資源
├── 🧪 tests/               # 測試文件
├── 🛠️ scripts/             # 工具腳本
├── 📚 docs/                # 專案文檔
└── 🚀 deployment/          # 部署配置
```

## 🌐 部署環境

| 環境 | 網址 | 用途 |
|------|------|------|
| **STG** | [測試環境](https://japan-property-analyzer-864942598341.asia-northeast1.run.app) | 功能測試和驗證 |
| **PRD** | [生產環境](https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app) | 正式發布版本 |

## 🛠️ 開發工具

### 腳本工具
```bash
# 開發工具
./scripts/development/start_dev.sh        # 啟動開發環境
python scripts/development/dev_complete_check.py  # 開發完成檢查

# 維護工具
python scripts/maintenance/quality_checker.py     # 程式碼品質檢查
python scripts/maintenance/version_manager.py     # 版本管理

# OAuth 工具
python scripts/oauth/setup_oauth.py       # OAuth 設定
```

### CI/CD 流程
1. **開發** → `feature/` 分支開發
2. **測試** → 自動部署到 STG 環境
3. **審查** → Pull Request 代碼審查
4. **發布** → 合併到 `main` 分支部署到 PRD

詳細流程請參考 [CI/CD 文檔](docs/CI_CD_WORKFLOW.md)

## 📊 功能特色

### ✅ 已完成功能
- **財務分析引擎**：多變現模式 ROI 計算
- **風險評估系統**：投資風險等級分析
- **報表生成**：PDF 格式專業報告
- **響應式介面**：跨裝置使用體驗

### 🔄 規劃功能
- **用戶系統**：Google OAuth 登入
- **案件管理**：投資案件收藏追蹤
- **AI 助手**：智能投資建議

## 📚 文檔中心

| 文檔 | 說明 |
|------|------|
| [📋 PRD](docs/PRD.md) | 產品需求文檔 |
| [📝 CHANGELOG](docs/CHANGELOG.md) | 版本變更記錄 |
| [🎨 設計系統](docs/guides/DESIGN_SYSTEM.md) | UI/UX 設計規範 |
| [🔐 OAuth 設定](docs/guides/GOOGLE_OAUTH_SETUP.md) | 認證系統指南 |
| [🚀 部署流程](docs/CI_CD_WORKFLOW.md) | CI/CD 指南 |

更多文檔請參考 [docs/README.md](docs/README.md)

## 🤝 貢獻指南

1. **Fork** 專案到您的 GitHub 帳戶
2. **建立分支**: `git checkout -b feature/new-feature`
3. **提交變更**: `git commit -m 'feat: add new feature'`
4. **推送分支**: `git push origin feature/new-feature`
5. **建立 PR**: 提交 Pull Request 進行審查

### 提交規範
- `feat:` 新功能
- `fix:` 錯誤修復
- `docs:` 文檔更新
- `style:` 格式調整
- `refactor:` 程式碼重構
- `test:` 測試相關

## 📄 版本資訊

**當前版本**: v1.3.0  
**發布日期**: 2025-07-02  
**開發者**: Benjamin Chang

查看完整版本歷史請參考 [CHANGELOG.md](docs/CHANGELOG.md)

## 📞 技術支援

- **專案維護**: Benjamin Chang
- **問題回報**: [GitHub Issues](https://github.com/username/japan-property-analyzer/issues)
- **功能建議**: [GitHub Discussions](https://github.com/username/japan-property-analyzer/discussions)

## 📜 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件

---

<p align="center">
  <strong>🏯 Professional Investment Intelligence</strong><br>
  專業投資分析，智慧決策支援
</p>