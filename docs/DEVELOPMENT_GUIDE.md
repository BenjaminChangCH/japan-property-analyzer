# 🔧 開發工作流程指南

## 📋 **每次開發的標準步驟**

### **🎯 開始前準備**

#### **1. 環境同步檢查**
```bash
# 檢查所有環境版本
./scripts/check_environments.sh

# 如不同步，執行環境同步
./scripts/sync_dev_environment.sh
```

#### **2. 確認當前狀態**
```bash
# 確保在 main 分支且是最新版本
git checkout main
git pull origin main
git status  # 應顯示 "working tree clean"
```

---

## 🚀 **功能開發流程**

### **步驟 1: 創建功能分支**
```bash
# 命名規則：feature/功能描述
git checkout -b feature/add-new-calculation

# 或針對問題修復
git checkout -b fix/calculation-error
git checkout -b hotfix/critical-security-fix
```

### **步驟 2: 進行開發**
```bash
# 1. 編輯代碼
# 2. 本機測試
python main.py  # 本機運行測試

# 3. 檢查代碼品質
python scripts/quality_checker.py

# 4. 提交變更
git add .
git commit -m "feat: 新增風險分析功能"
# 或
git commit -m "fix: 修正計算公式錯誤"
```

### **步驟 3: 推送並創建 PR**
```bash
# 推送分支
git push origin feature/add-new-calculation

# 到 GitHub 創建 Pull Request
# 目標分支: main
# 這會自動觸發 STG 部署
```

---

## 🧪 **測試與驗證流程**

### **STG 環境測試**
PR 創建後，系統會自動：
1. ✅ 部署到 STG 環境
2. ✅ 執行自動化測試
3. ✅ 生成測試報告

**您需要手動驗證：**
```bash
# STG 環境地址：
# https://japan-property-analyzer-stg-366005894157.asia-east1.run.app

# 測試檢查清單：
- [ ] 新功能正常運作
- [ ] 現有功能未被影響
- [ ] 計算結果正確
- [ ] 用戶界面正常
- [ ] 錯誤處理正確
```

### **測試文檔參考**
- 📄 **測試指南**: `docs/TEST_SUITE_OVERVIEW.md`
- 📄 **STG 測試報告**: `docs/STG_TEST_REPORT.md`

---

## ✅ **部署到生產環境**

### **合併 PR**
測試通過後：
1. 在 GitHub 上合併 PR
2. 系統自動部署到 PRD
3. 自動執行健康檢查

### **部署後驗證**
```bash
# PRD 環境地址：
# https://japan-property-analyzer-366005894157.asia-east1.run.app

# 快速檢查
curl https://japan-property-analyzer-366005894157.asia-east1.run.app/health
```

---

## 📚 **主要參考文檔**

### **🔥 必讀文檔（按優先順序）**

1. **📋 開發工作流程** (本文檔)
   - 每次開發必須遵循的步驟

2. **🚀 部署流程指南** - `docs/DEPLOYMENT_WORKFLOW.md`
   - 詳細的 CI/CD 流程說明
   - STG → PRD 部署檢查點
   - 緊急處理程序

3. **📊 版本控制指南** - `docs/VERSION_CONTROL_GUIDE.md`
   - Git 分支策略
   - 版本號管理
   - 提交訊息規範

4. **🧪 測試套件總覽** - `docs/TEST_SUITE_OVERVIEW.md`
   - 測試項目清單
   - 測試執行方法

### **📖 輔助文檔**

5. **🔀 Git Flow 指南** - `docs/GIT_FLOW_GUIDE.md`
   - Git 操作詳細說明

6. **📋 發佈檢查清單** - `docs/RELEASE_CHECKLIST.md`
   - 發佈前必須檢查的項目

7. **🏗️ 專案結構** - `docs/PROJECT_STRUCTURE.md`
   - 檔案組織結構說明

---

## 🚨 **常見問題處理**

### **❌ 開發遇到問題時**

#### **1. 代碼衝突**
```bash
# 拉取最新變更
git fetch origin
git rebase origin/main

# 解決衝突後
git add .
git rebase --continue
```

#### **2. STG 測試失敗**
```bash
# 檢查 STG 環境日誌
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=japan-property-analyzer-stg" --limit=50

# 修復問題後重新推送
git add .
git commit -m "fix: 修正 STG 測試問題"
git push origin feature/your-branch
```

#### **3. 緊急問題修復**
```bash
# 創建 hotfix 分支
git checkout main
git pull origin main
git checkout -b hotfix/critical-fix

# 修復 → 測試 → 部署
# 遵循相同流程但可加速審核
```

---

## ⚡ **快速命令參考**

### **日常開發**
```bash
# 開始新功能
git checkout main && git pull origin main
git checkout -b feature/new-feature

# 提交變更
git add . && git commit -m "feat: 功能描述"
git push origin feature/new-feature

# 檢查環境狀態
./scripts/check_environments.sh

# 代碼品質檢查
python scripts/quality_checker.py
```

### **問題排查**
```bash
# 查看版本資訊
python -c "from version import get_version_info; print(get_version_info())"

# 檢查應用程式健康狀態
curl https://japan-property-analyzer-366005894157.asia-east1.run.app/health

# 查看最近的提交
git log --oneline -5
```

---

## 📞 **需要幫助時**

1. **🔍 先查看相關文檔**
2. **📋 檢查 GitHub Issues**
3. **💬 查看 Git 提交歷史尋找類似問題**
4. **🔧 使用提供的自動化腳本**

---

## 🎯 **總結：簡化記憶版**

```
每次開發的四個步驟：

1️⃣ 準備：環境同步 + 創建分支
2️⃣ 開發：編碼 + 測試 + 提交
3️⃣ 驗證：推送 + PR + STG 測試  
4️⃣ 部署：合併 PR + PRD 驗證

參考順序：
📋 本指南 → 🚀 部署流程 → �� 版本控制 → 🧪 測試指南
``` 