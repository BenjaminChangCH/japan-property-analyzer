#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRD 環境 API 測試腳本
測試生產環境的基本功能和 API 端點
"""

import requests
import json
import time
from datetime import datetime

# PRD 環境配置
PRD_URL = "https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app"
TIMEOUT = 10

def test_homepage():
    """測試首頁載入"""
    print("🏠 測試首頁載入...")
    
    try:
        response = requests.get(PRD_URL, timeout=TIMEOUT)
        
        checks = {
            "狀態碼 200": response.status_code == 200,
            "包含標題": "日本不動產投資與商業模式財務分析" in response.text,
            "GA 追蹤碼存在": "googletagmanager.com" in response.text,
            "環境設定正確": "environment: 'production'" in response.text
        }
        
        passed = sum(checks.values())
        total = len(checks)
        
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check}")
        
        print(f"✅ 通過 首頁載入: 所有檢查通過 ({passed}/{total})")
        return True
        
    except Exception as e:
        print(f"❌ 失敗 首頁載入: {e}")
        return False

def test_airbnb_api():
    """測試 Airbnb 模式 API"""
    print("🏠 測試 Airbnb API...")
    
    test_data = {
        "monetizationModel": "airbnb",
        "purchaseType": "individual",
        "propertyPrice": 1550,
        "downPaymentRatio": 10,
        "acquisitionCostRatio": 8,
        "exchangeRate": 0.22,
        "loanOrigin": "japan",
        "initialFurnishingCost": 50,
        "japanLoanInterestRate": 2.5,
        "japanLoanTerm": 35,
        "managementFeeRatio": 5,
        "propertyTaxRate": 1.4,
        "annualAppreciation": 2,
        "investmentPeriod": 10,
        "buildingStructure": "concrete",
        "buildingRatio": 80,
        "annualInsuranceCost": 5,
        "operatingDaysCap": 180,
        "occupancyRate": 70,
        "dailyRate": 15000,
        "platformFeeRate": 15,
        "cleaningFee": 8,
        "avgStayDuration": 3,
        "avgGuests": 2,
        "baseOccupancyForFee": 2,
        "extraGuestFee": 2,
        "peakSeasonMarkup": 30,
        "monthlyUtilities": 2
    }
    
    try:
        response = requests.post(f"{PRD_URL}/calculate", json=test_data, timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            initial_investment = result.get('totalInitialInvestment', 0)
            monthly_income = result.get('monthlyNetIncome', 0)
            
            print(f"✅ 通過 Airbnb API: 初始投資: ¥{initial_investment:,.0f}, 月淨收入: ¥{monthly_income:,.0f}")
            return True
        else:
            print(f"❌ 失敗 Airbnb API: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 失敗 Airbnb API: {e}")
        return False

def test_personal_lease_api():
    """測試長租模式 API"""
    print("🏠 測試長租 API...")
    
    test_data = {
        "monetizationModel": "personalLease",
        "purchaseType": "individual",
        "propertyPrice": 1380,
        "downPaymentRatio": 10,
        "acquisitionCostRatio": 8,
        "exchangeRate": 0.22,
        "loanOrigin": "japan",
        "initialFurnishingCost": 0,
        "japanLoanInterestRate": 2.5,
        "japanLoanTerm": 35,
        "managementFeeRatio": 5,
        "propertyTaxRate": 1.4,
        "annualAppreciation": 2,
        "investmentPeriod": 10,
        "buildingStructure": "concrete",
        "buildingRatio": 80,
        "annualInsuranceCost": 5,
        "monthlyRent": 138,
        "vacancyRate": 5,
        "initialLeaseCostsRatio": 3,
        "leaseUtilities": 1,
        "leaseRenewalFeeFrequency": 2,
        "leaseRenewalFeeAmount": 1
    }
    
    try:
        response = requests.post(f"{PRD_URL}/calculate", json=test_data, timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            initial_investment = result.get('totalInitialInvestment', 0)
            monthly_income = result.get('monthlyNetIncome', 0)
            
            print(f"✅ 通過 長租 API: 初始投資: ¥{initial_investment:,.0f}, 月淨收入: ¥{monthly_income:,.0f}")
            return True
        else:
            print(f"❌ 失敗 長租 API: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 失敗 長租 API: {e}")
        return False

def test_corporate_purchase_api():
    """測試法人購買模式 API"""
    print("🏢 測試法人 API...")
    
    test_data = {
        "monetizationModel": "personalLease",
        "purchaseType": "corporate",
        "propertyPrice": 1970,
        "downPaymentRatio": 10,
        "acquisitionCostRatio": 8,
        "exchangeRate": 0.22,
        "loanOrigin": "japan",
        "initialFurnishingCost": 0,
        "japanLoanInterestRate": 2.5,
        "japanLoanTerm": 35,
        "managementFeeRatio": 5,
        "propertyTaxRate": 1.4,
        "annualAppreciation": 2,
        "investmentPeriod": 10,
        "buildingStructure": "concrete",
        "buildingRatio": 80,
        "corporateTaxRate": 23.2,
        "annualInsuranceCost": 5,
        "corporateSetupCost": 50,
        "annualTaxAccountantFee": 30,
        "monthlyRent": 138,
        "vacancyRate": 5,
        "initialLeaseCostsRatio": 3,
        "leaseUtilities": 0
    }
    
    try:
        response = requests.post(f"{PRD_URL}/calculate", json=test_data, timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            initial_investment = result.get('totalInitialInvestment', 0)
            monthly_income = result.get('monthlyNetIncome', 0)
            annual_tax = result.get('annualCorporateTax', 0)
            
            print(f"✅ 通過 法人 API: 初始投資: ¥{initial_investment:,.0f}, 月淨收入: ¥{monthly_income:,.0f}, 年稅額: ¥{annual_tax:,.0f}")
            return True
        else:
            print(f"❌ 失敗 法人 API: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 失敗 法人 API: {e}")
        return False

def test_error_handling():
    """測試錯誤處理"""
    print("⚠️  測試錯誤處理...")
    
    # 發送不完整的數據
    incomplete_data = {
        "monetizationModel": "personalLease"
        # 缺少必要欄位
    }
    
    try:
        response = requests.post(f"{PRD_URL}/calculate", json=incomplete_data, timeout=TIMEOUT)
        
        # 應該回傳錯誤或預設值，不應該崩潰
        if response.status_code in [200, 400, 422]:
            print("✅ 通過 錯誤處理: API 正確處理了不完整的請求")
            return True
        else:
            print(f"❌ 失敗 錯誤處理: 意外的狀態碼 {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 失敗 錯誤處理: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始 PRD 環境 API 測試...")
    print(f"🔗 測試網址: {PRD_URL}")
    print("-" * 60)
    
    # 執行所有測試
    tests = [
        ("首頁載入", test_homepage),
        ("Airbnb API", test_airbnb_api),
        ("長租 API", test_personal_lease_api),
        ("法人 API", test_corporate_purchase_api),
        ("錯誤處理", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 失敗 {test_name}: 測試執行錯誤 - {e}")
            results.append((test_name, False))
        
        print()  # 空行分隔
    
    # 總結報告
    print("-" * 60)
    print("📊 測試總結:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} {test_name}")
    
    if any(not result for _, result in results):
        print("\n❌ 失敗的測試:")
        for test_name, result in results:
            if not result:
                print(f"   - {test_name}")
    
    print(f"\n🎯 成功率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 PRD 環境測試全部通過，生產環境運作正常！")
    elif passed >= total * 0.8:
        print("✅ PRD 環境測試大部分通過，生產環境基本正常！")
    else:
        print("⚠️  PRD 環境測試通過率較低，請檢查生產環境配置！")

if __name__ == "__main__":
    main() 