#!/bin/bash
# 修復自定義網域 Google OAuth 重定向 URI 問題
# 專門處理 https://www.benjamin-changch.com 的 OAuth 登入失敗

echo "🔧 修復自定義網域 Google OAuth 問題"
echo "===================================="
echo

echo "🚨 問題診斷："
echo "網域：https://www.benjamin-changch.com"
echo "錯誤：redirect_uri_mismatch (400)"
echo "原因：Google Cloud Console 中缺少自定義網域的重定向 URI"
echo

echo "📋 當前 OAuth 配置分析："
echo "從您的截圖可以看到，您目前有 11 個重定向 URI，但缺少關鍵的自定義網域 URI。"
echo

echo "❌ 問題 URI（需要修復）："
echo "缺少：https://www.benjamin-changch.com/auth/callback"
echo

echo "🔧 立即修復步驟："
echo "=================================="
echo

echo "1️⃣ 前往 Google Cloud Console"
echo "   網址：https://console.cloud.google.com/apis/credentials?project=project-japan-462310"
echo

echo "2️⃣ 編輯 OAuth 2.0 用戶端 ID"
echo "   Client ID：864942598341-9mo8q9571hmbkj8eabhjcesgq44ddsul.apps.googleusercontent.com"
echo "   名稱：日本不動產投資分析工具"
echo

echo "3️⃣ 在「已授權的重新導向 URI」中添加："
echo "   ✅ https://www.benjamin-changch.com/auth/callback"
echo

echo "4️⃣ 確認完整的核心重定向 URI 清單："
echo "   ✅ http://localhost:5000/auth/callback (本機開發)"
echo "   ✅ http://localhost:5001/auth/callback (本機開發備用)"
echo "   ✅ https://japan-property-analyzer-2dal3iq3qa-an.a.run.app/auth/callback (STG)"
echo "   ✅ https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app/auth/callback (PRD)"
echo "   ✅ https://www.benjamin-changch.com/auth/callback (自定義網域) ⭐ 新增"
echo

echo "5️⃣ 清理建議（可選）："
echo "   可以刪除以下過時的 URI："
echo "   ❌ https://japan-property-analyzer-864942598341.asia-northeast1.run.app (舊 STG)"
echo "   ❌ https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app (舊 PRD)"
echo "   ❌ https://www.benjamin-changch.com/oauth2callback (錯誤路徑)"
echo

echo "6️⃣ 儲存設定並等待生效"
echo "   - 點擊「儲存」按鈕"
echo "   - 等待 5-10 分鐘讓設定生效"
echo

echo "🧪 修復後測試步驟："
echo "=================================="
echo "1. 前往：https://www.benjamin-changch.com"
echo "2. 點擊「使用 Google 登入」按鈕"
echo "3. 確認能正常重定向到 Google 登入頁面"
echo "4. 完成登入後確認能正常返回應用程式"
echo

echo "📊 環境狀態檢查："
echo "=================================="
echo

# 檢查各環境狀態
echo "🔍 檢查各環境可訪問性..."
echo

echo -n "自定義網域狀態: "
if curl -s -o /dev/null -w "%{http_code}" https://www.benjamin-changch.com | grep -q "200"; then
    echo "✅ 正常運行"
else
    echo "❌ 無法訪問"
fi

echo -n "STG 環境狀態: "
if curl -s -o /dev/null -w "%{http_code}" https://japan-property-analyzer-2dal3iq3qa-an.a.run.app | grep -q "200"; then
    echo "✅ 正常運行"
else
    echo "❌ 無法訪問"
fi

echo -n "PRD 環境狀態: "
if curl -s -o /dev/null -w "%{http_code}" https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app | grep -q "200"; then
    echo "✅ 正常運行"
else
    echo "❌ 無法訪問"
fi

echo

echo "🎯 修復完成後的預期結果："
echo "✅ 自定義網域 Google 登入功能正常"
echo "✅ 所有環境的 OAuth 功能都正常運作"
echo "✅ 用戶可以在 https://www.benjamin-changch.com 正常登入"
echo

echo "⚠️ 重要提醒："
echo "1. 必須在 Google Cloud Console 中手動添加重定向 URI"
echo "2. 設定變更需要 5-10 分鐘生效"
echo "3. 如果仍有問題，請檢查是否有快取問題"
echo

echo "📞 如需協助："
echo "如果修復後仍有問題，請提供以下資訊："
echo "- 錯誤訊息截圖"
echo "- 瀏覽器開發者工具的 Network 標籤"
echo "- 是否已確認在 Google Console 中添加了正確的 URI"
echo

echo "✅ 修復指南已完成！"
echo "請按照上述步驟在 Google Cloud Console 中添加重定向 URI。" 