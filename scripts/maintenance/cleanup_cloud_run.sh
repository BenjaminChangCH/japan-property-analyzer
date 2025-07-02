#!/bin/bash

# Cloud Run 服務清理腳本
# 安全地清理舊的不需要的服務

set -e

echo "🧹 Cloud Run 服務清理腳本"
echo "══════════════════════════════════════════════════════════════════"

# 顏色設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 列出所有服務
echo -e "${BLUE}📋 當前所有 Cloud Run 服務：${NC}"
gcloud run services list --platform=managed --region=asia-northeast1 --format="table(metadata.name,status.url,status.latestReadyRevisionName)"
echo ""

# 確認當前正在使用的服務
echo -e "${GREEN}✅ 正在使用的服務：${NC}"
echo "  • japan-property-analyzer (STG 環境)"
echo "  • japan-property-analyzer-prod (PRD 環境)"
echo ""

echo -e "${YELLOW}⚠️  建議刪除的服務：${NC}"
echo "  • japan-property-analyzer-stg (舊的 STG 環境，已不再使用)"
echo ""

# 安全檢查
echo -e "${RED}🚨 安全確認 🚨${NC}"
echo "刪除服務是不可逆的操作，請確認："
echo "1. 舊的 STG 服務 (japan-property-analyzer-stg) 確實不再需要"
echo "2. 沒有任何 OAuth redirect URI 指向該服務"
echo "3. 沒有任何外部連結指向該服務"
echo ""

read -p "確認要刪除 japan-property-analyzer-stg 服務嗎？(y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}正在刪除 japan-property-analyzer-stg 服務...${NC}"
    
    # 刪除服務
    gcloud run services delete japan-property-analyzer-stg \
        --region=asia-northeast1 \
        --quiet
        
    echo -e "${GREEN}✅ 服務已成功刪除${NC}"
    echo ""
    
    # 顯示清理後的服務列表
    echo -e "${BLUE}📋 清理後的服務列表：${NC}"
    gcloud run services list --platform=managed --region=asia-northeast1 --format="table(metadata.name,status.url,status.latestReadyRevisionName)"
    
else
    echo -e "${BLUE}💡 取消刪除，服務保持不變${NC}"
fi

echo ""
echo -e "${GREEN}🎉 清理腳本執行完成${NC}"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}📝 重要提醒：${NC}"
echo "  • STG 環境 URL: https://japan-property-analyzer-2dal3iq3qa-an.a.run.app"
echo "  • PRD 環境 URL: https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app"
echo "  • 這些 URL 在重新部署時不會改變"
echo "  • OAuth redirect URI 已正確配置，無需修改" 