# 版本變更記錄

所有重要的專案變更都會記錄在此檔案中。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，
並且本專案遵守 [語義化版本](https://semver.org/lang/zh-TW/)。

## [1.0.0] - 2025-06-08

### 新增
- 🎯 Google Analytics 4 (GA4) 整合
  - 追蹤 ID: G-59XMZ0SZ0G
  - 事件追蹤：頁面瀏覽、計算開始、計算完成、PDF下載
- 🏗️ CI/CD 自動化部署流程
  - STG 環境：自動部署到 Cloud Run
  - PRD 環境：自動部署到 Cloud Run
- 🧪 自動化測試框架
  - 簡化版 API 測試
  - 完整版瀏覽器測試（使用 Selenium）
- 📊 環境變數管理
  - STG/PRD 環境分離
  - GA 追蹤碼環境區分
- 📋 完整的專案文件
  - 部署說明
  - 測試報告
  - 環境變數範例

### 技術棧
- **後端**: Flask (Python)
- **前端**: HTML/CSS/JavaScript
- **部署**: Google Cloud Run
- **CI/CD**: Google Cloud Build
- **監控**: Google Analytics 4
- **容器化**: Docker

### 部署環境
- **STG**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app
- **PRD**: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app 