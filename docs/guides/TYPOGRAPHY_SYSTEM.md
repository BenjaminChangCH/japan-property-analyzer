# 文字層級系統設計規範

## 概述
本文檔定義了日本不動產投資分析工具的完整文字層級系統，確保整個應用程式的文字顯示一致、清晰且專業。

## 文字層級定義

### 標題層級

#### H1 - 主標題
- **字體大小**: 32px
- **字重**: 700 (Bold)
- **行高**: 1.2
- **用途**: 頁面主標題、報告標題
- **顏色**: 白色（在深色背景上）

#### H2 - 次標題
- **字體大小**: 24px
- **字重**: 600 (Semi-bold)
- **行高**: 1.3
- **用途**: 主要區塊標題、章節標題
- **顏色**: 主色調 (#1a4f72)
- **特殊樣式**: 底部有黃色邊框

#### H3 - 小標題
- **字體大小**: 20px
- **字重**: 600 (Semi-bold)
- **行高**: 1.4
- **用途**: 子區塊標題、功能模組標題
- **顏色**: 主色調 (#1a4f72)

#### H4 - 子標題
- **字體大小**: 16px
- **字重**: 600 (Semi-bold)
- **行高**: 1.4
- **用途**: 表單組標題、卡片標題
- **顏色**: 文字色 (#333)

### 內文層級

#### 內文 - 大
- **字體大小**: 16px
- **字重**: 400 (Regular)
- **行高**: 1.6
- **用途**: 重要說明文字、引言
- **CSS 類別**: `.text-lg`

#### 內文 - 標準
- **字體大小**: 14px
- **字重**: 400 (Regular)
- **行高**: 1.5
- **用途**: 一般內文、表單說明
- **CSS 類別**: 預設 `p` 標籤

#### 內文 - 小
- **字體大小**: 13px
- **字重**: 400 (Regular)
- **行高**: 1.4
- **用途**: 次要說明、表格內容
- **CSS 類別**: `.text-sm`

#### 說明文字
- **字體大小**: 12px
- **字重**: 400 (Regular)
- **行高**: 1.3
- **用途**: 提示文字、版權資訊
- **顏色**: #666
- **CSS 類別**: `.caption`

### 功能性文字

#### 標籤文字
- **字體大小**: 13px
- **字重**: 500 (Medium)
- **行高**: 1.2
- **用途**: 表單標籤、按鈕文字
- **顏色**: 文字色 (#333)

#### 按鈕文字
- **字體大小**: 14px
- **字重**: 500 (Medium)
- **行高**: 1.2
- **用途**: 按鈕內文字

#### 數據顯示

##### 數據 - 大
- **字體大小**: 18px
- **字重**: 600 (Semi-bold)
- **行高**: 1.2
- **用途**: 重要數據、關鍵指標
- **字體**: 等寬字體

##### 數據 - 標準
- **字體大小**: 16px
- **字重**: 600 (Semi-bold)
- **行高**: 1.2
- **用途**: 一般數據顯示
- **字體**: 等寬字體

##### 數據 - 小
- **字體大小**: 14px
- **字重**: 500 (Medium)
- **行高**: 1.2
- **用途**: 表格數據、次要數據
- **字體**: 等寬字體

## 間距系統

### 間距變數
- **XS**: 4px - 微小間距
- **SM**: 8px - 小間距
- **MD**: 16px - 標準間距
- **LG**: 24px - 大間距
- **XL**: 32px - 特大間距
- **XXL**: 48px - 超大間距

### 間距應用
- **元素內邊距**: 使用 SM 到 LG
- **元素外邊距**: 使用 MD 到 XXL
- **組件間距**: 使用 LG 到 XXL
- **區塊間距**: 使用 XL 到 XXL

## 圓角系統

- **SM**: 6px - 小元素（輸入框、小按鈕）
- **MD**: 8px - 標準元素（按鈕、卡片）
- **LG**: 12px - 大元素（面板、容器）
- **XL**: 16px - 特大元素（主容器）

## 陰影系統

- **SM**: `0 1px 3px rgba(0, 0, 0, 0.08)` - 輕微陰影
- **MD**: `0 2px 8px rgba(0, 0, 0, 0.1)` - 標準陰影
- **LG**: `0 4px 16px rgba(0, 0, 0, 0.12)` - 明顯陰影

## 字體堆疊

```css
font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### 等寬字體（數據顯示）
```css
font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace, 'Noto Sans TC';
```

## 顏色應用

### 文字顏色
- **主要文字**: #333
- **次要文字**: #6c757d
- **標題文字**: #1a4f72 (主色調)
- **說明文字**: #666
- **錯誤文字**: #dc3545
- **成功文字**: #28a745

### 背景顏色
- **主背景**: #fdfdfd
- **卡片背景**: #ffffff
- **淺色背景**: #f8f9fa
- **頁面背景**: #eef1f5

## 響應式設計

### 手機端調整 (≤ 768px)
- 標題字體適度縮小 (約 10-15%)
- 間距適度縮小
- 按鈕和輸入框增加觸控友好的尺寸

### 平板端調整 (769px - 1024px)
- 保持桌面端字體大小
- 調整間距以適應中等螢幕

## 使用指南

### CSS 變數使用
所有文字樣式都定義為 CSS 變數，使用時請引用變數而非硬編碼數值：

```css
/* 正確 */
font-size: var(--font-size-h3);
font-weight: var(--font-weight-h3);

/* 錯誤 */
font-size: 20px;
font-weight: 600;
```

### 一致性原則
1. 同類型內容使用相同的文字層級
2. 重要性層級要明確區分
3. 保持視覺層次的邏輯性
4. 確保可讀性和無障礙性

### 維護建議
1. 新增文字樣式時，優先使用現有層級
2. 如需新增層級，請更新此文檔
3. 定期檢查文字層級的一致性
4. 測試不同裝置上的顯示效果

## 更新記錄

- **2025-06-16**: 初始版本，建立完整文字層級系統
- 定義了 6 個標題層級和 4 個內文層級
- 建立了間距、圓角、陰影系統
- 統一了字體堆疊和顏色應用 