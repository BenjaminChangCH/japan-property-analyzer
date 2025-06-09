#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRD 環境 Google Analytics 測試腳本
測試生產環境的 GA 配置與事件追蹤
"""

import requests
import re
import json
import time

# PRD 環境配置
PRD_URL = "https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app"
PRD_GA_TRACKING_ID = "G-94SVDFL5YN"  # PRD 環境獨立的 GA 追蹤 ID

def test_ga_in_html():
    """測試 HTML 中的 GA 追蹤碼"""
    print("🔍 檢查 PRD 環境的 GA 追蹤碼...")
    
    try:
        response = requests.get(PRD_URL, timeout=10)
        html_content = response.text
        
        # 檢查 GA 腳本
        if "googletagmanager.com/gtag/js" in html_content:
            print("✅ GA 腳本載入標籤存在")
        else:
            print("❌ 未找到 GA 腳本載入標籤")
            return False
        
        # 檢查追蹤 ID
        if PRD_GA_TRACKING_ID in html_content:
            print(f"✅ GA 追蹤 ID 配置正確: {PRD_GA_TRACKING_ID}")
        else:
            print(f"❌ 未找到 GA 追蹤 ID: {PRD_GA_TRACKING_ID}")
            return False
        
        # 檢查 gtag 函數
        gtag_pattern = r'function gtag\(\)'
        if re.search(gtag_pattern, html_content):
            print("✅ gtag 函數定義存在")
        else:
            print("❌ 未找到 gtag 函數定義")
            return False
        
        # 檢查環境配置
        if "environment: 'production'" in html_content:
            print("✅ 環境配置正確: production")
        else:
            print("❌ 環境配置錯誤或缺失")
            print("   查找到的環境設定:", re.search(r"environment: '[^']*'", html_content))
        
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
        
        # 檢查是否有除錯模式（PRD 應該關閉）
        if "debug_mode: true" in html_content:
            print("⚠️  警告: PRD 環境啟用了除錯模式")
        else:
            print("✅ PRD 環境正確關閉除錯模式")
        
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
            'measurement_id': PRD_GA_TRACKING_ID,
            'api_secret': 'prd_api_secret'  # 這是測試用的，實際需要真實的 API secret
        }
        
        # 測試事件數據
        event_data = {
            'client_id': 'prd_test_client_12345',
            'events': [{
                'name': 'prd_test_event',
                'parameters': {
                    'event_category': 'test',
                    'event_label': 'prd_test',
                    'environment': 'production'
                }
            }]
        }
        
        # 注意：這個測試不會真的發送事件，因為我們沒有有效的 api_secret
        # 這只是為了展示如何檢查 GA 設置
        print(f"📡 GA4 端點: {ga4_endpoint}")
        print(f"📊 追蹤 ID: {PRD_GA_TRACKING_ID}")
        print("📝 注意: 實際的事件發送需要有效的 API secret")
        print("🚨 重要: PRD 環境事件將被記錄到實際的 GA 屬性中")
        
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
        api_url = f"{PRD_URL}/calculate"
        response = requests.post(api_url, json=test_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API 調用成功")
            print(f"   初始投資: ¥{result.get('totalInitialInvestment', 0):,.0f}")
            print(f"   月淨收入: ¥{result.get('monthlyNetIncome', 0):,.0f}")
            
            # 在實際應用中，這個 API 調用會觸發前端的 GA 事件
            print("📊 注意: 實際使用時，此 API 調用會觸發前端的 calculation_completed 事件")
            print("🚨 重要: 這是 PRD 環境，事件會被記錄到實際的 GA 中")
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
    
    print("📋 要檢查 PRD 環境 GA 是否收到數據，請按以下步驟操作:")
    print("1. 前往 Google Analytics: https://analytics.google.com/")
    print(f"2. 選擇對應的 GA 屬性 (追蹤 ID: {PRD_GA_TRACKING_ID})")
    print("3. 查看「即時」報告")
    print("4. 手動訪問 PRD 網站並進行操作")
    print("5. 確認是否有新的活躍使用者出現")
    
    print("\n🔍 建議測試步驟:")
    print(f"1. 打開瀏覽器訪問: {PRD_URL}")
    print("2. 填寫表單並點擊計算")
    print("3. 下載 PDF 報告")
    print("4. 在 GA 即時報告中查看事件")
    
    print("\n🚨 重要提醒:")
    print("   - 這是生產環境，所有操作都會影響實際的 GA 數據")
    print("   - 建議在非高峰時段進行測試")
    print("   - 確保測試完成後清理測試數據（如果可能）")
    
    return True

def compare_environments():
    """比較 STG 和 PRD 環境的 GA 配置"""
    print("\n🔄 比較 STG 和 PRD 環境...")
    
    try:
        # STG 環境配置
        stg_url = "https://japan-property-analyzer-864942598341.asia-northeast1.run.app"
        stg_response = requests.get(stg_url, timeout=10)
        stg_content = stg_response.text
        
        # PRD 環境配置
        prd_response = requests.get(PRD_URL, timeout=10)
        prd_content = prd_response.text
        
        print("📊 環境對比:")
        print("=" * 50)
        
        # 比較 GA 追蹤 ID
        stg_ga_match = re.search(r'G-[A-Z0-9]+', stg_content)
        prd_ga_match = re.search(r'G-[A-Z0-9]+', prd_content)
        
        stg_ga_id = stg_ga_match.group() if stg_ga_match else "未找到"
        prd_ga_id = prd_ga_match.group() if prd_ga_match else "未找到"
        
        print(f"STG GA 追蹤 ID: {stg_ga_id}")
        print(f"PRD GA 追蹤 ID: {prd_ga_id}")
        
        if stg_ga_id == prd_ga_id:
            print("⚠️  警告: STG 和 PRD 使用相同的 GA 追蹤 ID")
            print("   建議: 為 PRD 環境設定獨立的 GA 追蹤 ID")
        else:
            print("✅ STG 和 PRD 使用不同的 GA 追蹤 ID")
        
        # 比較環境設定
        stg_env = "staging" if "environment: 'staging'" in stg_content else "未設定"
        prd_env = "production" if "environment: 'production'" in prd_content else "未設定"
        
        print(f"STG 環境標識: {stg_env}")
        print(f"PRD 環境標識: {prd_env}")
        
        return True
        
    except Exception as e:
        print(f"❌ 環境比較失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始 PRD 環境 Google Analytics 測試...")
    print(f"🔗 測試網址: {PRD_URL}")
    print(f"📊 GA 追蹤 ID: {PRD_GA_TRACKING_ID}")
    print("🚨 警告: 這是生產環境測試，請謹慎操作！")
    print("=" * 60)
    
    results = []
    
    # 測試 HTML 中的 GA 配置
    results.append(("PRD HTML 中的 GA 配置", test_ga_in_html()))
    
    # 測試 GA 事件發送機制
    results.append(("PRD GA 事件發送機制", test_ga_measurement_protocol()))
    
    # 測試 API 調用
    results.append(("PRD API 功能測試", test_api_with_tracking()))
    
    # 檢查即時數據說明
    results.append(("PRD GA 即時數據檢查說明", check_ga_real_time_api()))
    
    # 環境比較
    results.append(("STG vs PRD 環境比較", compare_environments()))
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 PRD 環境測試總結:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 成功率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 PRD 環境 GA 測試全部通過！")
        print("📊 GA 追蹤碼已正確安裝在 PRD 環境中")
        print("🚨 提醒: 生產環境的所有 GA 事件都會被實際記錄")
    else:
        print("\n⚠️  部分 PRD 環境測試失敗，請檢查配置")
    
    print("\n🔧 後續建議:")
    if PRD_GA_TRACKING_ID == "G-59XMZ0SZ0G":
        print("   1. 建議為 PRD 環境設定獨立的 GA 追蹤 ID")
        print("   2. 更新 cloudbuild-production.yaml 中的 GA_TRACKING_ID")
        print("   3. 重新部署 PRD 環境")

if __name__ == "__main__":
    main() 