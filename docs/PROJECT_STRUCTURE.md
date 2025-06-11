# 專案檔案結構說明

## 📁 整理後的檔案結構

## 🛠️ 開發工具使用

### 版本管理
```bash
python scripts/version_manager.py
```

### 環境檢查
```bash
bash scripts/check_environments.sh
```

### 程式碼品質檢查
```bash
python scripts/quality_checker.py
```

### 備份管理
```bash
python scripts/backup_manager.py
```

```
Project Japan/
├── 📄 main.py                    # 主要應用程式 (含版本 API)
├── 📄 version.py                 # 版本號管理檔案
├── 📄 .gitignore                 # Git 忽略檔案
├── 📄 env.example               # 環境變數範例
├── 
├── 📁 config/                   # 配置相關
│   ├── 📄 __init__.py
│   ├── 📄 config.py             # 環境配置管理
│   └── 📄 setup_prd_ga.py       # PRD GA 設定工具
├── 
├── 📁 deployment/               # 部署相關
│   ├── 📄 Dockerfile           # Docker 建置檔案 (支援版本號)
│   ├── 📄 cloudbuild-staging.yaml    # STG 版本化部署配置
│   ├── 📄 cloudbuild-production.yaml # PRD 版本化部署配置
│   ├── 📄 requirements.txt      # Python 依賴
│   ├── 📄 requirements-dev.txt  # 開發依賴
│   └── 📄 test-requirements.txt # 測試依賴
├── 
├── 📁 docs/                     # 文檔資料
│   ├── 📄 CHANGELOG.md          # 變更日誌
│   ├── 📄 DEPLOYMENT.md         # 部署說明
│   ├── 📄 GA_TEST_REPORT.md     # GA 測試報告
│   ├── 📄 STG_TEST_REPORT.md    # STG 測試報告
│   ├── 📄 TEST_SUITE_OVERVIEW.md # 測試套件概覽
│   ├── 📄 GIT_FLOW_GUIDE.md     # Git Flow 指引
│   ├── 📄 VERSION_CONTROL_GUIDE.md # 版本號控制指引
│   └── 📄 PROJECT_STRUCTURE.md  # 專案結構說明 (本檔案)
├── 
├── 📁 scripts/                  # 腳本工具
│   ├── 📄 sync_dev_environment.sh  # 開發環境同步腳本
│   ├── 📄 version_manager.py       # 版本管理工具
│   ├── 📄 backup_manager.py        # 備份管理工具
│   ├── 📄 check_environments.sh    # 環境檢查腳本
│   └── 📄 quality_checker.py       # 程式碼品質檢查工具
├── 
├── 📁 templates/                # 網頁模板
│   └── 📄 index.html           # 主頁面模板
├── 
├── 📁 tests/                    # 測試套件
│   ├── 📄 __init__.py
│   ├── 📁 stg/                 # STG 環境測試
│   │   ├── 📄 __init__.py
│   │   ├── 📄 test_stg_api.py    # STG API 測試
│   │   ├── 📄 test_stg_browser.py # STG 瀏覽器測試
│   │   └── 📄 test_stg_ga.py     # STG GA 測試
│   ├── 📁 prd/                 # PRD 環境測試
│   │   ├── 📄 __init__.py
│   │   ├── 📄 test_prd_api.py    # PRD API 測試
│   │   └── 📄 test_prd_ga.py     # PRD GA 測試
│   └── 📁 shared/              # 共用測試工具
│       ├── 📄 __init__.py
│       ├── 📄 test_ga_tracking.py      # GA 追蹤測試
│       └── 📄 verify_prd_deployment.py # 部署驗證
└── 
└── 📁 .git/                    # Git 版本控制 (隱藏)
└── 📁 .venv/                   # 虛擬環境 (隱藏)
```

## 🎯 檔案分類說明

### 📄 根目錄核心檔案
* **main.py**: 主要 Flask 應用程式，含版本 API 端點 (`/version`)
* **version.py**: 版本號定義和管理，遵循 Semantic Versioning

### 📁 config/ - 配置管理
* **config.py**: 統一的環境配置管理
* **setup_prd_ga.py**: PRD 環境 GA 設定互動工具

### 📁 deployment/ - 部署配置
* **Dockerfile**: Docker 映像建置，支援版本號和建置編號
* **cloudbuild-*.yaml**: Google Cloud Build 配置，整合版本號管理
* **requirements*.txt**: Python 依賴管理

### 📁 docs/ - 文檔資料
* **技術文檔**: 測試報告、部署說明
* **開發指引**: Git Flow、版本控制指引
* **專案文檔**: 變更日誌、結構說明

### 📁 scripts/ - 開發工具
* **sync_dev_environment.sh**: 開發環境同步腳本
* **version_manager.py**: 版本號管理和發佈工具
* **backup_manager.py**: 備份管理工具
* **check_environments.sh**: 環境檢查腳本
* **quality_checker.py**: 程式碼品質檢查工具

### 📁 tests/ - 測試套件
* **stg/**: STG 環境專用測試
* **prd/**: PRD 環境專用測試  
* **shared/**: 跨環境共用測試工具

### 📁 templates/ - 前端模板
* **index.html**: 主應用程式 HTML 模板

## 🔧 使用方式

### 運行測試
```bash
# STG 環境測試
python tests/stg/test_stg_api.py
python tests/stg/test_stg_ga.py

# PRD 環境測試
python tests/prd/test_prd_api.py
python tests/prd/test_prd_ga.py

# 共用工具
python tests/shared/verify_prd_deployment.py
```



### 版本號管理
```bash
# 查看版本狀態
python scripts/version_manager.py status

# 發佈新版本
python scripts/version_manager.py release patch "修復描述"
python scripts/version_manager.py release minor "新功能描述"
python scripts/version_manager.py release major "重大更新描述"

# 查看版本資訊
python version.py
```

### 配置管理
```bash
# 設定 PRD GA 追蹤
python config/setup_prd_ga.py

# 查看配置設定
python -c "from config.config import *; print('STG:', STG_CONFIG); print('PRD:', PRD_CONFIG)"
```

## 📋 檔案整理優點

1. **清晰分類**: 按功能分類檔案，易於維護
2. **環境隔離**: STG/PRD 測試完全分離
3. **模組化**: 使用 Python 模組結構
4. **標準化**: 遵循 Python 專案最佳實踐
5. **版本控制**: 完整的版本號管理系統
6. **自動化**: Git Flow 和版本發佈自動化
7. **易於擴展**: 新增功能時結構清晰

## 🛡️ Git Flow 整合

整理後的結構完全支援標準 Git Flow：
* **標準化分支管理** 確保代碼品質
* **CI/CD** 自動部署流程

## 🔢 版本號控制整合

新增的版本號控制系統：
* **scripts/version_manager.py** 自動化版本管理
* **version.py** 標準化版本定義
* **CI/CD 版本化** 每次部署都有明確版本號
* **版本 API** 可查詢應用程式版本資訊

## 📝 維護注意事項

1. **新增測試**: 按環境分類放置對應資料夾
2. **更新文檔**: 在 docs/ 目錄維護相關文檔
3. **配置變更**: 統一在 config/ 目錄管理
4. **部署設定**: 在 deployment/ 目錄更新相關檔案
5. **版本發佈**: 使用 version_manager.py 工具標準化發佈流程
6. **Git Flow**: 遵循標準 Git Flow 開發流程

## 🚀 開發流程整合

完整的企業級開發流程：

```
1. 需求分析
   ↓
2. 創建 Feature Branch
   ↓
3. 開發實作
   ↓
4. 測試驗證 (tests/)
   ↓
5. 提交到 Feature Branch
   ↓
6. 創建 Pull Request
   ↓
7. 代碼審查
   ↓
8. 合併到 Main
   ↓
9. 發佈版本 (version_manager.py)
   ↓
10. 自動化部署 (CI/CD + 版本號)
    ↓
11. 生產環境驗證
```

這個結構讓專案更專業化，便於團隊協作和維護，同時具備企業級的版本控制和部署能力。 