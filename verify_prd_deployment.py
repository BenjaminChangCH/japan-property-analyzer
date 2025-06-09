#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRD 部署驗證腳本
驗證 PRD 環境 GA 追蹤 ID 部署是否成功
"""

import requests
import re
import time

PRD_URL = "https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app"
EXPECTED_GA_ID = "G-94SVDFL5YN"
OLD_GA_ID = "G-59XMZ0SZ0G"

def verify_prd_deployment():
    """驗證 PRD 部署狀況"""
    print("🔍 驗證 PRD 環境部署狀況...")
    print(f"🎯 期望的 GA 追蹤 ID: {EXPECTED_GA_ID}")
    print("=" * 60)
    
    try:
        response = requests.get(PRD_URL, timeout=10)
        html_content = response.text
        
        # 檢查新的 GA 追蹤 ID
        if EXPECTED_GA_ID in html_content:
            print(f"✅ 新的 GA 追蹤 ID 已部署: {EXPECTED_GA_ID}")
            new_ga_deployed = True
        else:
            print(f"❌ 新的 GA 追蹤 ID 尚未部署: {EXPECTED_GA_ID}")
            new_ga_deployed = False
        
        # 檢查舊的 GA 追蹤 ID 是否還存在
        if OLD_GA_ID in html_content:
            print(f"⚠️  舊的 GA 追蹤 ID 仍存在: {OLD_GA_ID}")
            old_ga_exists = True
        else:
            print(f"✅ 舊的 GA 追蹤 ID 已移除: {OLD_GA_ID}")
            old_ga_exists = False
        
        # 檢查環境標識
        if "environment: 'production'" in html_content:
            print("✅ 環境標識正確: production")
            env_correct = True
        else:
            print("❌ 環境標識錯誤")
            env_correct = False
        
        # 檢查除錯模式
        if "debug_mode: true" in html_content:
            print("⚠️  警告: PRD 環境仍啟用除錯模式")
            debug_off = False
        else:
            print("✅ PRD 環境正確關閉除錯模式")
            debug_off = True
        
        # 總結
        print("\n" + "=" * 60)
        print("📊 部署驗證結果:")
        
        if new_ga_deployed and not old_ga_exists and env_correct and debug_off:
            print("🎉 PRD 環境部署完全成功！")
            print(f"✅ 新 GA 追蹤 ID: {EXPECTED_GA_ID}")
            print("✅ 舊 GA 追蹤 ID 已清除")
            print("✅ 環境配置正確")
            return True
        elif new_ga_deployed and env_correct:
            print("✅ PRD 環境部署基本成功")
            print("⚠️  但有部分問題需要注意")
            return True
        else:
            print("❌ PRD 環境部署尚未完成或有問題")
            print("🔄 建議等待幾分鐘後重新檢查")
            return False
    
    except Exception as e:
        print(f"❌ 驗證失敗: {e}")
        return False

def main():
    print("🚀 PRD 環境部署驗證")
    print(f"🔗 檢查網址: {PRD_URL}")
    print(f"📊 預期 GA ID: {EXPECTED_GA_ID}")
    print("")
    
    # 進行驗證
    success = verify_prd_deployment()
    
    if success:
        print("\n🎯 下一步建議:")
        print("1. 運行完整測試: python test_prd_ga.py")
        print("2. 在 Google Analytics 中設定新的 GA4 屬性")
        print("3. 測試實際的事件追蹤功能")
    else:
        print("\n🔄 如果部署尚未完成:")
        print("1. 檢查 Cloud Build 部署狀況")
        print("2. 等待 3-5 分鐘後重新運行此腳本")
        print("3. 確認 GitHub PR 已成功合併")

if __name__ == "__main__":
    main() 