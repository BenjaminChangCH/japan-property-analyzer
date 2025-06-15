# 🎨 日本不動產投資分析工具 - 設計系統規範

## 📋 文件概述

本文件定義了日本不動產投資分析工具的完整設計系統，是所有 UI/UX 開發的標準依據。

**重要原則**：
- ✅ **優先使用現有規範** - 開發新功能時必須先參考此規範
- ⚠️ **謹慎修改系統** - 只有在現有規範無法滿足需求時才考慮修改
- 📝 **記錄所有變更** - 任何修改都必須更新此文件並說明原因

---

## 🎯 設計原則

### 核心價值
1. **專業性** - 體現金融分析工具的專業形象
2. **清晰性** - 資訊層次分明，易於理解
3. **一致性** - 統一的視覺語言和互動模式
4. **可用性** - 優秀的用戶體驗和無障礙性
5. **可維護性** - 模組化設計，便於擴展和維護

### 設計哲學
- **內容優先** - 設計服務於內容，不喧賓奪主
- **漸進增強** - 從基礎功能開始，逐步增加複雜性
- **響應式優先** - 移動端、平板、桌面全覆蓋
- **性能導向** - 快速載入，流暢互動

---

## 🔤 文字系統 (Typography System)

### 字體堆疊 (Font Stack)

#### 主要字體
```css
font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

#### 等寬字體（數據顯示）
```css
font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace, 'Noto Sans TC';
```

### 文字層級定義

#### 標題層級 (Headings)

| 層級 | 大小 | 字重 | 行高 | 用途 | CSS 變數 |
|------|------|------|------|------|----------|
| H1 | 32px | 700 | 1.2 | 頁面主標題 | `--font-size-h1` |
| H2 | 24px | 600 | 1.3 | 區塊標題 | `--font-size-h2` |
| H3 | 20px | 600 | 1.4 | 子區塊標題 | `--font-size-h3` |
| H4 | 16px | 600 | 1.4 | 組件標題 | `--font-size-h4` |

#### 內文層級 (Body Text)

| 層級 | 大小 | 字重 | 行高 | 用途 | CSS 類別 |
|------|------|------|------|------|----------|
| 大 | 16px | 400 | 1.6 | 重要說明 | `.text-lg` |
| 標準 | 14px | 400 | 1.5 | 一般內文 | 預設 |
| 小 | 13px | 400 | 1.4 | 次要說明 | `.text-sm` |
| 說明 | 12px | 400 | 1.3 | 提示文字 | `.caption` |

#### 功能性文字 (Functional Text)

| 類型 | 大小 | 字重 | 行高 | 用途 | CSS 變數 |
|------|------|------|------|------|----------|
| 標籤 | 13px | 500 | 1.2 | 表單標籤 | `--font-size-label` |
| 按鈕 | 14px | 500 | 1.2 | 按鈕文字 | `--font-size-button` |
| 數據大 | 18px | 600 | 1.2 | 關鍵指標 | `--font-size-data-lg` |
| 數據標準 | 16px | 600 | 1.2 | 一般數據 | `--font-size-data` |
| 數據小 | 14px | 500 | 1.2 | 表格數據 | `--font-size-data-sm` |

### 使用規則

#### ✅ 正確使用
```css
/* 使用 CSS 變數 */
font-size: var(--font-size-h3);
font-weight: var(--font-weight-h3);
line-height: var(--line-height-h3);
```

#### ❌ 錯誤使用
```css
/* 硬編碼數值 */
font-size: 20px;
font-weight: 600;
```

---

## 🎨 色彩系統 (Color System)

### 主色調 (Primary Colors)

| 名稱 | 色碼 | 用途 | CSS 變數 |
|------|------|------|----------|
| 主色調 | `#1a4f72` | 標題、按鈕、重點 | `--primary-color` |
| 次色調 | `#f0b90b` | 強調、邊框、圖標 | `--secondary-color` |

### 中性色 (Neutral Colors)

| 名稱 | 色碼 | 用途 | CSS 變數 |
|------|------|------|----------|
| 文字色 | `#333` | 主要文字 | `--text-color` |
| 次要文字 | `#6c757d` | 說明文字 | - |
| 提示文字 | `#666` | 輔助資訊 | - |
| 邊框色 | `#dee2e6` | 邊框、分隔線 | `--border-color` |

### 背景色 (Background Colors)

| 名稱 | 色碼 | 用途 | CSS 變數 |
|------|------|------|----------|
| 主背景 | `#fdfdfd` | 頁面背景 | `--background-color` |
| 卡片背景 | `#ffffff` | 卡片、面板 | - |
| 淺色背景 | `#f8f9fa` | 表格標題、輸入框 | `--light-gray` |
| 頁面背景 | `#eef1f5` | 外層背景 | - |

### 狀態色 (Status Colors)

| 狀態 | 色碼 | 用途 |
|------|------|------|
| 成功 | `#28a745` | 正面數據、成功狀態 |
| 警告 | `#ffc107` | 注意事項、中性狀態 |
| 危險 | `#dc3545` | 負面數據、錯誤狀態 |
| 資訊 | `#17a2b8` | 一般資訊、提示 |

### 健康指標色彩

| 等級 | 背景色 | 文字色 | 用途 |
|------|--------|--------|------|
| 優秀 | `#d4edda` | `#155724` | 表現優異 |
| 良好 | `#d1ecf1` | `#0c5460` | 表現良好 |
| 警告 | `#fff3cd` | `#856404` | 需要注意 |
| 危險 | `#f8d7da` | `#721c24` | 需要改善 |

---

## 📐 間距系統 (Spacing System)

### 間距變數

| 名稱 | 數值 | 用途 | CSS 變數 |
|------|------|------|----------|
| XS | 4px | 微小間距、內部間距 | `--spacing-xs` |
| SM | 8px | 小間距、元素間距 | `--spacing-sm` |
| MD | 16px | 標準間距、組件間距 | `--spacing-md` |
| LG | 24px | 大間距、區塊間距 | `--spacing-lg` |
| XL | 32px | 特大間距、主要區塊 | `--spacing-xl` |
| XXL | 48px | 超大間距、頁面區塊 | `--spacing-xxl` |

### 應用規則

#### 內邊距 (Padding)
- **小元素**: XS ~ SM (4px ~ 8px)
- **按鈕、輸入框**: SM ~ MD (8px ~ 16px)
- **卡片、面板**: MD ~ LG (16px ~ 24px)
- **主要容器**: LG ~ XL (24px ~ 32px)

#### 外邊距 (Margin)
- **文字段落**: MD (16px)
- **組件間距**: MD ~ LG (16px ~ 24px)
- **區塊間距**: LG ~ XXL (24px ~ 48px)
- **頁面區塊**: XL ~ XXL (32px ~ 48px)

---

## 🔘 圓角系統 (Border Radius System)

| 名稱 | 數值 | 用途 | CSS 變數 |
|------|------|------|----------|
| SM | 6px | 小元素（輸入框、小按鈕） | `--radius-sm` |
| MD | 8px | 標準元素（按鈕、卡片） | `--radius-md` |
| LG | 12px | 大元素（面板、容器） | `--radius-lg` |
| XL | 16px | 特大元素（主容器） | `--radius-xl` |

---

## 🌟 陰影系統 (Shadow System)

| 名稱 | 數值 | 用途 | CSS 變數 |
|------|------|------|----------|
| SM | `0 1px 3px rgba(0, 0, 0, 0.08)` | 輕微陰影 | `--shadow-sm` |
| MD | `0 2px 8px rgba(0, 0, 0, 0.1)` | 標準陰影 | `--shadow-md` |
| LG | `0 4px 16px rgba(0, 0, 0, 0.12)` | 明顯陰影 | `--shadow-lg` |

---

## 🔲 組件規範 (Component Standards)

### 按鈕 (Buttons)

#### 主要按鈕 (Primary Button)
```css
.btn {
    padding: var(--spacing-sm) var(--spacing-lg);
    border-radius: var(--radius-md);
    font-size: var(--font-size-button);
    font-weight: var(--font-weight-button);
    background-color: var(--primary-color);
    color: white;
    box-shadow: var(--shadow-sm);
}
```

#### 次要按鈕 (Secondary Button)
```css
.btn-secondary {
    background-color: transparent;
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
}
```

#### 下載按鈕 (Download Button)
```css
.btn-download {
    background-color: var(--secondary-color);
    color: var(--primary-color);
}
```

### 表單元素 (Form Elements)

#### 輸入框 (Input Fields)
```css
input, select {
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    font-size: var(--font-size-body);
    box-shadow: var(--shadow-sm);
}
```

#### 標籤 (Labels)
```css
label {
    font-size: var(--font-size-label);
    font-weight: var(--font-weight-label);
    margin-bottom: var(--spacing-sm);
}
```

### 卡片 (Cards)

#### 標準卡片
```css
.card {
    background-color: white;
    border-radius: var(--radius-md);
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-sm);
    margin-bottom: var(--spacing-lg);
}
```

#### 摘要卡片
```css
.summary-card {
    background-color: var(--light-gray);
    border-left: 4px solid var(--primary-color);
    padding: var(--spacing-lg);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
}
```

### 表格 (Tables)

#### 基礎表格
```css
table {
    border-collapse: collapse;
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

th {
    background-color: var(--light-gray);
    font-size: var(--font-size-label);
    font-weight: var(--font-weight-label);
    color: var(--primary-color);
    padding: var(--spacing-md);
}

td {
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--border-color);
}
```

#### 數據表格
```css
.data-cell {
    font-family: 'SF Mono', monospace;
    font-size: var(--font-size-data-sm);
    font-weight: var(--font-weight-data-sm);
    text-align: right;
}
```

### 工具提示 (Tooltips)

```css
.tooltip .tooltiptext {
    background-color: #2d3748;
    color: white;
    border-radius: var(--radius-md);
    padding: var(--spacing-md);
    font-size: var(--font-size-body-sm);
    box-shadow: var(--shadow-lg);
}
```

---

## 📱 響應式設計 (Responsive Design)

### 斷點定義 (Breakpoints)

| 裝置 | 寬度範圍 | 主要調整 |
|------|----------|----------|
| 手機 | ≤ 768px | 字體縮小、間距調整、單欄佈局 |
| 平板 | 769px ~ 1024px | 保持字體、調整間距、雙欄佈局 |
| 桌面 | ≥ 1025px | 完整尺寸、多欄佈局 |

### 響應式規則

#### 手機端調整
```css
@media (max-width: 768px) {
    /* 字體適度縮小 */
    h1 { font-size: calc(var(--font-size-h1) * 0.9); }
    h2 { font-size: calc(var(--font-size-h2) * 0.9); }
    
    /* 間距調整 */
    .section { padding: var(--spacing-md); }
    
    /* 按鈕觸控友好 */
    .btn { min-height: 44px; }
}
```

---

## 🎯 使用指南 (Usage Guidelines)

### 開發流程

#### 1. 需求分析階段
- 📋 確認功能需求和視覺需求
- 🔍 檢查現有組件是否能滿足需求
- 📝 記錄特殊需求和例外情況

#### 2. 設計階段
- ✅ **優先使用現有規範** - 從設計系統中選擇合適的組件
- 🔄 **組合現有元素** - 通過組合創建新的佈局
- ⚠️ **謹慎創建新元素** - 只有在必要時才創建新組件

#### 3. 開發階段
- 📐 使用 CSS 變數而非硬編碼數值
- 🧩 遵循組件規範和命名約定
- 📱 確保響應式設計的實現

#### 4. 測試階段
- 🖥️ 測試不同螢幕尺寸的顯示效果
- ♿ 檢查無障礙性和可用性
- 🎨 驗證視覺一致性

### 修改規範的流程

#### 何時可以修改設計系統？
1. **功能需求** - 現有規範無法滿足新功能需求
2. **用戶體驗** - 發現明顯的可用性問題
3. **技術限制** - 現有規範在技術實現上有困難
4. **品牌升級** - 整體品牌形象需要更新

#### 修改流程
1. **提出需求** - 詳細說明修改原因和預期效果
2. **影響評估** - 評估對現有組件和頁面的影響
3. **設計方案** - 提供具體的設計方案和實現方式
4. **團隊討論** - 與相關人員討論可行性
5. **實施修改** - 更新設計系統和相關文檔
6. **全面測試** - 確保修改不會破壞現有功能

### 命名約定 (Naming Conventions)

#### CSS 類別命名
- **組件**: `.component-name` (如 `.summary-card`)
- **修飾符**: `.component-name--modifier` (如 `.btn--secondary`)
- **狀態**: `.component-name.is-state` (如 `.btn.is-active`)
- **工具類**: `.utility-name` (如 `.text-lg`)

#### CSS 變數命名
- **字體**: `--font-size-*`, `--font-weight-*`
- **顏色**: `--color-*`, `--primary-color`
- **間距**: `--spacing-*`
- **圓角**: `--radius-*`
- **陰影**: `--shadow-*`

---

## 📚 參考資源 (References)

### 設計靈感
- [Material Design](https://material.io/design)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Ant Design](https://ant.design/)

### 技術參考
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [Responsive Web Design](https://web.dev/responsive-web-design-basics/)
- [Web Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

### 工具推薦
- **設計工具**: Figma, Sketch
- **開發工具**: Chrome DevTools, VS Code
- **測試工具**: Lighthouse, WAVE

---

## 📝 維護記錄 (Maintenance Log)

### 版本歷史

#### v1.0.0 - 2025-06-16
- 🎉 **初始版本** - 建立完整設計系統
- 📐 定義文字層級系統（6個標題層級 + 4個內文層級）
- 🎨 建立色彩系統和間距系統
- 🔘 定義圓角和陰影系統
- 📱 制定響應式設計規範
- 📋 建立組件規範和使用指南

### 待辦事項 (TODO)
- [ ] 增加動畫和過渡效果規範
- [ ] 定義圖標系統和使用規範
- [ ] 建立暗色主題支援
- [ ] 增加列印樣式規範
- [ ] 建立組件庫和 Storybook

---

## ⚠️ 重要提醒

### 開發者必讀
1. **📖 熟讀規範** - 開發前必須完整閱讀此文件
2. **🔍 優先查找** - 遇到設計需求時先查找現有規範
3. **💬 及時溝通** - 發現問題或需要修改時及時溝通
4. **📝 記錄變更** - 任何修改都要更新文檔

### 品質保證
- **一致性檢查** - 定期檢查所有頁面的視覺一致性
- **性能監控** - 確保設計系統不影響頁面性能
- **用戶反饋** - 收集用戶對界面的反饋和建議
- **持續改進** - 根據使用情況持續優化設計系統

---

**文件維護者**: Benjamin Chang  
**最後更新**: 2025-06-16  
**版本**: v1.0.0

> 💡 **提示**: 此文件是活文檔，會隨著產品發展持續更新。請定期檢查最新版本。 