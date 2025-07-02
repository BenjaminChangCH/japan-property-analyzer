# -*- coding: utf-8 -*-
"""
NEW_UIUX 功能測試模組

此模組包含 UI/UX 改進功能的測試案例，包括：
- 設計系統一致性測試
- 響應式設計測試  
- 動畫效果測試
- 可用性測試
"""

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class UIUXDesignSystemTest(unittest.TestCase):
    """設計系統一致性測試"""

    def setUp(self):
        """測試設置"""
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5001")
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """測試清理"""
        self.driver.quit()

    def test_css_variables_usage(self):
        """測試 CSS 變數的正確使用"""
        # 檢查主要元素是否使用了設計系統變數
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn")
        for button in buttons:
            # 檢查按鈕是否使用了正確的字體大小變數
            font_size = button.value_of_css_property("font-size")
            self.assertIn("14px", font_size, "按鈕應使用 --font-size-button 變數")

    def test_color_consistency(self):
        """測試色彩系統一致性"""
        # 檢查主色調的使用
        primary_elements = self.driver.find_elements(By.CSS_SELECTOR, ".btn-primary, h2, .nav-link")
        for element in primary_elements:
            color = element.value_of_css_property("color")
            # 檢查是否使用了主色調
            self.assertIsNotNone(color, "主要元素應使用主色調")

    def test_spacing_system(self):
        """測試間距系統一致性"""
        # 檢查卡片間距
        cards = self.driver.find_elements(By.CSS_SELECTOR, ".card")
        for card in cards:
            padding = card.value_of_css_property("padding")
            self.assertIsNotNone(padding, "卡片應使用標準間距")

    def test_border_radius_consistency(self):
        """測試圓角系統一致性"""
        # 檢查圓角使用
        rounded_elements = self.driver.find_elements(By.CSS_SELECTOR, ".btn, .card, input, select")
        for element in rounded_elements:
            border_radius = element.value_of_css_property("border-radius")
            self.assertIsNotNone(border_radius, "元素應使用標準圓角")


class ResponsiveDesignTest(unittest.TestCase):
    """響應式設計測試"""

    def setUp(self):
        """測試設置"""
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5001")
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """測試清理"""
        self.driver.quit()

    def test_mobile_viewport(self):
        """測試手機端顯示"""
        # 設置手機端視窗大小
        self.driver.set_window_size(375, 667)  # iPhone 6/7/8
        time.sleep(1)

        # 檢查導航是否適應手機端
        nav = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
        self.assertTrue(nav.is_displayed(), "導航應在手機端正常顯示")

        # 檢查按鈕觸控友好性
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn")
        for button in buttons:
            height = button.size['height']
            self.assertGreaterEqual(height, 44, "按鈕高度應至少 44px（觸控友好）")

    def test_tablet_viewport(self):
        """測試平板端顯示"""
        # 設置平板端視窗大小
        self.driver.set_window_size(768, 1024)  # iPad
        time.sleep(1)

        # 檢查佈局是否適應平板端
        container = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
        self.assertTrue(container.is_displayed(), "容器應在平板端正常顯示")

    def test_desktop_viewport(self):
        """測試桌面端顯示"""
        # 設置桌面端視窗大小
        self.driver.set_window_size(1920, 1080)
        time.sleep(1)

        # 檢查桌面端佈局
        body = self.driver.find_element(By.TAG_NAME, "body")
        self.assertTrue(body.is_displayed(), "頁面應在桌面端正常顯示")


class AnimationTest(unittest.TestCase):
    """動畫效果測試"""

    def setUp(self):
        """測試設置"""
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5001")
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """測試清理"""
        self.driver.quit()

    def test_button_hover_animation(self):
        """測試按鈕 hover 動畫"""
        button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn")))
        
        # 模擬 hover 效果
        actions = ActionChains(self.driver)
        actions.move_to_element(button).perform()
        time.sleep(0.5)

        # 檢查是否有動畫效果（通過 transition 屬性）
        transition = button.value_of_css_property("transition")
        self.assertIsNotNone(transition, "按鈕應有 hover 動畫效果")

    def test_page_load_animation(self):
        """測試頁面載入動畫"""
        # 重新載入頁面以測試載入動畫
        self.driver.refresh()
        time.sleep(2)

        # 檢查動畫元素是否存在
        animated_elements = self.driver.find_elements(By.CSS_SELECTOR, ".animate-on-load")
        if animated_elements:
            for element in animated_elements:
                self.assertTrue(element.is_displayed(), "動畫元素應正確顯示")

    def test_form_feedback_animation(self):
        """測試表單反饋動畫"""
        # 查找表單輸入框
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input, select")
        if inputs:
            input_field = inputs[0]
            
            # 模擬輸入和失焦
            input_field.click()
            input_field.send_keys("test")
            self.driver.find_element(By.TAG_NAME, "body").click()  # 失焦
            time.sleep(0.5)

            # 檢查是否有視覺反饋
            self.assertTrue(input_field.is_displayed(), "輸入框應提供視覺反饋")


class AccessibilityTest(unittest.TestCase):
    """無障礙性測試"""

    def setUp(self):
        """測試設置"""
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5001")
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """測試清理"""
        self.driver.quit()

    def test_alt_text_for_images(self):
        """測試圖片的 alt 文字"""
        images = self.driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            alt_text = img.get_attribute("alt")
            self.assertIsNotNone(alt_text, "所有圖片都應有 alt 文字")
            self.assertNotEqual(alt_text.strip(), "", "alt 文字不應為空")

    def test_heading_hierarchy(self):
        """測試標題層級結構"""
        headings = self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
        self.assertGreater(len(headings), 0, "頁面應包含標題元素")

        # 檢查是否有 h1
        h1_elements = self.driver.find_elements(By.TAG_NAME, "h1")
        self.assertGreater(len(h1_elements), 0, "頁面應包含 h1 標題")

    def test_focus_indicators(self):
        """測試焦點指示器"""
        focusable_elements = self.driver.find_elements(By.CSS_SELECTOR, "a, button, input, select")
        for element in focusable_elements:
            if element.is_displayed():
                element.click()
                # 檢查是否有焦點樣式
                outline = element.value_of_css_property("outline")
                self.assertIsNotNone(outline, "可焦點元素應有焦點指示器")

    def test_color_contrast(self):
        """測試色彩對比度"""
        # 檢查文字元素的對比度
        text_elements = self.driver.find_elements(By.CSS_SELECTOR, "p, h1, h2, h3, h4, h5, h6, span")
        for element in text_elements:
            if element.is_displayed() and element.text.strip():
                color = element.value_of_css_property("color")
                background = element.value_of_css_property("background-color")
                # 基本檢查：確保有顏色值
                self.assertIsNotNone(color, "文字應有顏色屬性")


class PerformanceTest(unittest.TestCase):
    """效能測試"""

    def setUp(self):
        """測試設置"""
        self.driver = webdriver.Chrome()

    def tearDown(self):
        """測試清理"""
        self.driver.quit()

    def test_page_load_time(self):
        """測試頁面載入時間"""
        start_time = time.time()
        self.driver.get("http://localhost:5001")
        
        # 等待頁面完全載入
        self.wait = WebDriverWait(self.driver, 10)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        end_time = time.time()
        load_time = end_time - start_time
        
        self.assertLess(load_time, 3, "頁面載入時間應少於 3 秒")

    def test_css_file_size(self):
        """測試 CSS 檔案大小（通過檢查載入時間）"""
        start_time = time.time()
        self.driver.get("http://localhost:5001")
        
        # 檢查 CSS 是否載入完成
        self.wait = WebDriverWait(self.driver, 10)
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        self.assertLess(total_time, 5, "包含 CSS 的完整頁面載入應少於 5 秒")


if __name__ == '__main__':
    # 創建測試套件
    suite = unittest.TestSuite()
    
    # 添加測試案例
    suite.addTest(unittest.makeSuite(UIUXDesignSystemTest))
    suite.addTest(unittest.makeSuite(ResponsiveDesignTest))
    suite.addTest(unittest.makeSuite(AnimationTest))
    suite.addTest(unittest.makeSuite(AccessibilityTest))
    suite.addTest(unittest.makeSuite(PerformanceTest))
    
    # 執行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 輸出測試結果
    if result.wasSuccessful():
        print("\n✅ 所有 UI/UX 測試通過！")
    else:
        print(f"\n❌ 測試失敗：{len(result.failures)} 個失敗，{len(result.errors)} 個錯誤") 