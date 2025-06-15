# 🚀 日本不動產投資分析工具 - 開發快捷指令參考

## 📋 專案簡介
日本不動產投資分析工具 - 專業的財務分析 Web 應用程式
- **技術棧**：Flask + HTML/CSS/JavaScript
- **部署**：Google Cloud Platform (Cloud Run)
- **開發助手**：Cursor AI + 簡化指令系統
- **版本**：v1.2.0

## ⌨️ Cursor AI 核心快捷鍵

| 快捷鍵 | 功能 | 使用場景 |
|--------|------|----------|
| `Ctrl/Cmd + K` | 開啟對話 | 問題諮詢、功能開發 |
| `Ctrl/Cmd + L` | 選擇程式碼並詢問 | 程式碼審查、優化 |
| `Ctrl/Cmd + I` | 內聯編輯 | 直接修改程式碼 |

## 🎯 簡化調用格式 (Slash Commands)

### 🔧 開發相關指令
```bash
/fix                   # 修復程式碼錯誤或 bug
/refactor              # 重構程式碼，提高可讀性和效能
/test                  # 建立或執行測試案例
/deploy-stg            # 部署到 STG 測試環境
/deploy-prd            # 部署到 PRD 生產環境
/optimize              # 效能優化和程式碼改進
/security              # 安全性檢查和漏洞修復
/lint                  # 程式碼風格檢查和修正
```

### ⚡ 功能開發指令
```bash
/init [功能名稱]        # 一鍵初始化新功能開發環境
/feature [功能名稱]     # 開發新功能
/api [API名稱]         # 建立或修改 API 端點
/ui [頁面名稱]         # 建立或修改使用者介面
/db [操作類型]         # 資料庫相關操作
/auth                  # 用戶認證系統相關功能
/ai                    # AI 對話助手相關功能
```

### 🎨 設計系統指令
```bash
/design-check          # 檢查當前頁面是否符合設計系統規範
/design-update         # 更新設計系統規範文檔
/component [組件名稱]   # 創建符合設計系統的新組件
/style-audit           # 審查 CSS 是否使用了硬編碼值
/responsive-test       # 測試響應式設計在不同裝置上的效果
```

### 📚 文件管理指令
```bash
/prd                   # 更新或檢查 PRD 進度
/docs [文件類型]       # 建立或更新文件
/changelog             # 更新版本變更記錄
/readme                # 更新 README 文件
/analysis              # 程式碼分析和技術債務檢查
```

### 🎯 專案管理指令
```bash
/complete              # 開發完成檢查，確保環境一致性
/status                # 檢查專案整體狀態和進度
/milestone             # 檢查或更新開發里程碑
/review                # 程式碼審查和品質檢查
/backup                # 備份重要檔案和配置
/clean                 # 清理暫存檔案和無用程式碼
```

### 🎓 學習支援指令
```bash
/explain [概念]        # 解釋技術概念或程式碼邏輯
/best-practice [主題]  # 提供最佳實踐建議
/tutorial [技術]       # 提供學習教程和範例
/troubleshoot          # 問題診斷和解決方案
```

## 🔄 標準開發流程

### 1. 初始化階段 (`/init [功能名稱]`)
```bash
python scripts/cursor_commands.py init "Google OAuth 登入功能"
```
- 📊 檢查 PRD 狀態和需求定義
- 🌿 創建 feature branch (feature/功能名稱)
- 📁 準備目錄結構和檔案模板
- 🗄️ 設計資料庫結構 (如需要)
- 📝 定義 API 規格
- 🧪 創建測試檔案模板
- 📚 準備技術文件模板
- 🔄 更新 PRD 狀態為進行中

### 2. 開發階段 (`/feature [功能名稱]`)
- 實現核心功能邏輯
- 建立 API 端點
- 開發前端界面
- 整合現有系統

### 3. 測試階段 (`/test`)
- 單元測試
- 整合測試
- 功能測試

### 4. 完成檢查階段 (`/complete`)
```bash
python scripts/cursor_commands.py complete
```
- 🔍 檢查程式碼品質和語法
- 🧪 驗證測試狀態
- 📚 確認文檔完整性
- 📝 檢查 Git 狀態和同步
- 🚀 驗證部署準備狀態
- 📊 更新 PRD 進度
- 🔄 準備下一次開發環境
- 📋 生成完成報告

### 5. 部署階段 (`/deploy-stg`)
- 推送到 feature branch
- 自動部署到 STG 環境
- STG 環境測試

### 6. 發布階段 (`/deploy-prd`)
- 創建 Pull Request
- 代碼審查
- 合併到 main branch
- 自動部署到 PRD 環境

## 🌐 部署環境

### STG 環境
- **URL**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app
- **觸發**: 推送到 feature branch
- **用途**: 功能測試和審查

### PRD 環境
- **URL**: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app
- **觸發**: 合併到 main branch
- **用途**: 生產環境

## 📊 PRD 狀態標記系統

- 🔴 **未開始 (0%)**: 功能尚未開始開發
- 🟡 **進行中 (X%)**: 功能正在開發中，X 為完成百分比
- 🟢 **已完成 (100%)**: 功能已完成並通過測試
- 🔵 **已部署**: 功能已部署到生產環境
- ⚠️ **需修復**: 功能存在問題需要修復
- 📋 **待測試**: 功能開發完成，等待測試

## 💡 實用提示詞模板

### 🔍 程式碼審查
```
你是資深 Python 開發者，請審查這段程式碼的品質、安全性和效能，並提供改進建議
```

### 🐛 錯誤修復
```
我的程式出現錯誤：[貼上錯誤訊息]
請幫我分析原因並提供修復方案
```

### ⚡ 功能開發
```
你是 Flask 專家，請幫我實現 [具體功能]
要求：遵循現有程式碼風格，添加中文註釋，考慮錯誤處理
```

### 💰 財務計算專用
```
你是財務計算專家，請檢查這個 [IRR/NPV/現金流] 計算邏輯是否正確
並解釋計算公式和步驟
```

### 🎨 前端優化
```
你是前端 UX 專家，請優化這個表單的用戶體驗
要求：添加即時驗證、錯誤提示、響應式設計
```

## 🚨 緊急問題解決

### 應用程式無法啟動
```
我的 Flask 應用無法啟動，錯誤訊息：[貼上完整錯誤]
請快速診斷問題並提供解決方案
```

### 部署失敗
```
Google Cloud Run 部署失敗，錯誤：[貼上錯誤]
請提供解決方案和部署最佳實踐
```

### 計算結果異常
```
財務計算結果看起來不對，輸入參數：[貼上參數]
請檢查計算邏輯並修正問題
```

## 💡 指令組合使用範例

### 完整新功能開發
```bash
/init Google OAuth 登入功能
/feature Google OAuth 登入功能
/test
/complete
/deploy-stg
```

### 修復問題並部署
```bash
/fix 計算函數的精度問題
/test
/complete
/deploy-stg
```

### 重構和優化
```bash
/refactor main.py 的 calculate 函數
/optimize 資料庫查詢效能
/test
/complete
/review
```

### 版本發布流程
```bash
/complete
/changelog
/release v1.3.0
/deploy-prd
```

## 🎯 立即可以嘗試

### 第一次使用建議
1. **程式碼審查**：選擇 `main.py` 中的 `calculate` 函數 → `Ctrl/Cmd + L` → 「請審查這個函數並提供優化建議」
2. **功能開發**：`Ctrl/Cmd + K` → 「我想添加淨現值(NPV)計算功能，請提供實現方案」
3. **開發完成檢查**：`python scripts/cursor_commands.py complete`

## 📋 檢查項目說明

### ✅ 必須通過項目
- **Python 語法檢查**: 確保沒有語法錯誤
- **Git 狀態檢查**: 確保代碼已提交
- **必要文檔存在**: README.md, PRD.md, .cursorrules
- **部署配置**: requirements.txt, Dockerfile

### ⚠️ 警告項目（建議處理）
- **測試文件**: 建議添加單元測試和整合測試
- **函數長度**: 建議重構過長的函數（>100行）
- **文檔完整性**: 功能相關文檔
- **環境配置**: .env.example 文件
- **依賴更新**: 過時的套件

### 📊 自動執行項目
- **PRD 進度更新**: 自動記錄開發完成狀態
- **完成報告生成**: 詳細的檢查結果報告
- **臨時文件清理**: 清理 .pyc, __pycache__ 等
- **環境檢查**: 虛擬環境和依賴狀態

## 📄 生成的文件

### 完成報告
- **位置**: `docs/completion_report_YYYY-MM-DD_HH-MM-SS.md`
- **內容**: 詳細的檢查結果、建議和下一步操作

### PRD 進度更新
- **位置**: `docs/PRD.md`
- **內容**: 自動添加開發完成記錄和狀態更新

---

**記住**：Cursor AI + 簡化指令系統是您的開發夥伴，善用它們能大幅提升開發效率！🚀 