#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRD 環境 GA 追蹤設定腳本
幫助設定 PRD 環境的獨立 GA 追蹤 ID
"""

import re
import sys

def update_cloudbuild_production(new_ga_id):
    """更新 cloudbuild-production.yaml 中的 GA 追蹤 ID"""
    print(f"🔧 更新 cloudbuild-production.yaml...")
    
    try:
        # 讀取檔案
        with open('cloudbuild-production.yaml', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替換 GA 追蹤 ID
        old_pattern = r'GA_TRACKING_ID=G-[A-Z0-9]+'
        new_value = f'GA_TRACKING_ID={new_ga_id}'
        
        updated_content = re.sub(old_pattern, new_value, content)
        
        # 寫回檔案
        with open('cloudbuild-production.yaml', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ 已更新 cloudbuild-production.yaml")
        print(f"   舊值: GA_TRACKING_ID=G-59XMZ0SZ0G")
        print(f"   新值: GA_TRACKING_ID={new_ga_id}")
        return True
        
    except Exception as e:
        print(f"❌ 更新失敗: {e}")
        return False

def update_test_prd_ga(new_ga_id):
    """更新測試檔案中的 GA 追蹤 ID"""
    print(f"🔧 更新 test_prd_ga.py...")
    
    try:
        # 讀取檔案
        with open('test_prd_ga.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替換 GA 追蹤 ID
        old_pattern = r'PRD_GA_TRACKING_ID = "G-[A-Z0-9]+"'
        new_value = f'PRD_GA_TRACKING_ID = "{new_ga_id}"'
        
        updated_content = re.sub(old_pattern, new_value, content)
        
        # 寫回檔案
        with open('test_prd_ga.py', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ 已更新 test_prd_ga.py")
        return True
        
    except Exception as e:
        print(f"❌ 更新失敗: {e}")
        return False

def update_config_py(new_ga_id):
    """更新 config.py 中的生產環境 GA ID"""
    print(f"🔧 更新 config.py...")
    
    try:
        # 讀取檔案
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替換生產環境的 GA 追蹤 ID
        old_pattern = r"'production': \{[^}]*'ga_tracking_id': '[^']*'"
        
        # 找到生產環境區塊並替換
        lines = content.split('\n')
        in_production_block = False
        
        for i, line in enumerate(lines):
            if "'production': {" in line:
                in_production_block = True
            elif in_production_block and "'ga_tracking_id':" in line:
                lines[i] = re.sub(r"'ga_tracking_id': '[^']*'", f"'ga_tracking_id': '{new_ga_id}'", line)
                break
        
        updated_content = '\n'.join(lines)
        
        # 寫回檔案
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ 已更新 config.py")
        return True
        
    except Exception as e:
        print(f"❌ 更新失敗: {e}")
        return False

def validate_ga_id(ga_id):
    """驗證 GA 追蹤 ID 格式"""
    pattern = r'^G-[A-Z0-9]{10}$'
    return re.match(pattern, ga_id) is not None

def show_next_steps():
    """顯示後續步驟"""
    print("\n🚀 後續部署步驟:")
    print("=" * 50)
    print("1. 提交更改到 Git:")
    print("   git add .")
    print("   git commit -m \"feat: 設定 PRD 環境獨立 GA 追蹤 ID\"")
    print("   git push origin main")
    print("")
    print("2. 觸發 PRD 環境部署:")
    print("   - Git 推送會自動觸發 Cloud Build")
    print("   - 或手動在 Google Cloud Console 觸發部署")
    print("")
    print("3. 驗證部署:")
    print("   python test_prd_ga.py")
    print("")
    print("4. 在 Google Analytics 中設定新屬性:")
    print("   - 創建新的 GA4 屬性")
    print("   - 配置資料流")
    print("   - 設定目標和轉換")

def main():
    """主函數"""
    print("🚀 PRD 環境 GA 追蹤設定助手")
    print("=" * 50)
    
    # 檢查當前狀況
    print("📊 當前狀況:")
    print("   STG 環境: G-59XMZ0SZ0G")
    print("   PRD 環境: G-59XMZ0SZ0G (與 STG 相同)")
    print("")
    print("🎯 建議設定:")
    print("   為 PRD 環境設定獨立的 GA 追蹤 ID")
    print("   這樣可以完全分離 STG 和 PRD 的追蹤資料")
    print("")
    
    # 獲取用戶輸入
    while True:
        print("請選擇操作:")
        print("1. 設定新的 PRD GA 追蹤 ID")
        print("2. 保持當前設定（使用相同的 GA ID）")
        print("3. 退出")
        
        choice = input("\n請輸入選項 (1-3): ").strip()
        
        if choice == "1":
            # 設定新的 GA ID
            while True:
                new_ga_id = input("\n請輸入 PRD 環境的 GA 追蹤 ID (格式: G-XXXXXXXXXX): ").strip()
                
                if validate_ga_id(new_ga_id):
                    break
                else:
                    print("❌ GA 追蹤 ID 格式錯誤，請使用 G-XXXXXXXXXX 格式")
            
            print(f"\n🔧 開始設定 PRD 環境 GA 追蹤 ID: {new_ga_id}")
            print("-" * 50)
            
            # 更新各個檔案
            success_count = 0
            total_updates = 3
            
            if update_cloudbuild_production(new_ga_id):
                success_count += 1
            
            if update_test_prd_ga(new_ga_id):
                success_count += 1
            
            if update_config_py(new_ga_id):
                success_count += 1
            
            # 總結
            print(f"\n📊 更新總結: {success_count}/{total_updates} 個檔案成功更新")
            
            if success_count == total_updates:
                print("🎉 所有檔案更新成功！")
                show_next_steps()
            else:
                print("⚠️  部分檔案更新失敗，請手動檢查")
            
            break
            
        elif choice == "2":
            print("\n📝 保持當前設定")
            print("STG 和 PRD 環境將繼續使用相同的 GA 追蹤 ID: G-59XMZ0SZ0G")
            print("您可以在 GA 控制台中通過環境標籤來區分資料")
            break
            
        elif choice == "3":
            print("\n👋 退出設定")
            break
            
        else:
            print("❌ 無效選項，請重新選擇")

if __name__ == "__main__":
    main() 