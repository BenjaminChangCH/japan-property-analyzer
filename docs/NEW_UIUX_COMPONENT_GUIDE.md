# 🧩 NEW_UIUX 組件開發指南

**版本**: v1.0  
**建立日期**: 2025-07-02  
**維護者**: Benjamin Chang  

## 📋 組件庫概覽

此指南定義了 NEW_UIUX 功能中新增和改進的組件標準，確保所有組件都符合設計系統規範。

## 🎯 組件開發原則

### 1. 設計系統優先
- ✅ **使用 CSS 變數**: 所有樣式都必須使用設計系統定義的變數
- ✅ **遵循命名規範**: 使用 BEM 標準化命名
- ✅ **保持一致性**: 同類組件統一的視覺和行為模式

### 2. 響應式設計
- ✅ **移動優先**: 先設計移動端，再適配大屏幕
- ✅ **彈性佈局**: 使用 Flexbox 和 Grid 實現自適應
- ✅ **觸控友好**: 所有互動元素最小 44px 高度

### 3. 可用性標準
- ✅ **無障礙性**: 支援鍵盤導航、螢幕閱讀器
- ✅ **語義化**: 使用正確的 HTML 標籤和 ARIA 屬性
- ✅ **效能優化**: 最小化重繪和重排

## 🔧 核心組件模板

### 增強型按鈕組件

#### HTML 結構
```html
<button class="btn btn--primary" type="button" aria-label="主要操作按鈕">
    <span class="btn__text">開始分析</span>
</button>
```

#### CSS 樣式
```css
.btn {
    /* 佈局 */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    
    /* 尺寸 */
    padding: var(--spacing-sm) var(--spacing-lg);
    border-radius: var(--radius-md);
    min-height: 44px; /* 觸控友好 */
    
    /* 字體 */
    font-size: var(--font-size-button);
    font-weight: var(--font-weight-button);
    
    /* 視覺 */
    border: none;
    background-color: var(--primary-color);
    color: white;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    
    /* 動畫 */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.btn:focus-visible {
    outline: 2px solid var(--secondary-color);
    outline-offset: 2px;
}

.btn--secondary {
    background-color: transparent;
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
}
```

### 增強型卡片組件

#### HTML 結構
```html
<article class="card" role="article">
    <header class="card__header">
        <h3 class="card__title">案件標題</h3>
        <span class="badge badge--status-considering">考慮中</span>
    </header>
    <div class="card__body">
        <p class="card__description">案件描述內容...</p>
    </div>
    <footer class="card__footer">
        <button class="btn btn--secondary btn--size-sm">編輯</button>
        <button class="btn btn--primary btn--size-sm">分析</button>
    </footer>
</article>
```

#### CSS 樣式
```css
.card {
    background-color: white;
    border-radius: var(--radius-lg);
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.card__header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--spacing-md);
}

.card__title {
    font-size: var(--font-size-h4);
    font-weight: var(--font-weight-h4);
    color: var(--text-color);
    margin: 0;
}

.card__footer {
    display: flex;
    gap: var(--spacing-sm);
    justify-content: flex-end;
    border-top: 1px solid var(--border-color);
    padding-top: var(--spacing-md);
    margin-top: var(--spacing-md);
}
```

### 增強型表單組件

#### HTML 結構
```html
<div class="form__group">
    <label class="form__label" for="input-name">
        標籤名稱 <span class="form__required">*</span>
    </label>
    <input 
        class="form__input" 
        type="text" 
        id="input-name" 
        name="inputName"
        required
        aria-describedby="input-name-error"
    >
    <div class="form__error" id="input-name-error" role="alert"></div>
</div>
```

#### CSS 樣式
```css
.form__group {
    margin-bottom: var(--spacing-lg);
}

.form__label {
    display: block;
    font-size: var(--font-size-label);
    font-weight: var(--font-weight-label);
    margin-bottom: var(--spacing-sm);
}

.form__input {
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    font-size: var(--font-size-body);
    transition: all 0.2s ease;
}

.form__input:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(26, 79, 114, 0.1);
}

.form__error {
    color: var(--error-color);
    font-size: var(--font-size-caption);
    margin-top: var(--spacing-xs);
    min-height: 1.2em;
}
```

## 📱 響應式設計

### 斷點策略
```css
/* 手機端 */
@media (max-width: 768px) {
    .btn {
        width: 100%;
        min-height: 48px;
    }
    
    .card {
        padding: var(--spacing-md);
    }
    
    .card__footer {
        flex-direction: column;
    }
}

/* 平板端 */
@media (min-width: 769px) and (max-width: 1024px) {
    .card {
        margin-bottom: var(--spacing-lg);
    }
}
```

## 🎨 動畫效果

### 載入動畫
```css
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-on-load {
    animation: fadeInUp 0.6s ease-out;
}
```

### 互動動畫
```css
.btn {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
```

## 📋 開發檢查清單

### 組件完成檢查
- [ ] ✅ **設計系統合規**: 使用 CSS 變數，無硬編碼值
- [ ] ✅ **響應式設計**: 在所有斷點正常顯示
- [ ] ✅ **無障礙性**: 支援鍵盤導航和螢幕閱讀器
- [ ] ✅ **瀏覽器相容性**: 支援主流瀏覽器
- [ ] ✅ **效能優化**: 無不必要的重繪和重排
- [ ] ✅ **測試覆蓋**: 包含單元測試和整合測試

### 最佳實踐
1. **CSS 組織**: 按 BEM 命名規範組織樣式
2. **JavaScript 增強**: 漸進式增強，不依賴 JS 的基本功能
3. **效能考量**: 使用 `transform` 和 `opacity` 進行動畫
4. **可維護性**: 模組化設計，便於後續擴展

## 🔗 相關資源

- [設計系統規範](guides/DESIGN_SYSTEM.md)
- [開發計劃](NEW_UIUX_DEVELOPMENT_PLAN.md)
- [測試規範](../tests/test_new_uiux.py)

---

**維護者**: Benjamin Chang  
**最後更新**: 2025-07-02  
**版本**: v1.0 