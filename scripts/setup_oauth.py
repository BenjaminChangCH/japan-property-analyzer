#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google OAuth 設定腳本
幫助配置 STG 和 PRD 環境的 Google OAuth 環境變數
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """執行命令並處理錯誤"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失敗: {e.stderr}")
        return None

def check_gcloud_auth():
    """檢查 gcloud 認證狀態"""
    print("🔍 檢查 Google Cloud 認證狀態...")
    
    result = run_command("gcloud auth list --filter=status:ACTIVE --format='value(account)'", "檢查認證帳號")
    if result:
        print(f"✅ 已認證帳號: {result}")
        return True
    else:
        print("❌ 未找到已認證的 Google Cloud 帳號")
        print("請先執行: gcloud auth login")
        return False

def get_oauth_credentials():
    """獲取 Google OAuth 憑證"""
    print("\n📋 Google OAuth 憑證設定")
    print("=" * 50)
    print("請前往 Google Cloud Console > API 和服務 > 憑證")
    print("找到您的 OAuth 2.0 用戶端 ID 憑證")
    print("")
    
    client_id = input("請輸入 Google Client ID: ").strip()
    if not client_id:
        print("❌ Client ID 不能為空")
        return None, None
    
    client_secret = input("請輸入 Google Client Secret: ").strip()
    if not client_secret:
        print("❌ Client Secret 不能為空")
        return None, None
    
    return client_id, client_secret

def generate_secret_key():
    """生成 Flask SECRET_KEY"""
    import secrets
    return secrets.token_hex(32)

def update_stg_environment(client_id, client_secret):
    """更新 STG 環境變數"""
    print("\n🧪 更新 STG 環境變數...")
    
    secret_key = generate_secret_key()
    
    env_vars = [
        f"GA_TRACKING_ID=G-59XMZ0SZ0G",
        f"ENVIRONMENT=staging",
        f"NO_INDEX=true",
        f"SECRET_KEY={secret_key}",
        f"GOOGLE_CLIENT_ID={client_id}",
        f"GOOGLE_CLIENT_SECRET={client_secret}"
    ]
    
    env_vars_str = ",".join(env_vars)
    
    command = f"""gcloud run services update japan-property-analyzer \\
        --region=asia-northeast1 \\
        --set-env-vars="{env_vars_str}" """
    
    result = run_command(command, "更新 STG 環境變數")
    return result is not None

def update_prd_environment(client_id, client_secret):
    """更新 PRD 環境變數"""
    print("\n🚀 更新 PRD 環境變數...")
    
    secret_key = generate_secret_key()
    
    env_vars = [
        f"GA_TRACKING_ID=G-94SVDFL5YN",
        f"ENVIRONMENT=production",
        f"NO_INDEX=false",
        f"SECRET_KEY={secret_key}",
        f"GOOGLE_CLIENT_ID={client_id}",
        f"GOOGLE_CLIENT_SECRET={client_secret}"
    ]
    
    env_vars_str = ",".join(env_vars)
    
    command = f"""gcloud run services update japan-property-analyzer-prod \\
        --region=asia-northeast1 \\
        --set-env-vars="{env_vars_str}" """
    
    result = run_command(command, "更新 PRD 環境變數")
    return result is not None

def update_cloudbuild_configs(client_id, client_secret):
    """更新 Cloud Build 配置檔案"""
    print("\n📝 更新 Cloud Build 配置檔案...")
    
    # 更新 STG 配置
    stg_config_path = Path("deployment/cloudbuild-staging.yaml")
    if stg_config_path.exists():
        with open(stg_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替換環境變數
        content = content.replace(
            "GOOGLE_CLIENT_ID=864942598341-your-client-id.googleusercontent.com",
            f"GOOGLE_CLIENT_ID={client_id}"
        )
        content = content.replace(
            "GOOGLE_CLIENT_SECRET=your-client-secret-here",
            f"GOOGLE_CLIENT_SECRET={client_secret}"
        )
        
        with open(stg_config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ STG Cloud Build 配置已更新")
    
    # 更新 PRD 配置
    prd_config_path = Path("deployment/cloudbuild-production.yaml")
    if prd_config_path.exists():
        with open(prd_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替換環境變數
        content = content.replace(
            "GOOGLE_CLIENT_ID=864942598341-your-client-id.googleusercontent.com",
            f"GOOGLE_CLIENT_ID={client_id}"
        )
        content = content.replace(
            "GOOGLE_CLIENT_SECRET=your-client-secret-here",
            f"GOOGLE_CLIENT_SECRET={client_secret}"
        )
        
        with open(prd_config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ PRD Cloud Build 配置已更新")

def verify_oauth_setup():
    """驗證 OAuth 設定"""
    print("\n🧪 驗證 OAuth 設定...")
    
    # 測試 STG 環境
    stg_url = "https://japan-property-analyzer-864942598341.asia-northeast1.run.app/auth/login"
    print(f"📍 STG 登入測試: {stg_url}")
    
    # 測試 PRD 環境
    prd_url = "https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app/auth/login"
    print(f"📍 PRD 登入測試: {prd_url}")
    
    print("\n✅ 請手動測試以上網址的 Google 登入功能")

def create_env_file(client_id, client_secret):
    """創建本地 .env 檔案"""
    print("\n📄 創建本地 .env 檔案...")
    
    secret_key = generate_secret_key()
    
    env_content = f"""# Google OAuth 2.0 設定
GOOGLE_CLIENT_ID={client_id}
GOOGLE_CLIENT_SECRET={client_secret}

# Flask 應用程式密鑰
SECRET_KEY={secret_key}

# 資料庫設定
DATABASE_URL=sqlite:///app.db

# Google Analytics 4 追蹤 ID (本地開發不需要)
GA_TRACKING_ID=

# 環境標識
ENVIRONMENT=development

# GCP 專案設定
GCP_PROJECT_ID=japan-property-analyzer
GCP_REGION=asia-northeast1
CLOUD_RUN_SERVICE_NAME=japan-property-analyzer
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ .env 檔案已創建")

def main():
    """主函數"""
    print("🚀 Google OAuth 設定助手")
    print("=" * 60)
    print("此腳本將幫助您設定 STG 和 PRD 環境的 Google OAuth 憑證")
    print("")
    
    # 檢查 gcloud 認證
    if not check_gcloud_auth():
        sys.exit(1)
    
    # 獲取 OAuth 憑證
    client_id, client_secret = get_oauth_credentials()
    if not client_id or not client_secret:
        sys.exit(1)
    
    print(f"\n📋 設定摘要:")
    print(f"Client ID: {client_id}")
    print(f"Client Secret: {'*' * len(client_secret)}")
    print("")
    
    # 確認設定
    confirm = input("確認要使用這些憑證設定環境嗎？(y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ 設定已取消")
        sys.exit(0)
    
    print("\n🔧 開始設定環境...")
    print("-" * 60)
    
    success_count = 0
    total_tasks = 4
    
    # 更新 STG 環境
    if update_stg_environment(client_id, client_secret):
        success_count += 1
    
    # 更新 PRD 環境
    if update_prd_environment(client_id, client_secret):
        success_count += 1
    
    # 更新 Cloud Build 配置
    try:
        update_cloudbuild_configs(client_id, client_secret)
        success_count += 1
    except Exception as e:
        print(f"❌ 更新 Cloud Build 配置失敗: {e}")
    
    # 創建本地 .env 檔案
    try:
        create_env_file(client_id, client_secret)
        success_count += 1
    except Exception as e:
        print(f"❌ 創建 .env 檔案失敗: {e}")
    
    # 總結
    print(f"\n📊 設定總結: {success_count}/{total_tasks} 項任務完成")
    print("=" * 60)
    
    if success_count == total_tasks:
        print("🎉 所有設定完成！")
        verify_oauth_setup()
        
        print("\n📋 後續步驟:")
        print("1. 提交 Cloud Build 配置變更到 Git")
        print("2. 推送到 feature branch 觸發 STG 部署")
        print("3. 測試 STG 環境的 Google 登入功能")
        print("4. 創建 PR 並合併到 main 分支")
        print("5. 測試 PRD 環境的 Google 登入功能")
    else:
        print("⚠️ 部分設定失敗，請檢查錯誤訊息並重新執行")

if __name__ == "__main__":
    main() 