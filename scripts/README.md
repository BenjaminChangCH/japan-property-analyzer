# 🛠️ Scripts Directory

Japan Property Analyzer 工具腳本集合

## 📁 目錄結構

```
scripts/
├── development/          # 開發工具
├── maintenance/          # 維護工具
├── oauth/               # OAuth 相關工具
├── deployment/          # 部署腳本（預留）
└── README.md           # 本說明文檔
```

## 🚀 開發工具 (development/)

### `start_dev.sh`
- **功能**：啟動開發環境
- **使用**：`./scripts/development/start_dev.sh`

### `sync_dev_environment.sh`
- **功能**：同步開發環境配置
- **使用**：`./scripts/development/sync_dev_environment.sh`

### `dev_complete_check.py`
- **功能**：開發完成檢查，確保程式碼品質
- **使用**：`python scripts/development/dev_complete_check.py`

## 🔧 維護工具 (maintenance/)

### `backup_manager.py`
- **功能**：資料庫和配置檔案備份管理
- **使用**：`python scripts/maintenance/backup_manager.py`

### `quality_checker.py`
- **功能**：程式碼品質檢查
- **使用**：`python scripts/maintenance/quality_checker.py`

### `version_manager.py`
- **功能**：版本管理和發布準備
- **使用**：`python scripts/maintenance/version_manager.py`

## 🔐 OAuth 工具 (oauth/)

### `setup_oauth.py`
- **功能**：設定 Google OAuth 配置
- **使用**：`python scripts/oauth/setup_oauth.py`

### OAuth 修復腳本
- `fix_stg_oauth.sh` - 修復 STG 環境 OAuth
- `fix_prd_oauth.sh` - 修復 PRD 環境 OAuth
- `fix_custom_domain_oauth.sh` - 修復自定義域名 OAuth
- `clean_oauth_redirect_uris.sh` - 清理 OAuth redirect URIs

## 🚀 通用工具

### `cursor_commands.py`
- **功能**：Cursor IDE 快捷指令處理
- **使用**：`python scripts/cursor_commands.py [command]`

### `feature_init.py`
- **功能**：初始化新功能開發
- **使用**：`python scripts/feature_init.py [feature_name]`

### `check_environments.sh`
- **功能**：檢查多環境狀態
- **使用**：`./scripts/check_environments.sh`

### `clean_ports.sh`
- **功能**：清理被佔用的端口
- **使用**：`./scripts/clean_ports.sh [port]`

## 📋 使用指南

### 權限設定
```bash
# 為所有 shell 腳本添加執行權限
chmod +x scripts/**/*.sh
```

### 環境要求
- Python 3.11+
- 設置虛擬環境：`python -m venv .venv`
- 安裝依賴：`pip install -r requirements.txt`

### 最佳實踐
1. 執行腳本前先檢查當前工作目錄
2. 重要操作前建議先備份
3. 在測試環境先驗證腳本功能
4. 查看腳本內容了解具體操作

---
*最後更新：2025-07-02* 