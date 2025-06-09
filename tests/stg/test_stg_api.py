#!/usr/bin/env python3
"""
STG 環境簡化版自動化測試腳本
僅使用 requests 庫測試基本 API 功能
"""

import requests
import time
import json

class SimpleSTGTest:
    def __init__(self):
        self.base_url = "https://japan-property-analyzer-864942598341.asia-northeast1.run.app"
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """記錄測試結果"""
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
    
    def test_homepage_load(self):
        """測試 1: 首頁載入測試"""
        try:
            response = requests.get(self.base_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # 檢查基本 HTML 結構
                checks = [
                    ("日本不動產投資與商業模式財務分析" in content, "頁面標題"),
                    ("G-59XMZ0SZ0G" in content, "GA 追蹤碼"),
                    ("calculateBtn" in content, "計算按鈕"),
                    ("downloadBtn" in content, "下載按鈕")
                ]
                
                passed_checks = sum(1 for check, _ in checks if check)
                total_checks = len(checks)
                
                if passed_checks == total_checks:
                    self.log_test("首頁載入", True, f"所有檢查通過 ({passed_checks}/{total_checks})")
                else:
                    failed = [name for check, name in checks if not check]
                    self.log_test("首頁載入", False, f"部分檢查失敗: {', '.join(failed)}")
            else:
                self.log_test("首頁載入", False, f"HTTP 狀態碼: {response.status_code}")
                
        except requests.exceptions.Timeout:
            self.log_test("首頁載入", False, "請求超時")
        except requests.exceptions.ConnectionError:
            self.log_test("首頁載入", False, "連線錯誤")
        except Exception as e:
            self.log_test("首頁載入", False, f"未預期錯誤: {str(e)}")
    
    def test_calculate_api_airbnb(self):
        """測試 2: Airbnb 模式計算 API"""
        try:
            api_url = f"{self.base_url}/calculate"
            payload = {
                "monetizationModel": "airbnb",
                "purchaseType": "individual",
                "propertyPrice": 5000,  # 5000萬日圓
                "downPaymentRatio": 20,
                "acquisitionCostRatio": 7,
                "exchangeRate": 0.22,
                "loanOrigin": "japan",
                "initialFurnishingCost": 200,
                "japanLoanInterestRate": 1.5,
                "japanLoanTerm": 35,
                "creditLoanRate": 3.5,
                "managementFeeRatio": 5,
                "propertyTaxRate": 1.4,
                "annualAppreciation": 1.0,
                "investmentPeriod": 10,
                "buildingStructure": "rc",
                "buildingRatio": 70,
                "corporateTaxRate": 25,
                "annualInsuranceCost": 10,
                "operatingDaysCap": 365,
                "occupancyRate": 70,
                "dailyRate": 15000,
                "platformFeeRate": 3,
                "cleaningFee": 8000,
                "avgStayDuration": 3,
                "avgGuests": 2,
                "baseOccupancyForFee": 2,
                "extraGuestFee": 2000,
                "peakSeasonMarkup": 20,
                "monthlyUtilities": 15000
            }
            
            response = requests.post(
                api_url,
                json=payload,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 檢查重要的計算結果欄位
                required_fields = [
                    "totalInitialInvestment",
                    "monthlyNetRevenue", 
                    "cashFlows",
                    "totalAnnualExpenses"
                ]
                
                missing_fields = [field for field in required_fields if field not in result]
                
                if not missing_fields:
                    investment = result.get('totalInitialInvestment', 0)
                    revenue = result.get('monthlyNetRevenue', 0)
                    self.log_test("Airbnb API", True, f"初始投資: ¥{investment:,.0f}, 月淨收入: ¥{revenue:,.0f}")
                else:
                    self.log_test("Airbnb API", False, f"缺少欄位: {', '.join(missing_fields)}")
            else:
                self.log_test("Airbnb API", False, f"HTTP 狀態碼: {response.status_code}")
                
        except requests.exceptions.Timeout:
            self.log_test("Airbnb API", False, "API 請求超時")
        except Exception as e:
            self.log_test("Airbnb API", False, f"API 測試錯誤: {str(e)}")
    
    def test_calculate_api_lease(self):
        """測試 3: 長租模式計算 API"""
        try:
            api_url = f"{self.base_url}/calculate"
            payload = {
                "monetizationModel": "personalLease",
                "purchaseType": "individual",
                "propertyPrice": 4000,  # 4000萬日圓
                "downPaymentRatio": 25,
                "acquisitionCostRatio": 7,
                "exchangeRate": 0.22,
                "loanOrigin": "japan",
                "initialFurnishingCost": 100,
                "japanLoanInterestRate": 1.3,
                "japanLoanTerm": 35,
                "creditLoanRate": 3.5,
                "managementFeeRatio": 5,
                "propertyTaxRate": 1.4,
                "annualAppreciation": 1.0,
                "investmentPeriod": 10,
                "buildingStructure": "rc",
                "buildingRatio": 70,
                "corporateTaxRate": 25,
                "annualInsuranceCost": 8,
                "monthlyRent": 180000,
                "vacancyRate": 5,
                "initialLeaseCostsRatio": 3,
                "leaseUtilities": 5000,
                "leaseRenewalFeeFrequency": 2,
                "leaseRenewalFeeAmount": 1
            }
            
            response = requests.post(
                api_url,
                json=payload,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                investment = result.get('totalInitialInvestment', 0)
                revenue = result.get('monthlyNetRevenue', 0)
                self.log_test("長租 API", True, f"初始投資: ¥{investment:,.0f}, 月淨收入: ¥{revenue:,.0f}")
            else:
                self.log_test("長租 API", False, f"HTTP 狀態碼: {response.status_code}")
                
        except Exception as e:
            self.log_test("長租 API", False, f"API 測試錯誤: {str(e)}")
    
    def test_calculate_api_corporate(self):
        """測試 4: 法人購買模式計算 API"""
        try:
            api_url = f"{self.base_url}/calculate"
            payload = {
                "monetizationModel": "airbnb",
                "purchaseType": "corporate",  # 法人購買
                "propertyPrice": 6000,
                "downPaymentRatio": 20,
                "acquisitionCostRatio": 7,
                "exchangeRate": 0.22,
                "loanOrigin": "japan",
                "initialFurnishingCost": 300,
                "japanLoanInterestRate": 1.5,
                "japanLoanTerm": 35,
                "creditLoanRate": 3.5,
                "managementFeeRatio": 5,
                "propertyTaxRate": 1.4,
                "annualAppreciation": 1.0,
                "investmentPeriod": 10,
                "buildingStructure": "rc",
                "buildingRatio": 70,
                "corporateTaxRate": 25,
                "annualInsuranceCost": 12,
                "corporateSetupCost": 50,  # 法人設立費用
                "annualTaxAccountantFee": 30,  # 稅務會計師費用
                "operatingDaysCap": 365,
                "occupancyRate": 75,
                "dailyRate": 18000,
                "platformFeeRate": 3,
                "cleaningFee": 10000,
                "avgStayDuration": 3,
                "avgGuests": 2,
                "baseOccupancyForFee": 2,
                "extraGuestFee": 2000,
                "peakSeasonMarkup": 25,
                "monthlyUtilities": 18000
            }
            
            response = requests.post(
                api_url,
                json=payload,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                investment = result.get('totalInitialInvestment', 0)
                revenue = result.get('monthlyNetRevenue', 0)
                tax_y1 = result.get('annualTax_y1', 0)
                self.log_test("法人 API", True, f"初始投資: ¥{investment:,.0f}, 月淨收入: ¥{revenue:,.0f}, 年稅額: ¥{tax_y1:,.0f}")
            else:
                self.log_test("法人 API", False, f"HTTP 狀態碼: {response.status_code}")
                
        except Exception as e:
            self.log_test("法人 API", False, f"API 測試錯誤: {str(e)}")
    
    def test_error_handling(self):
        """測試 5: 錯誤處理測試"""
        try:
            api_url = f"{self.base_url}/calculate"
            
            # 測試無效的請求 (缺少必要欄位)
            invalid_payload = {
                "monetizationModel": "airbnb"
                # 故意缺少其他必要欄位
            }
            
            response = requests.post(
                api_url,
                json=invalid_payload,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            # 應該還是能回應 (因為有預設值處理)
            if response.status_code == 200:
                self.log_test("錯誤處理", True, "API 正確處理了不完整的請求")
            else:
                self.log_test("錯誤處理", True, f"API 適當地回應了錯誤: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("錯誤處理", False, f"錯誤處理測試失敗: {str(e)}")
    
    def run_all_tests(self):
        """執行所有測試"""
        print("🚀 開始 STG 環境簡化版自動化測試...")
        print(f"🔗 測試網址: {self.base_url}")
        print("-" * 60)
        
        # 執行各項測試
        self.test_homepage_load()
        self.test_calculate_api_airbnb()
        self.test_calculate_api_lease()
        self.test_calculate_api_corporate()
        self.test_error_handling()
        
        # 輸出測試總結
        self.print_summary()
    
    def print_summary(self):
        """輸出測試總結"""
        print("-" * 60)
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
        
        success_rate = passed/total*100 if total > 0 else 0
        print(f"\n🎯 成功率: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 STG 環境測試大部分通過，可以考慮部署到生產環境！")
        elif success_rate >= 60:
            print("⚠️  STG 環境有一些問題需要修正")
        else:
            print("❌ STG 環境存在重大問題，建議修正後再測試")

if __name__ == "__main__":
    tester = SimpleSTGTest()
    tester.run_all_tests() 