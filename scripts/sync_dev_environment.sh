#!/bin/bash
# 開發環境同步腳本

echo "🔄 開始同步本機開發環境..."

# 1. 檢查當前狀態
echo "1️⃣ 檢查當前環境狀態..."
git status

# 2. 如果有未保存變更，提醒用戶
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  發現未提交的變更，請選擇："
    echo "a) 提交變更 (git add . && git commit -m 'your message')"
    echo "b) 暫存變更 (git stash)"  
    echo "c) 放棄變更 (繼續執行此腳本)"
    read -p "請選擇 (a/b/c): " choice
    
    case $choice in
        a) echo "請手動提交後重新執行此腳本"; exit 1;;
        b) git stash push -m "自動暫存 $(date)"; echo "✅ 變更已暫存";;
        c) echo "⚠️  將放棄所有本機變更";;
        *) echo "❌ 無效選擇"; exit 1;;
    esac
fi

# 3. 清理未追蹤檔案
echo "2️⃣ 清理未追蹤檔案..."
git clean -fd

# 4. 從遠端拉取最新版本
echo "3️⃣ 同步遠端最新版本..."
git fetch origin
git reset --hard origin/main

# 5. 更新依賴
echo "4️⃣ 更新 Python 依賴..."
source .venv/bin/activate 2>/dev/null || source venv/bin/activate 2>/dev/null || echo "請手動啟動虛擬環境"
pip install -r requirements.txt

# 6. 驗證環境
echo "5️⃣ 驗證環境同步..."
echo "本機版本: $(python3 -c "from version import get_version_info; print(get_version_info()['version'])")"
echo "Git 版本: $(git rev-parse --short HEAD)"

echo "✅ 環境同步完成！" 