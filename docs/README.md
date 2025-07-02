# 📚 Japan Property Analyzer - 文檔中心

## 📋 核心文檔

### 產品規格
- [產品需求文檔 (PRD)](PRD.md) - 完整的產品規格和功能需求
- [變更記錄 (CHANGELOG)](CHANGELOG.md) - 版本更新歷史

### 開發指南
- [設計系統規範](guides/DESIGN_SYSTEM.md) - UI/UX 設計標準
- [Google OAuth 設定指南](guides/GOOGLE_OAUTH_SETUP.md) - 認證系統設定
- [CI/CD 部署流程](CI_CD_WORKFLOW.md) - 持續整合與部署指南

### 快速參考
- [設計系統快速參考](guides/DESIGN_SYSTEM_QUICK_REF.md)
- [字體系統指南](guides/TYPOGRAPHY_SYSTEM.md)
- [程式碼分析報告](guides/CODE_ANALYSIS.md)

## 📁 文檔結構

```
docs/
├── README.md                    # 文檔中心（本檔案）
├── PRD.md                      # 產品需求文檔
├── CHANGELOG.md                # 版本變更記錄
├── CI_CD_WORKFLOW.md           # 部署流程
├── guides/                     # 開發指南
│   ├── DESIGN_SYSTEM.md        # 設計系統
│   ├── GOOGLE_OAUTH_SETUP.md   # OAuth 設定
│   └── ...
└── archive/                    # 歷史文檔歸檔
    ├── oauth-fixes/            # OAuth 相關修復記錄
    └── completion-reports/     # 完成報告歸檔
```

## 🔧 維護指南

### 文檔更新規則
1. **核心文檔**：直接在 docs/ 根目錄更新
2. **技術指南**：放置在 guides/ 子目錄
3. **歷史記錄**：歸檔至 archive/ 目錄
4. **臨時文檔**：完成後移至 archive/ 或刪除

### 版本控制
- 重要變更需更新 CHANGELOG.md
- 每次 PR 需檢查相關文檔是否需要更新
- 保持文檔與程式碼同步

---
*最後更新：2025-07-02* 