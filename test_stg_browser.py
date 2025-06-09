#!/usr/bin/env python3
"""
STG 環境自動化測試腳本
測試日本不動產投資分析工具的主要功能流程
"""

import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class STGAutomationTest:
    def __init__(self):
        self.base_url = "https://japan-property-analyzer-864942598341.asia-northeast1.run.app"
        self.driver = None
        self.test_results = []
        
    def setup_driver(self):
        """設定 Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 無頭模式
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            return True
        except Exception as e:
            print(f"❌ 設定 WebDriver 失敗: {e}")
            return False
    
    def log_test(self, test_name, success, message=""):
        """記錄測試結果"""
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
    
    def test_page_load(self):
        """測試 1: 頁面載入測試"""
        try:
            self.driver.get(self.base_url)
            
            # 等待頁面標題載入
            WebDriverWait(self.driver, 10).until(
                EC.title_contains("日本不動產投資與商業模式財務分析")
            )
            
            # 檢查 GA 追蹤碼是否存在
            ga_script = self.driver.find_elements(By.XPATH, "//script[contains(@src, 'googletagmanager.com/gtag/js?id=G-59XMZ0SZ0G')]")
            
            if ga_script:
                self.log_test("頁面載入", True, "頁面成功載入，GA 追蹤碼已安裝")
            else:
                self.log_test("頁面載入", False, "GA 追蹤碼未找到")
                
        except TimeoutException:
            self.log_test("頁面載入", False, "頁面載入超時")
        except Exception as e:
            self.log_test("頁面載入", False, f"未預期錯誤: {str(e)}")
    
    def test_form_elements(self):
        """測試 2: 表單元素測試"""
        try:
            # 檢查主要表單元素是否存在
            required_elements = [
                ("monetizationModel", "變現模式選擇"),
                ("purchaseType", "購買類型選擇"),
                ("propertyPrice", "房屋價格輸入"),
                ("calculateBtn", "計算按鈕")
            ]
            
            missing_elements = []
            for element_id, description in required_elements:
                try:
                    element = self.driver.find_element(By.ID, element_id)
                    if not element.is_displayed():
                        missing_elements.append(f"{description} (不可見)")
                except:
                    missing_elements.append(f"{description} (未找到)")
            
            if not missing_elements:
                self.log_test("表單元素", True, "所有主要表單元素都存在且可見")
            else:
                self.log_test("表單元素", False, f"缺少元素: {', '.join(missing_elements)}")
                
        except Exception as e:
            self.log_test("表單元素", False, f"檢查表單元素時發生錯誤: {str(e)}")
    
    def test_form_interaction(self):
        """測試 3: 表單互動測試"""
        try:
            # 填寫基本表單資料
            
            # 1. 選擇變現模式
            monetization_select = Select(self.driver.find_element(By.ID, "monetizationModel"))
            monetization_select.select_by_value("airbnb")
            
            # 2. 選擇購買類型
            purchase_select = Select(self.driver.find_element(By.ID, "purchaseType"))
            purchase_select.select_by_value("individual")
            
            # 3. 填寫房屋價格 (5000萬日圓)
            price_input = self.driver.find_element(By.ID, "propertyPrice")
            price_input.clear()
            price_input.send_keys("5000")
            
            # 4. 填寫頭期款比例
            down_payment = self.driver.find_element(By.ID, "downPaymentRatio")
            down_payment.clear()
            down_payment.send_keys("20")
            
            # 5. 填寫日租金
            daily_rate = self.driver.find_element(By.ID, "dailyRate")
            daily_rate.clear()
            daily_rate.send_keys("15000")
            
            # 短暫等待表單更新
            time.sleep(1)
            
            self.log_test("表單互動", True, "成功填寫基本表單資料")
            
        except Exception as e:
            self.log_test("表單互動", False, f"填寫表單時發生錯誤: {str(e)}")
    
    def test_calculate_button(self):
        """測試 4: 計算按鈕功能測試"""
        try:
            # 點擊計算按鈕
            calculate_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "calculateBtn"))
            )
            
            # 使用 JavaScript 點擊以避免被其他元素遮擋
            self.driver.execute_script("arguments[0].click();", calculate_btn)
            
            # 等待結果顯示 (最多等待 15 秒)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "reportToPrint"))
            )
            
            # 檢查結果是否顯示
            results_container = self.driver.find_element(By.ID, "resultsContainer")
            if "hidden" not in results_container.get_attribute("class"):
                self.log_test("計算按鈕", True, "計算成功，結果已顯示")
            else:
                self.log_test("計算按鈕", False, "計算後結果未顯示")
                
        except TimeoutException:
            self.log_test("計算按鈕", False, "計算超時，結果未在預期時間內顯示")
        except ElementClickInterceptedException:
            self.log_test("計算按鈕", False, "無法點擊計算按鈕 (被其他元素遮擋)")
        except Exception as e:
            self.log_test("計算按鈕", False, f"計算過程中發生錯誤: {str(e)}")
    
    def test_download_button(self):
        """測試 5: 下載按鈕測試"""
        try:
            # 檢查下載按鈕是否可見
            download_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "downloadBtn"))
            )
            
            if "hidden" in download_btn.get_attribute("class"):
                self.log_test("下載按鈕", False, "下載按鈕未顯示")
                return
            
            # 點擊下載按鈕 (不等待實際下載完成，只測試點擊動作)
            self.driver.execute_script("arguments[0].click();", download_btn)
            
            # 短暫等待，讓下載動作開始
            time.sleep(2)
            
            self.log_test("下載按鈕", True, "下載按鈕點擊成功")
            
        except TimeoutException:
            self.log_test("下載按鈕", False, "下載按鈕未在預期時間內出現")
        except Exception as e:
            self.log_test("下載按鈕", False, f"下載按鈕測試時發生錯誤: {str(e)}")
    
    def test_api_endpoint(self):
        """測試 6: API 端點測試"""
        try:
            # 測試計算 API
            api_url = f"{self.base_url}/calculate"
            test_payload = {
                "monetizationModel": "airbnb",
                "purchaseType": "individual",
                "propertyPrice": 5000,
                "downPaymentRatio": 20,
                "acquisitionCostRatio": 7,
                "exchangeRate": 0.22,
                "loanOrigin": "japan",
                "dailyRate": 15000,
                "occupancyRate": 70
            }
            
            response = requests.post(
                api_url, 
                json=test_payload, 
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'totalInitialInvestment' in result:
                    self.log_test("API 端點", True, f"API 回應正常，初始投資: {result.get('totalInitialInvestment', 'N/A')}")
                else:
                    self.log_test("API 端點", False, "API 回應格式不正確")
            else:
                self.log_test("API 端點", False, f"API 回應錯誤: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            self.log_test("API 端點", False, "API 請求超時")
        except Exception as e:
            self.log_test("API 端點", False, f"API 測試時發生錯誤: {str(e)}")
    
    def run_all_tests(self):
        """執行所有測試"""
        print("🚀 開始 STG 環境自動化測試...")
        print(f"🔗 測試網址: {self.base_url}")
        print("-" * 50)
        
        if not self.setup_driver():
            print("❌ 無法設定 WebDriver，測試終止")
            return
        
        try:
            # 執行各項測試
            self.test_page_load()
            self.test_form_elements()
            self.test_form_interaction()
            self.test_calculate_button()
            self.test_download_button()
            self.test_api_endpoint()
            
        finally:
            if self.driver:
                self.driver.quit()
        
        # 輸出測試總結
        self.print_summary()
    
    def print_summary(self):
        """輸出測試總結"""
        print("-" * 50)
        print("📊 測試總結:")
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"✅ 通過: {passed}/{total}")
        print(f"❌ 失敗: {total - passed}/{total}")
        
        if total - passed > 0:
            print("\n❌ 失敗的測試:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   - {result['test']}: {result['message']}")
        
        print(f"\n🎯 成功率: {passed/total*100:.1f}%")

if __name__ == "__main__":
    tester = STGAutomationTest()
    tester.run_all_tests() 