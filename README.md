# 🏠 日本不動產投資分析工具

這是一個專業的日本不動產投資財務分析 Web 應用程式，旨在幫助投資者分析不同投資策略的財務回報。本應用程式基於 Flask (Python) 開發，並計劃未來擴展為 iOS/Android 應用程式。

## 🚀 快速開始

### 本地開發
```bash
# 克隆專案
git clone <repository-url>
cd Project\ Japan

# 創建虛擬環境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt

# 運行應用程式
python main.py
```

### 🎯 開發完成檢查系統

本專案配備了完整的開發完成檢查系統，確保每次開發完成後環境一致性：

```bash
# 開發完成檢查（推薦每次開發完成後使用）
python scripts/cursor_commands.py complete

# 初始化新功能開發
python scripts/cursor_commands.py init "功能名稱"

# 快速狀態檢查
python scripts/cursor_commands.py status

# 查看所有可用指令
python scripts/cursor_commands.py help
```

**詳細使用說明**: 參考 [USAGE_GUIDE.md](USAGE_GUIDE.md)

## 🌟 核心功能

### 已完成功能 (80%)
- ✅ **財務分析引擎**: 多種變現模式分析 (Airbnb、長租、店鋪)
- ✅ **IRR 計算**: 內部報酬率計算和現金流預測
- ✅ **PDF 報告生成**: 專業的分析報告輸出
- ✅ **響應式 UI**: 現代化的使用者界面

### 開發中功能
- 🟡 **用戶認證系統**: Google OAuth 登入 (計劃中)
- 🟡 **案件管理系統**: 投資案件收藏和管理 (計劃中)
- 🟡 **AI 對話助手**: 智能投資建議 (計劃中)

## 🏗️ 技術架構

- **後端**: Flask (Python 3.11+)
- **前端**: HTML/CSS/JavaScript
- **部署**: Google Cloud Run
- **CI/CD**: GitHub Actions
- **資料庫**: 計劃使用 Cloud SQL

## 🌐 部署環境

- **STG 環境**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app
- **PRD 環境**: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app

## 📊 專案進度

| 模組 | 狀態 | 完成度 | 備註 |
|------|------|--------|------|
| 財務分析引擎 | 🟢 已完成 | 80% | 核心功能完成 |
| 基礎架構 | 🟢 已完成 | 95% | 部署和 CI/CD 完成 |
| 用戶認證系統 | 🔴 未開始 | 0% | 等待開發 |
| 案件管理系統 | 🔴 未開始 | 0% | 等待開發 |
| AI 對話助手 | 🔴 未開始 | 0% | 等待開發 |

**詳細進度**: 參考 [docs/PRD.md](docs/PRD.md)

## 🛠️ 開發工具

### 簡化指令系統
本專案使用簡化指令系統提高開發效率：

```bash
# 功能開發
python scripts/cursor_commands.py init "新功能名稱"    # 初始化新功能
python scripts/cursor_commands.py complete           # 開發完成檢查

# 專案管理
python scripts/cursor_commands.py status            # 檢查專案狀態
python scripts/cursor_commands.py prd               # PRD 狀態統計
python scripts/cursor_commands.py clean             # 清理臨時文件

# 版本控制
python scripts/cursor_commands.py version           # 檢查版本信息
python scripts/cursor_commands.py changelog         # 檢查變更記錄
python scripts/cursor_commands.py release v1.3.0    # 準備版本發布
```

### 開發流程
1. **初始化**: 使用 `/init` 創建新功能分支和模板
2. **開發**: 實現功能邏輯和測試
3. **檢查**: 使用 `/complete` 進行完整檢查
4. **部署**: 推送到 STG 環境測試
5. **發布**: 合併到 main 分支部署到 PRD

## 📚 文檔

- [產品需求文檔 (PRD)](docs/PRD.md) - 完整的產品規劃和需求
- [程式碼分析報告](docs/CODE_ANALYSIS.md) - 技術架構和程式碼分析
- [使用指南](USAGE_GUIDE.md) - 開發完成檢查系統使用說明
- [快速參考](CURSOR_QUICK_REFERENCE.md) - Cursor 指令快速參考
- [版本記錄](docs/CHANGELOG.md) - 版本變更和發布記錄

## 🤝 貢獻指南

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/amazing-feature`)
3. 使用 `/complete` 檢查開發完成狀態
4. 提交變更 (`git commit -m 'feat: add amazing feature'`)
5. 推送到分支 (`git push origin feature/amazing-feature`)
6. 創建 Pull Request

## 📄 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 文件

## 📞 聯絡

Benjamin Chang - 專案維護者

---

**開發提示**: 建議每次開發完成後使用 `python scripts/cursor_commands.py complete` 進行完整檢查，確保程式碼品質和專案一致性。

## 專案進度管理

本專案的詳細功能需求、開發進度與狀態追蹤，請參閱 `docs/PRD.md` 文件。所有模組的完成度、版本資訊和未來規劃都將在該文件中維護。

## 技術棧

- **後端**: Python 3.11+, Flask
- **前端**: HTML, CSS, JavaScript
- **部署**: Google Cloud Platform (Cloud Run)

## 目錄結構

```
/
├── main.py                 # 主應用程式
├── config/                 # 配置模組
├── templates/              # HTML 模板
├── static/                 # 靜態資源
│   ├── css/
│   ├── js/
│   └── images/
├── tests/                  # 測試檔案
├── docs/                   # 文件 (含 PRD.md)
├── deployment/             # 部署相關
└── scripts/                # 工具腳本
```

---
*最新更新日期: 2024-07-29* 