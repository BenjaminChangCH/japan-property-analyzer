# 🚀 開發完成檢查系統使用指南

## 概覽

這個系統為您提供了一個完整的開發完成檢查流程，確保每次開發完成後所有環境和文檔都保持一致，並為下一次開發做好準備。

## 🎯 核心指令

### `/complete` - 開發完成檢查
```bash
python scripts/cursor_commands.py complete
```

**功能**：
- 🔍 檢查程式碼品質和語法
- 🧪 驗證測試狀態
- 📚 確認文檔完整性
- 📝 檢查 Git 狀態和同步
- 🚀 驗證部署準備狀態
- 📊 更新 PRD 進度
- 🔄 準備下一次開發環境
- 📋 生成完成報告

### `/init` - 功能初始化
```bash
python scripts/cursor_commands.py init "功能名稱"
```

**功能**：
- 📊 檢查 PRD 狀態和需求定義
- 🌿 創建 feature branch
- 📁 準備目錄結構和檔案模板

## 📊 輔助指令

### 快速狀態檢查
```bash
python scripts/cursor_commands.py status
```

### PRD 狀態統計
```bash
python scripts/cursor_commands.py prd
```

### 清理臨時文件
```bash
python scripts/cursor_commands.py clean
```

### 顯示幫助
```bash
python scripts/cursor_commands.py help
```

## 🔄 標準開發流程

### 1. 開始新功能開發
```bash
# 初始化新功能
python scripts/cursor_commands.py init "Google OAuth 登入"

# 開始開發...
# (編寫程式碼、測試等)
```

### 2. 開發完成檢查
```bash
# 執行完整檢查
python scripts/cursor_commands.py complete
```

### 3. 根據檢查結果採取行動

#### ✅ 如果檢查全部通過
```bash
# 推送到遠端分支
git push origin feature/your-feature-name

# 部署到 STG 環境測試
# (通過 GitHub Actions 自動觸發)
```

#### ⚠️ 如果有警告項目
- 可選擇處理警告項目
- 或直接推送到 STG 環境測試

#### ❌ 如果有失敗項目
- 必須先解決失敗項目
- 重新執行 `/complete` 檢查

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

## 🌐 部署環境

### STG 環境
- **URL**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app
- **觸發**: 推送到 feature branch
- **用途**: 功能測試和審查

### PRD 環境
- **URL**: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app
- **觸發**: 合併到 main branch
- **用途**: 生產環境

## 💡 最佳實踐

### 每次開發完成後
1. 執行 `/complete` 檢查
2. 查看生成的完成報告
3. 處理必要的失敗項目
4. 考慮處理警告項目
5. 推送代碼到遠端分支
6. 部署到 STG 環境測試

### 定期維護
- 使用 `/clean` 清理臨時文件
- 使用 `/prd` 檢查專案進度
- 定期更新依賴套件

### 問題排查
- 查看詳細的完成報告
- 檢查 Git 狀態和分支同步
- 確認所有必要文檔存在
- 驗證部署配置文件

---

**提示**: 這個系統設計為自動化您的開發完成檢查流程，確保程式碼品質和專案一致性。建議每次開發完成後都使用 `/complete` 指令進行檢查。 