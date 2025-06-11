# Git Flow 開發流程指引

## 🔄 Git Flow 變化說明

### ⚠️ 重要變化：從直接推送到分支保護

#### **之前的流程（簡單直推）:**
```bash
git add .
git commit -m "更新功能"
git push origin main  # ✅ 直接成功
```

#### **現在的流程（受保護的 main 分支）:**
```bash
git add .
git commit -m "更新功能"
git push origin main  # ❌ 被拒絕！
# error: failed to push some refs
# hint: Updates were rejected because the remote contains work
```

## 🛡️ 為什麼需要這個變化？

### 安全性保護機制

1. **代碼審查**: 防止未經審查的代碼進入生產環境
2. **品質控制**: 確保所有變更都經過測試
3. **CI/CD 控制**: 只有審查過的代碼才會觸發自動部署
4. **團隊協作**: 標準化的開發流程

### GitHub 分支保護規則

您的 repository 已啟用以下保護：
- ✅ **Require pull request reviews**: 需要 PR 審查
- ✅ **Require status checks**: 需要通過狀態檢查
- ✅ **Require branches to be up to date**: 需要與 main 同步
- ✅ **Restrict pushes**: 限制直接推送到 main

## 📝 標準 Git Flow 流程

### 🚀 快速開始

#### 1. 創建功能分支
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

#### 2. 開發並提交
```bash
git add .
git commit -m "feat: 新增功能描述"
git push origin feature/your-feature-name
```

#### 3. 檢查狀態
```bash
git status
git log --oneline -5
```

### 💡 分支命名規範

推薦的分支命名格式：
```bash
feature/add-payment-feature
feature/fix-calculation-bug  
feature/update-ga-tracking
```

### 🔄 完整開發流程

1. **創建功能分支**
```bash
git checkout -b feature/add-tax-calculation
```

2. **開發和測試**
```bash
# 開發程式碼...
# 執行測試...
```

3. **提交變更**
```bash
git add .
git commit -m "feat: 新增稅務計算功能"
```

4. **推送到遠端**
```bash
git push origin feature/add-tax-calculation
```

5. **創建 Pull Request**
- 在 GitHub 上創建 PR
- 等待代碼審查
- 合併到 main 分支

### 📋 最佳實踐

1. **分支管理**
   - 從最新的 main 分支創建功能分支
   - 使用描述性的分支名稱
   - 保持分支小而專注

2. **提交規範**
   - 使用有意義的提交訊息
   - 遵循 Conventional Commits 格式
   - 每個提交應該是一個邏輯單元

3. **代碼審查**
   - 創建詳細的 PR 描述
   - 回應審查意見
   - 保持代碼品質

### 🛠️ 常用命令參考

```bash
# 檢查當前狀態
git status

# 查看分支
git branch -a

# 切換分支
git checkout branch-name

# 更新本地 main 分支
git checkout main && git pull origin main

# 查看提交歷史
git log --oneline --graph --decorate

# 撤銷上次提交（保留檔案變更）
git reset --soft HEAD~1
```

## 🛠️ 故障排除

### 常見問題與解決方案

#### 1. 推送被拒絕
```bash
# 錯誤訊息
error: failed to push some refs to 'origin'
hint: Updates were rejected because the remote contains work

# 解決方案：使用 feature branch
python scripts/git_flow_helper.py create "your-feature-name"
```

#### 2. 分支落後於 main
```bash
# 在 feature branch 中同步最新變更
git checkout main
git pull origin main
git checkout feature/your-feature-name
git merge main
```

#### 3. 忘記在哪個分支
```bash
python scripts/git_flow_helper.py status
# 🌿 當前分支: feature/your-feature-name
```

## 🎯 最佳實踐

### 1. 分支命名規範
```
feature/功能描述     # 新功能
fix/問題描述        # 修復
hotfix/緊急修復     # 緊急修復
docs/文檔更新       # 文檔
test/測試相關       # 測試
```

### 2. 提交訊息格式
```
類型: 簡短描述

詳細說明（可選）

相關 Issue: #123
```

### 3. PR 最佳實踐
- 保持 PR 小而聚焦
- 提供清晰的描述
- 包含測試覆蓋
- 及時回應審查意見

## 📞 獲得幫助

如果遇到 Git Flow 相關問題：

1. **查看工具幫助**: `python scripts/git_flow_helper.py`
2. **檢查當前狀態**: `python scripts/git_flow_helper.py status`
3. **參考文檔**: 查看 `docs/PROJECT_STRUCTURE.md`

---

**🎉 恭喜！您現在已經掌握了新的 Git Flow 開發流程！**

這個流程雖然多了幾個步驟，但能確保代碼品質和部署安全性。
使用我們提供的工具，整個流程會變得非常簡單和自動化。 