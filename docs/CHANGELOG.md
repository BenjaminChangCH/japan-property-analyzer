# 📋 版本變更記錄

本文件記錄專案的所有重要變更和版本發布。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，
版本號遵循 [語義化版本](https://semver.org/lang/zh-TW/)。

## [未發布]

### 修復
- **重大修復**: STG 環境 OAuth invalid_client 錯誤
- **重大修復**: 本機開發環境 OAuth 重定向 URI 協議問題
- **重大修復**: 識別 PRD Google 登入失敗根本原因 - OAuth 重定向 URI 配置不完整
- 修復 cloudbuild-staging.yaml 使用假憑證的問題
- 修復本機開發環境 HTTPS/HTTP 協議衝突
- 完整分析 STG 和 PRD 環境配置差異，提供詳細修復指南
- 增強 OAuth 錯誤處理和授權碼驗證

### 新增
- STG 環境 SEO 控制：添加 noindex 防止搜尋引擎索引
- 動態 robots.txt 支援：根據環境變數自動生成
- GitHub Actions STG 部署工作流程
- Google Cloud Secret Manager 整合
- 環境感知的 OAuth 重定向 URI 配置
- 完整的 OAuth 錯誤處理機制
- STG 環境修復自動化腳本 (`scripts/fix_stg_oauth.sh`)

### 變更
- STG 環境 Cloud Run 配置：取消連線限制，開放公開存取
- 增強 HTML meta tags：支援 robots noindex 控制
- 優化部署配置：統一 ingress 和 execution environment 設定
- **安全性提升**: 移除所有硬編碼 OAuth 憑證
- **CI/CD 改進**: STG 環境使用 Secret Manager 管理敏感資訊
- 本機開發環境支援 HTTP 協議 (localhost:5001)
- 生產環境強制使用 HTTPS 協議

### 技術改進
- Cloud Build 服務帳戶 Secret Manager 權限配置
- Docker 基礎映像更新至 python:3.11-slim-bookworm
- 新增 .dockerignore 檔案優化建置效能
- 統一 STG 和 PRD 環境憑證管理策略

## [v1.3.0] - 2025-06-16

### 新增
- 完整的文字層級系統設計規範
- 統一的 CSS 變數系統（字體、間距、圓角、陰影）
- 專業的視覺層次結構
- 響應式文字大小調整
- 等寬字體數據顯示系統
- 開發完成檢查系統 (`/complete` 指令)
- 功能初始化系統 (`/init` 指令)
- 統一指令管理系統 (`scripts/cursor_commands.py`)
- 完整的開發流程自動化
- 統一快捷指令參考文檔 (`QUICK_REFERENCE.md`)
- 文檔歸檔系統 (`docs/guides/`, `docs/reports/`, `docs/archive/`)

### 變更
- **重大更新**: 完全重構 CSS 文字層級系統
- **建立設計系統規範**: 創建完整的設計系統文檔作為開發標準
- **強制性設計規範**: 更新 .cursorrules 強制要求遵循設計系統
- **文檔結構重整**: 重新整理專案文件結構，刪除重複文檔
- 統一所有標題、內文、標籤的字體大小和字重
- 優化表格和數據顯示的可讀性
- 改善按鈕、表單和卡片的視覺設計
- 增強工具提示和說明文字的專業度
- 新增設計系統相關的 Slash Commands
- 整合 CURSOR_QUICK_REFERENCE.md 和 USAGE_GUIDE.md 為統一參考文檔
- 更新檢查腳本以適應新的文檔結構

### 新增文件
- `QUICK_REFERENCE.md` - **統一快捷指令參考文檔**
- `docs/README.md` - 文檔目錄索引
- `docs/guides/DESIGN_SYSTEM.md` - **完整設計系統規範文檔**
- `docs/guides/TYPOGRAPHY_SYSTEM.md` - 文字層級系統設計規範
- `docs/guides/DESIGN_SYSTEM_QUICK_REF.md` - 設計系統快速參考
- `scripts/dev_complete_check.py` - 開發完成檢查核心腳本
- `scripts/feature_init.py` - 功能初始化核心腳本
- `scripts/cursor_commands.py` - 統一指令管理腳本

### 移除文件
- `CURSOR_QUICK_REFERENCE.md` - 已整合到 QUICK_REFERENCE.md
- `USAGE_GUIDE.md` - 已整合到 QUICK_REFERENCE.md
- 過時的完成報告文檔
- 重複的 OAuth 初始化報告

### 技術改進
- 建立了 6 個標題層級 (H1-H4) 和 4 個內文層級
- 定義了完整的間距系統 (XS 到 XXL)
- 統一了圓角和陰影系統
- 優化了字體堆疊和顏色應用
- 改善了響應式設計的文字適配
- 完善了文檔歸檔和索引系統

## [v1.1.0] - 2025-06-15

### 新增
- 完整的產品需求文檔 (PRD.md)
- 程式碼分析報告 (CODE_ANALYSIS.md)
- Cursor 快速參考指南 (CURSOR_QUICK_REFERENCE.md)
- 專案規則和開發規範 (.cursorrules)

### 變更
- 重構專案文檔結構
- 統一文檔格式和風格
- 清理重複和過時文檔

### 移除
- 重複的開發指南文檔
- 過時的部署工作流程文檔
- 冗餘的測試報告文檔

## [v1.0.0] - 2025-06-01

### 新增
- 基礎財務分析引擎
- 多種變現模式分析 (Airbnb、長租、店鋪)
- IRR 計算和現金流預測
- PDF 報告生成功能
- 響應式 Web 界面
- Google Cloud Run 部署配置
- CI/CD 自動化流程

### 技術架構
- Flask 後端框架
- HTML/CSS/JavaScript 前端
- Docker 容器化
- GitHub Actions CI/CD

---

## 版本號規則

### 語義化版本 (MAJOR.MINOR.PATCH)

- **MAJOR**: 不相容的 API 變更
- **MINOR**: 向下相容的功能新增
- **PATCH**: 向下相容的問題修正

### 版本標籤

- `[未發布]` - 尚未發布的變更
- `[vX.Y.Z]` - 已發布的版本
- 日期格式: YYYY-MM-DD

### 變更類型

- **新增** - 新功能
- **變更** - 現有功能的變更
- **棄用** - 即將移除的功能
- **移除** - 已移除的功能
- **修復** - 錯誤修復
- **安全性** - 安全性相關變更

---

**維護者**: Benjamin Chang  
**最後更新**: 2025-06-16 