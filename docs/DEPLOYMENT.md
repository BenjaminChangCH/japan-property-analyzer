# 部署說明文件

## Google Analytics 整合

### GA4 設定
- **測量 ID**: `G-59XMZ0SZ0G`
- **追蹤事件**:
  - `page_view`: 頁面瀏覽
  - `calculation_started`: 開始計算分析
  - `calculation_completed`: 完成計算分析
  - `pdf_download`: 下載 PDF 報告

### 環境變數
```bash
GA_TRACKING_ID=G-59XMZ0SZ0G
ENVIRONMENT=staging|production
```

## CI/CD 部署流程

### STG 環境部署 ✅ 已完成
1. 推送到任何非 `main` 分支
2. 觸發 `cloudbuild-staging.yaml`
3. 部署到 `japan-property-analyzer` (STG)

### 生產環境部署 ✅ 已完成
1. 合併 PR 到 `main` 分支
2. 觸發 `cloudbuild-production.yaml`
3. 部署到 `japan-property-analyzer-prod` (PRD)

## 手動部署指令

### 部署到 STG
```bash
gcloud builds submit --config cloudbuild-staging.yaml
```

### 部署到生產環境
```bash
gcloud builds submit --config cloudbuild-production.yaml
```

## 驗證 GA 追蹤

1. 開啟 [Google Analytics 即時報告](https://analytics.google.com/analytics/web/#/p/your-property-id/realtime/overview)
2. 訪問網站並執行以下操作：
   - 瀏覽頁面
   - 點擊「生成分析報告」
   - 下載 PDF 報告
3. 在即時報告中確認事件被正確追蹤

## 環境 URL

- **STG**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app ✅ 已部署
- **PRD**: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app ✅ 已部署

## 最新部署狀態

### STG 環境 ✅
- 部署時間: 2025-06-08T18:26:18.179986Z
- 狀態: 運行中
- 權限: 公開存取 (allUsers)
- GA 追蹤: 已啟用
- 環境變數: ENVIRONMENT=staging

### PRD 環境 ✅
- 部署時間: 2025-06-08T18:47:03.246024Z
- 狀態: 運行中
- 權限: 公開存取 (allUsers)
- GA 追蹤: 已啟用
- 環境變數: ENVIRONMENT=production

## 🎉 部署完成！

### ✅ 已完成的功能
- Google Analytics 4 整合
- STG 和 PRD 環境分離
- 自動化 CI/CD 流程
- 環境變數管理
- 自動化測試腳本

### 📊 監控建議
- 定期檢查 Google Analytics 數據
- 監控 Cloud Run 服務效能
- 定期執行自動化測試
- 追蹤用戶行為和轉換率

### 🔄 未來維護
- 新功能開發請使用 `feature/*` 分支
- 在 STG 環境充分測試後再合併到 main
- 定期更新依賴套件
- 監控服務日誌和錯誤 