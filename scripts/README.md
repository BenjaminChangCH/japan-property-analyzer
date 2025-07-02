# 🛠️ Scripts Directory

本目錄包含專案的各種工具腳本，按功能分類組織。

## 📁 目錄結構

```
scripts/
├── development/     # 開發工具
├── deployment/      # 部署腳本  
├── maintenance/     # 維護工具
├── oauth/          # OAuth 相關工具
└── README.md       # 本說明文件
```

## 🔧 開發工具 (development/)

### 環境管理
- `start_dev.sh` - 快速啟動開發環境
- `check_environments.sh` - 檢查開發環境狀態
- `sync_dev_environment.sh` - 同步開發環境設定

### 開發輔助
- `cursor_commands.py` - Cursor 編輯器快捷指令
- `dev_complete_check.py` - 開發完成度檢查工具
- `feature_init.py` - 新功能初始化腳本
- `version_manager.py` - 版本管理工具

**使用範例:**
```bash
# 啟動開發環境
./scripts/development/start_dev.sh

# 檢查開發完成度
python scripts/development/dev_complete_check.py

# 初始化新功能
python scripts/development/feature_init.py --feature "用戶認證"
```

## 🚀 部署腳本 (deployment/)

*目前為空，預留給未來的部署自動化腳本*

## 🔧 維護工具 (maintenance/)

### 系統維護
- `clean_ports.sh` - 清理被占用的端口
- `backup_manager.py` - 資料備份管理工具
- `quality_checker.py` - 程式碼品質檢查工具

**使用範例:**
```bash
# 清理端口 5001
./scripts/maintenance/clean_ports.sh 5001

# 程式碼品質檢查
python scripts/maintenance/quality_checker.py

# 建立備份
python scripts/maintenance/backup_manager.py --create
```

## 🔐 OAuth 工具 (oauth/)

*OAuth 相關的設定和修復工具*

## 📋 使用說明

### 權限設定
在 Unix/Linux 系統上，首次使用前需要設定執行權限：

```bash
# 設定所有 shell 腳本的執行權限
find scripts/ -name "*.sh" -exec chmod +x {} \;
```

### 環境需求
- Python 3.11+
- Bash (Unix/Linux/macOS)
- PowerShell (Windows)

### 安全注意事項
1. 🔒 不要在版本控制中提交包含敏感資訊的腳本
2. 🛡️ OAuth 相關腳本包含敏感設定，請謹慎使用
3. 📝 執行前請先閱讀腳本內容，了解其功能

## 🆘 故障排除

### 常見問題

**Q: 腳本沒有執行權限**
```bash
chmod +x scripts/path/to/script.sh
```

**Q: Python 腳本找不到模組**
```bash
# 確保在專案根目錄執行，並啟動虛擬環境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows
```

**Q: 環境變數未設定**
```bash
# 確保 .env 文件存在且正確設定
cp env.example .env
# 編輯 .env 文件設定必要變數
```

## 🤝 貢獻新腳本

當添加新腳本時：

1. 將腳本放入適當的分類目錄
2. 添加腳本說明和使用範例到本文件
3. 確保腳本包含適當的錯誤處理
4. 在腳本頂部添加用途說明註釋

---

📝 **注意**: 所有腳本都應該在專案根目錄下執行，以確保路徑正確。 