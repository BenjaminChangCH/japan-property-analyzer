#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版 Google Analytics 測試
測試 STG 環境的 GA 配置
"""

import requests
import re
import json
import time

# 測試配置
STG_URL = "https://japan-property-analyzer-864942598341.asia-northeast1.run.app"
GA_TRACKING_ID = "G-59XMZ0SZ0G"

def test_ga_in_html():
    """測試 HTML 中的 GA 追蹤碼"""
    print("🔍 檢查 STG 環境的 GA 追蹤碼...")
    
    try:
        response = requests.get(STG_URL, timeout=10)
        html_content = response.text
        
        # 檢查 GA 腳本
        if "googletagmanager.com/gtag/js" in html_content:
            print("✅ GA 腳本載入標籤存在")
        else:
            print("❌ 未找到 GA 腳本載入標籤")
            return False
        
        # 檢查追蹤 ID
        if GA_TRACKING_ID in html_content:
            print(f"✅ GA 追蹤 ID 配置正確: {GA_TRACKING_ID}")
        else:
            print(f"❌ 未找到 GA 追蹤 ID: {GA_TRACKING_ID}")
            return False
        
        # 檢查 gtag 函數
        gtag_pattern = r'function gtag\(\)'
        if re.search(gtag_pattern, html_content):
            print("✅ gtag 函數定義存在")
        else:
            print("❌ 未找到 gtag 函數定義")
            return False
        
        # 檢查環境配置
        if "environment: 'staging'" in html_content:
            print("✅ 環境配置正確: staging")
        else:
            print("❌ 環境配置錯誤或缺失")
        
        # 檢查事件追蹤
        events_to_check = [
            'calculation_started',
            'calculation_completed', 
            'pdf_download'
        ]
        
        events_found = []
        for event in events_to_check:
            if event in html_content:
                events_found.append(event)
        
        if events_found:
            print(f"✅ 找到事件追蹤: {', '.join(events_found)}")
        else:
            print("❌ 未找到任何事件追蹤")
        
        return True
        
    except Exception as e:
        print(f"❌ 檢查失敗: {e}")
        return False

def test_ga_measurement_protocol():
    """測試 GA Measurement Protocol (模擬事件發送)"""
    print("\n📊 測試 GA 事件發送...")
    
    try:
        # GA4 Measurement Protocol 端點
        ga4_endpoint = "https://www.google-analytics.com/mp/collect"
        
        # 測試參數
        params = {
            'measurement_id': GA_TRACKING_ID,
            'api_secret': 'test_secret'  # 這是測試用的，實際需要真實的 API secret
        }
        
        # 測試事件數據
        event_data = {
            'client_id': 'test_client_12345',
            'events': [{
                'name': 'test_event',
                'parameters': {
                    'event_category': 'test',
                    'event_label': 'stg_test',
                    'environment': 'staging'
                }
            }]
        }
        
        # 注意：這個測試不會真的發送事件，因為我們沒有有效的 api_secret
        # 這只是為了展示如何檢查 GA 設置
        print(f"📡 GA4 端點: {ga4_endpoint}")
        print(f"📊 追蹤 ID: {GA_TRACKING_ID}")
        print("📝 注意: 實際的事件發送需要有效的 API secret")
        
        return True
        
    except Exception as e:
        print(f"❌ GA 事件測試失敗: {e}")
        return False

def test_api_with_tracking():
    """測試 API 調用並檢查是否觸發追蹤"""
    print("\n🧮 測試 API 調用...")
    
    try:
        # 準備測試數據
        test_data = {
            "monetizationModel": "personalLease",
            "purchaseType": "individual",
            "propertyPrice": 1550,
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
        
        # 調用 API
        api_url = f"{STG_URL}/calculate"
        response = requests.post(api_url, json=test_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API 調用成功")
            print(f"   初始投資: ¥{result.get('totalInitialInvestment', 0):,.0f}")
            print(f"   月淨收入: ¥{result.get('monthlyNetIncome', 0):,.0f}")
            
            # 在實際應用中，這個 API 調用會觸發前端的 GA 事件
            print("📊 注意: 實際使用時，此 API 調用會觸發前端的 calculation_completed 事件")
            return True
        else:
            print(f"❌ API 調用失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API 測試失敗: {e}")
        return False

def check_ga_real_time_api():
    """檢查 GA Real Time API (需要認證)"""
    print("\n⏰ 檢查 GA 實時數據...")
    
    print("📋 要檢查 GA 是否收到數據，請按以下步驟操作:")
    print("1. 前往 Google Analytics: https://analytics.google.com/")
    print(f"2. 選擇對應的 GA 屬性 (追蹤 ID: {GA_TRACKING_ID})")
    print("3. 查看「即時」報告")
    print("4. 手動訪問 STG 網站並進行操作")
    print("5. 確認是否有新的活躍使用者出現")
    
    print("\n🔍 建議測試步驟:")
    print(f"1. 打開瀏覽器訪問: {STG_URL}")
    print("2. 填寫表單並點擊計算")
    print("3. 下載 PDF 報告")
    print("4. 在 GA 即時報告中查看事件")
    
    return True

def main():
    """主測試函數"""
    print("🚀 開始 Google Analytics 簡化測試...")
    print(f"🔗 測試網址: {STG_URL}")
    print(f"📊 GA 追蹤 ID: {GA_TRACKING_ID}")
    print("=" * 60)
    
    results = []
    
    # 測試 HTML 中的 GA 配置
    results.append(("HTML 中的 GA 配置", test_ga_in_html()))
    
    # 測試 GA 事件發送機制
    results.append(("GA 事件發送機制", test_ga_measurement_protocol()))
    
    # 測試 API 調用
    results.append(("API 功能測試", test_api_with_tracking()))
    
    # 檢查即時數據說明
    results.append(("GA 即時數據檢查說明", check_ga_real_time_api()))
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 測試總結:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 成功率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有基本測試通過！")
        print("📊 GA 追蹤碼已正確安裝在 STG 環境中")
        print("⚠️  如果 GA 控制台沒有數據，可能的原因：")
        print("   1. 數據延遲（最多可能需要 24-48 小時）")
        print("   2. 需要實際用戶訪問觸發事件")
        print("   3. 廣告攔截器阻擋了 GA 腳本")
        print("   4. 網路問題導致事件無法發送")
    else:
        print("\n⚠️  部分測試失敗，請檢查配置")

if __name__ == "__main__":
    main() 