# 🎨 設計系統快速參考

> 📖 **完整文檔**: `docs/DESIGN_SYSTEM.md`

## ⚡ 快速規則

### ✅ 必須做
- 使用 CSS 變數而非硬編碼
- 先查閱設計系統再開發
- 遵循響應式設計原則

### ❌ 禁止做
- 硬編碼字體大小、間距、顏色
- 跳過設計系統直接創建樣式
- 不一致的視覺元素

---

## 📏 常用 CSS 變數

### 文字大小
```css
--font-size-h1: 32px      /* 主標題 */
--font-size-h2: 24px      /* 次標題 */
--font-size-h3: 20px      /* 小標題 */
--font-size-h4: 16px      /* 子標題 */
--font-size-body: 14px    /* 標準內文 */
--font-size-body-lg: 16px /* 大內文 */
--font-size-body-sm: 13px /* 小內文 */
--font-size-caption: 12px /* 說明文字 */
--font-size-label: 13px   /* 標籤 */
--font-size-button: 14px  /* 按鈕 */
--font-size-data: 16px    /* 數據顯示 */
```

### 間距
```css
--spacing-xs: 4px         /* 微小間距 */
--spacing-sm: 8px         /* 小間距 */
--spacing-md: 16px        /* 標準間距 */
--spacing-lg: 24px        /* 大間距 */
--spacing-xl: 32px        /* 特大間距 */
--spacing-xxl: 48px       /* 超大間距 */
```

### 圓角
```css
--radius-sm: 6px          /* 小元素 */
--radius-md: 8px          /* 標準元素 */
--radius-lg: 12px         /* 大元素 */
--radius-xl: 16px         /* 特大元素 */
```

### 陰影
```css
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08)    /* 輕微 */
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1)     /* 標準 */
--shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12)   /* 明顯 */
```

### 顏色
```css
--primary-color: #1a4f72     /* 主色調 */
--secondary-color: #f0b90b   /* 次色調 */
--text-color: #333           /* 文字色 */
--border-color: #dee2e6      /* 邊框色 */
--light-gray: #f8f9fa        /* 淺色背景 */
```

---

## 🔧 常用組件模板

### 按鈕
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

### 卡片
```css
.card {
    background-color: white;
    border-radius: var(--radius-md);
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-sm);
    margin-bottom: var(--spacing-lg);
}
```

### 輸入框
```css
input, select {
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    font-size: var(--font-size-body);
    box-shadow: var(--shadow-sm);
}
```

### 標籤
```css
label {
    font-size: var(--font-size-label);
    font-weight: var(--font-weight-label);
    margin-bottom: var(--spacing-sm);
}
```

---

## 📱 響應式斷點

```css
/* 手機端 */
@media (max-width: 768px) {
    /* 字體縮小、間距調整、單欄佈局 */
}

/* 平板端 */
@media (769px <= width <= 1024px) {
    /* 保持字體、調整間距、雙欄佈局 */
}

/* 桌面端 */
@media (min-width: 1025px) {
    /* 完整尺寸、多欄佈局 */
}
```

---

## 🚀 Slash Commands

### 設計系統相關
- `/design-check` - 檢查設計規範符合度
- `/component [名稱]` - 創建新組件
- `/style-audit` - 審查硬編碼樣式
- `/responsive-test` - 測試響應式效果

### 開發流程
- `/init [功能]` - 初始化新功能
- `/ui [頁面]` - 開發使用者介面
- `/review` - 程式碼審查

---

## 💡 開發提示

1. **開發前**: 先查閱 `docs/DESIGN_SYSTEM.md`
2. **選擇組件**: 優先使用現有組件和樣式
3. **創建新樣式**: 必須使用 CSS 變數
4. **測試**: 確保響應式設計正常
5. **文檔**: 新組件要更新設計系統文檔

---

**快速連結**: [完整設計系統](./DESIGN_SYSTEM.md) | [文字系統](./TYPOGRAPHY_SYSTEM.md) | [變更記錄](./CHANGELOG.md) 