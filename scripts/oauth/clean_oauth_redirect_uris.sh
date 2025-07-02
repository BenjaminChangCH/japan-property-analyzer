#!/bin/bash
# Google OAuth 重定向 URI 清理指南
# 清理多餘和過時的重定向 URI

echo "🧹 Google OAuth 重定向 URI 清理指南"
echo "===================================="
echo

echo "📋 當前 URI 狀態分析："
echo "從截圖分析，您目前有 11 個重定向 URI，其中包含多餘和過時的項目。"
echo

echo "❌ 建議刪除的 URI（多餘/過時）："
echo "2. https://japan-property-analyzer-864942598341.asia-northeast1.run.app"
echo "   ↳ 原因：舊的錯誤 STG URL，已被正確的 URI 7 取代"
echo
echo "8. https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app"
echo "   ↳ 原因：舊的錯誤 PRD URL，已被正確的 URI 11 取代"
echo
echo "9. https://www.benjamin-changch.com/oauth2callback"
echo "   ↳ 原因：個人網站 URI，與此專案無關"
echo
echo "10. https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app"
echo "    ↳ 原因：與 URI 8 重複的錯誤 PRD URL"
echo

echo "✅ 建議保留的核心 URI："
echo "1. http://localhost:5000/auth/callback"
echo "   ↳ 用途：本機開發環境"
echo
echo "3. http://localhost:8080/auth/callback"
echo "   ↳ 用途：本機開發環境（備用端口）"
echo
echo "4. http://localhost:5001/auth/callback"
echo "   ↳ 用途：本機開發環境（備用端口）"
echo
echo "5. http://127.0.0.1:5000/auth/callback"
echo "   ↳ 用途：本機開發環境（IP 形式）"
echo
echo "6. http://127.0.0.1:5001/auth/callback"
echo "   ↳ 用途：本機開發環境（IP 形式備用）"
echo
echo "7. https://japan-property-analyzer-2dal3iq3qa-an.a.run.app/auth/callback"
echo "   ↳ 用途：STG 測試環境（正確 URL）"
echo
echo "11. https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app/auth/callback"
echo "    ↳ 用途：PRD 生產環境（正確 URL）"
echo

echo "🔧 清理步驟："
echo "1. 前往 Google Cloud Console"
echo "   https://console.cloud.google.com/apis/credentials"
echo
echo "2. 選擇專案：project-japan-462310"
echo
echo "3. 編輯 OAuth 2.0 用戶端 ID"
echo
echo "4. 刪除以下 4 個多餘的 URI："
echo "   ❌ URI 2: https://japan-property-analyzer-864942598341.asia-northeast1.run.app"
echo "   ❌ URI 8: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app"
echo "   ❌ URI 9: https://www.benjamin-changch.com/oauth2callback"
echo "   ❌ URI 10: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app"
echo
echo "5. 確認保留的 7 個核心 URI："
echo "   ✅ http://localhost:5000/auth/callback"
echo "   ✅ http://localhost:8080/auth/callback"
echo "   ✅ http://localhost:5001/auth/callback"
echo "   ✅ http://127.0.0.1:5000/auth/callback"
echo "   ✅ http://127.0.0.1:5001/auth/callback"
echo "   ✅ https://japan-property-analyzer-2dal3iq3qa-an.a.run.app/auth/callback"
echo "   ✅ https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app/auth/callback"
echo
echo "6. 儲存設定"
echo

echo "💡 清理後的好處："
echo "- 🎯 配置更加清晰易懂"
echo "- 🔒 減少安全風險（移除無用的端點）"
echo "- 🧹 避免未來的混淆和錯誤"
echo "- 📋 更容易維護和管理"
echo

echo "⚠️ 注意事項："
echo "- 清理不會影響現有功能"
echo "- 所有環境的 OAuth 登入仍然正常"
echo "- 建議在非高峰時間進行清理"
echo "- 清理後可立即測試各環境登入功能"
echo

echo "🧪 清理後測試清單："
echo "□ 本機開發環境登入測試"
echo "□ STG 環境登入測試"
echo "□ PRD 環境登入測試"
echo

echo "✅ 清理完成後，您將擁有一個乾淨、高效的 OAuth 配置！" 