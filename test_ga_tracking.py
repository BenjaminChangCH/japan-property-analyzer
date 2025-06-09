#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Analytics 追蹤測試腳本
測試 STG 環境的 GA 配置與事件追蹤
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 測試配置
STG_URL = "https://japan-property-analyzer-864942598341.asia-northeast1.run.app"
GA_TRACKING_ID = "G-59XMZ0SZ0G"

def setup_driver():
    """設置 Chrome 瀏覽器驅動"""
    options = Options()
    options.add_argument('--headless')  # 無頭模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def test_ga_installation():
    """測試 GA 追蹤碼是否正確安裝"""
    print("🔍 測試 GA 追蹤碼安裝...")
    
    driver = setup_driver()
    try:
        driver.get(STG_URL)
        time.sleep(3)
        
        # 檢查 GA 腳本是否載入
        ga_scripts = driver.find_elements(By.CSS_SELECTOR, "script[src*='googletagmanager.com/gtag/js']")
        if ga_scripts:
            print(f"✅ GA 腳本已載入: {len(ga_scripts)} 個")
        else:
            print("❌ 未找到 GA 腳本")
            return False
        
        # 檢查 gtag 函數是否存在
        gtag_exists = driver.execute_script("return typeof gtag !== 'undefined';")
        if gtag_exists:
            print("✅ gtag 函數存在")
        else:
            print("❌ gtag 函數不存在")
            return False
        
        # 檢查追蹤 ID
        ga_config = driver.execute_script("""
            var gaConfig = null;
            if (window.dataLayer) {
                for (var i = 0; i < window.dataLayer.length; i++) {
                    if (window.dataLayer[i][0] === 'config' && window.dataLayer[i][1] === arguments[0]) {
                        gaConfig = window.dataLayer[i];
                        break;
                    }
                }
            }
            return gaConfig;
        """, GA_TRACKING_ID)
        
        if ga_config:
            print(f"✅ GA 配置正確: {GA_TRACKING_ID}")
            print(f"   配置詳情: {ga_config}")
        else:
            print(f"❌ 未找到 GA 配置: {GA_TRACKING_ID}")
            return False
        
        # 檢查環境變數
        page_source = driver.page_source
        if 'environment: \'staging\'' in page_source:
            print("✅ 環境設定正確: staging")
        else:
            print("❌ 環境設定錯誤")
        
        return True
        
    except Exception as e:
        print(f"❌ GA 安裝測試失敗: {e}")
        return False
    finally:
        driver.quit()

def test_ga_events():
    """測試 GA 事件追蹤"""
    print("\n📊 測試 GA 事件追蹤...")
    
    driver = setup_driver()
    try:
        driver.get(STG_URL)
        time.sleep(3)
        
        # 檢查是否有 dataLayer
        data_layer_exists = driver.execute_script("return typeof window.dataLayer !== 'undefined';")
        if not data_layer_exists:
            print("❌ dataLayer 不存在")
            return False
        
        # 獲取初始的 dataLayer 內容
        initial_events = driver.execute_script("return window.dataLayer.length;")
        print(f"📋 初始事件數量: {initial_events}")
        
        # 檢查頁面載入事件
        page_view_events = driver.execute_script("""
            var events = [];
            if (window.dataLayer) {
                for (var i = 0; i < window.dataLayer.length; i++) {
                    var event = window.dataLayer[i];
                    if (event && (event[0] === 'event' || event.event)) {
                        events.push(event);
                    }
                }
            }
            return events;
        """)
        
        print(f"📈 找到的事件: {len(page_view_events)}")
        for i, event in enumerate(page_view_events):
            print(f"   事件 {i+1}: {event}")
        
        # 模擬觸發計算開始事件
        driver.execute_script("""
            if (typeof gtag !== 'undefined') {
                gtag('event', 'calculation_started', {
                    'event_category': 'engagement',
                    'event_label': 'test_trigger'
                });
            }
        """)
        
        time.sleep(1)
        
        # 檢查新增的事件
        final_events = driver.execute_script("return window.dataLayer.length;")
        print(f"📋 最終事件數量: {final_events}")
        
        if final_events > initial_events:
            print("✅ 成功觸發自定義事件")
            return True
        else:
            print("❌ 未能觸發自定義事件")
            return False
        
    except Exception as e:
        print(f"❌ GA 事件測試失敗: {e}")
        return False
    finally:
        driver.quit()

def test_network_requests():
    """測試 GA 網路請求"""
    print("\n🌐 測試 GA 網路請求...")
    
    driver = setup_driver()
    try:
        # 啟用網路日誌
        driver.execute_cdp_cmd('Network.enable', {})
        
        # 收集網路請求
        network_requests = []
        
        def capture_request(message):
            if message['method'] == 'Network.requestWillBeSent':
                url = message['params']['request']['url']
                if 'google-analytics.com' in url or 'googletagmanager.com' in url:
                    network_requests.append(url)
        
        driver.add_cdp_listener('Network.requestWillBeSent', capture_request)
        
        driver.get(STG_URL)
        time.sleep(5)  # 等待所有請求完成
        
        print(f"📡 找到 GA 相關請求: {len(network_requests)}")
        for i, req in enumerate(network_requests):
            print(f"   請求 {i+1}: {req[:100]}...")
        
        return len(network_requests) > 0
        
    except Exception as e:
        print(f"❌ 網路請求測試失敗: {e}")
        return False
    finally:
        driver.quit()

def main():
    """主測試函數"""
    print("🚀 開始 Google Analytics 追蹤測試...")
    print(f"🔗 測試網址: {STG_URL}")
    print(f"📊 GA 追蹤 ID: {GA_TRACKING_ID}")
    print("=" * 60)
    
    results = []
    
    # 測試 GA 安裝
    results.append(("GA 追蹤碼安裝", test_ga_installation()))
    
    # 測試 GA 事件
    results.append(("GA 事件追蹤", test_ga_events()))
    
    # 測試網路請求
    try:
        results.append(("GA 網路請求", test_network_requests()))
    except Exception as e:
        print(f"❌ 網路請求測試跳過: {e}")
        results.append(("GA 網路請求", False))
    
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
        print("🎉 所有 GA 測試通過！")
    else:
        print("⚠️  部分 GA 測試失敗，請檢查配置")

if __name__ == "__main__":
    main() 