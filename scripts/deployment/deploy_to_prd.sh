#!/bin/bash

# PRD 環境部署腳本
# 標準部署流程：STG 測試 → 合併到 main → 部署到 PRD

set -e

echo "🚀 PRD 環境部署腳本"
echo "════════════════════════════════════════════════════════════════════"

# 顏色設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查當前分支
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${BLUE}📍 當前分支: ${CURRENT_BRANCH}${NC}"

if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${YELLOW}⚠️  當前不在 main 分支，正在切換...${NC}"
    git checkout main
    git pull origin main
fi

# 檢查是否有未提交的更改
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}❌ 發現未提交的更改，請先提交或暫存${NC}"
    git status
    exit 1
fi

# 顯示最近的提交
echo -e "${BLUE}📋 最近的提交記錄:${NC}"
git log --oneline -5
echo ""

# 確認部署
echo -e "${YELLOW}🔍 PRD 部署前確認${NC}"
echo "1. STG 環境測試是否完成？"
echo "2. 所有功能是否正常運作？"
echo "3. Google OAuth 是否測試通過？"
echo "4. 效能測試是否滿意？"
echo ""

read -p "確認要部署到 PRD 環境嗎？(y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}🚀 開始 PRD 部署...${NC}"
    
    # 執行 PRD 部署
    gcloud builds submit --config=deployment/cloudbuild-production.yaml .
    
    echo -e "${GREEN}✅ PRD 部署完成！${NC}"
    echo ""
    echo -e "${BLUE}📍 PRD 環境網址:${NC}"
    echo "  • 主要網址: https://www.benjamin-changch.com/"
    echo "  • 備用網址: https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app/"
    echo ""
    echo -e "${YELLOW}🧪 請立即測試 PRD 環境:${NC}"
    echo "  1. 基本功能測試"
    echo "  2. Google OAuth 登入"
    echo "  3. 財務分析工具"
    echo "  4. 響應式設計"
    
else
    echo -e "${BLUE}💡 部署已取消${NC}"
fi

echo ""
echo -e "${GREEN}🎉 PRD 部署腳本執行完成${NC}"
echo "════════════════════════════════════════════════════════════════════" 