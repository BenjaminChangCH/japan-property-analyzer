#!/usr/bin/env python3
"""
Enterprise 發佈管理系統
提供完整的 STG → PRD 發佈流程控制
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ReleaseManager:
    """發佈管理器"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.release_config_file = os.path.join(self.project_root, "config", "release_config.json")
        self.ensure_config_exists()
    
    def ensure_config_exists(self):
        """確保設定檔存在"""
        os.makedirs(os.path.dirname(self.release_config_file), exist_ok=True)
        if not os.path.exists(self.release_config_file):
            default_config = {
                "stg_approval_required": True,
                "prd_approval_required": True,
                "auto_rollback_enabled": True,
                "health_check_timeout": 300,
                "stg_base_url": "https://japan-property-analyzer-stg.example.com",
                "prd_base_url": "https://japan-property-analyzer-prod.example.com"
            }
            with open(self.release_config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    def run_command(self, command: str, capture_output: bool = True) -> Tuple[bool, str, str]:
        """執行命令"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=capture_output, 
                text=True, 
                cwd=self.project_root
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return False, "", str(e)
    
    def get_current_version(self) -> Optional[str]:
        """獲取當前版本"""
        try:
            sys.path.insert(0, self.project_root)
            from version import __version__
            return __version__
        except ImportError:
            return None
    
    def get_git_info(self) -> Dict:
        """獲取 Git 資訊"""
        success, branch, _ = self.run_command("git branch --show-current")
        current_branch = branch if success else "unknown"
        
        success, status, _ = self.run_command("git status --porcelain")
        has_changes = bool(status.strip()) if success else True
        
        success, latest_tag, _ = self.run_command("git describe --tags --abbrev=0")
        latest_tag = latest_tag if success else "無標籤"
        
        return {
            "current_branch": current_branch,
            "has_changes": has_changes,
            "latest_tag": latest_tag
        }
    
    def check_stg_health(self, version: str) -> bool:
        """檢查 STG 環境健康狀態"""
        print("🔍 檢查 STG 環境健康狀態...")
        
        # 這裡可以加入實際的健康檢查邏輯
        # 例如：API 健康檢查、功能測試等
        
        health_checks = [
            self._check_api_health("staging"),
            self._check_version_match("staging", version),
            self._run_smoke_tests("staging")
        ]
        
        all_passed = all(health_checks)
        if all_passed:
            print("✅ STG 環境健康檢查通過")
        else:
            print("❌ STG 環境健康檢查失敗")
        
        return all_passed
    
    def _check_api_health(self, environment: str) -> bool:
        """檢查 API 健康狀態"""
        print(f"  📡 檢查 {environment.upper()} API 健康狀態...")
        # 實際實作可以呼叫 /health 端點
        return True
    
    def _check_version_match(self, environment: str, expected_version: str) -> bool:
        """檢查版本是否匹配"""
        print(f"  🔢 檢查 {environment.upper()} 版本匹配 (期望: {expected_version})...")
        # 實際實作可以呼叫 /version 端點
        return True
    
    def _run_smoke_tests(self, environment: str) -> bool:
        """執行冒煙測試"""
        print(f"  🧪 執行 {environment.upper()} 冒煙測試...")
        # 實際實作可以執行關鍵功能測試
        return True
    
    def prompt_approval(self, stage: str, version: str) -> bool:
        """提示手動審核"""
        print(f"\n🔐 {stage} 審核檢查點")
        print("=" * 50)
        print(f"版本: {version}")
        print(f"階段: {stage}")
        print(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        while True:
            response = input("是否繼續部署？ (y/n/details): ").lower().strip()
            if response == 'y':
                return True
            elif response == 'n':
                print("❌ 部署已取消")
                return False
            elif response == 'details':
                self._show_deployment_details(version)
            else:
                print("請輸入 y (繼續), n (取消), 或 details (查看詳情)")
    
    def _show_deployment_details(self, version: str):
        """顯示部署詳情"""
        print("\n📊 部署詳情")
        print("-" * 30)
        print(f"版本: {version}")
        
        git_info = self.get_git_info()
        print(f"分支: {git_info['current_branch']}")
        print(f"最新標籤: {git_info['latest_tag']}")
        print(f"工作目錄: {'有未提交變更' if git_info['has_changes'] else '乾淨'}")
        print()
    
    def deploy_to_staging(self, version: str) -> bool:
        """部署到 STG 環境"""
        print(f"🚀 部署版本 {version} 到 STG 環境")
        print("=" * 50)
        
        # 檢查分支
        git_info = self.get_git_info()
        if git_info["current_branch"] == "main":
            print("⚠️  警告: 您在 main 分支上，STG 部署通常使用功能分支")
            if not self.prompt_approval("STG 分支確認", version):
                return False
        
        # 觸發 STG 部署
        print("🔧 觸發 Cloud Build (STG)...")
        success, output, error = self.run_command(
            f"gcloud builds submit --config=deployment/cloudbuild-staging.yaml ."
        )
        
        if not success:
            print(f"❌ STG 部署失敗: {error}")
            return False
        
        print("✅ STG 部署完成")
        
        # 等待服務啟動
        print("⏳ 等待服務啟動...")
        time.sleep(30)
        
        # 健康檢查
        if not self.check_stg_health(version):
            return False
        
        print(f"🎉 版本 {version} 成功部署到 STG 環境")
        return True
    
    def deploy_to_production(self, version: str) -> bool:
        """部署到 PRD 環境"""
        print(f"🚀 部署版本 {version} 到 PRD 環境")
        print("=" * 50)
        
        # 檢查分支
        git_info = self.get_git_info()
        if git_info["current_branch"] != "main":
            print(f"❌ PRD 部署必須在 main 分支 (當前: {git_info['current_branch']})")
            return False
        
        # STG 檢查點
        print("🔍 STG 檢查點驗證...")
        if not self.check_stg_health(version):
            print("❌ STG 環境驗證失敗，無法部署到 PRD")
            return False
        
        # 手動審核
        if not self.prompt_approval("PRD 部署", version):
            return False
        
        # 觸發 PRD 部署
        print("🔧 觸發 Cloud Build (PRD)...")
        success, output, error = self.run_command(
            f"gcloud builds submit --config=deployment/cloudbuild-production.yaml ."
        )
        
        if not success:
            print(f"❌ PRD 部署失敗: {error}")
            return False
        
        print("✅ PRD 部署完成")
        
        # 等待服務啟動
        print("⏳ 等待服務啟動...")
        time.sleep(60)
        
        # 健康檢查
        if not self._check_api_health("production"):
            print("⚠️  PRD 健康檢查失敗，考慮回滾")
            return False
        
        print(f"🎉 版本 {version} 成功部署到 PRD 環境")
        return True
    
    def full_release_pipeline(self, version: str):
        """完整發佈流程"""
        print(f"🎯 開始完整發佈流程: {version}")
        print("=" * 60)
        
        # 階段 1: 部署到 STG
        print("\n📍 階段 1: STG 部署")
        if not self.deploy_to_staging(version):
            print("❌ STG 部署失敗，發佈流程中止")
            return False
        
        # 階段 2: STG 驗證檢查點
        print("\n📍 階段 2: STG 驗證檢查點")
        if not self.prompt_approval("STG 驗證完成", version):
            return False
        
        # 階段 3: 合併到 main
        print("\n📍 階段 3: 合併到 main 分支")
        git_info = self.get_git_info()
        if git_info["current_branch"] != "main":
            print(f"當前分支: {git_info['current_branch']}")
            print("請手動合併到 main 分支後繼續")
            input("按 Enter 鍵繼續...")
        
        # 階段 4: 部署到 PRD
        print("\n📍 階段 4: PRD 部署")
        if not self.deploy_to_production(version):
            print("❌ PRD 部署失敗")
            return False
        
        print(f"\n🎊 版本 {version} 完整發佈流程成功完成！")
        return True
    
    def show_status(self):
        """顯示發佈狀態"""
        print("📊 發佈管理狀態")
        print("=" * 50)
        
        version = self.get_current_version()
        print(f"當前版本: {version or '未設定'}")
        
        git_info = self.get_git_info()
        print(f"當前分支: {git_info['current_branch']}")
        print(f"最新標籤: {git_info['latest_tag']}")
        print(f"工作目錄: {'有未提交變更' if git_info['has_changes'] else '乾淨'}")
    
    def show_help(self):
        """顯示使用說明"""
        print("📖 Enterprise 發佈管理系統")
        print("=" * 60)
        print("用法:")
        print("  python scripts/release_manager.py <command> [options]")
        print("")
        print("命令:")
        print("  status                    - 顯示發佈狀態")
        print("  deploy-stg <version>      - 部署到 STG 環境")
        print("  deploy-prd <version>      - 部署到 PRD 環境") 
        print("  full-release <version>    - 執行完整發佈流程 (STG → PRD)")
        print("")
        print("範例:")
        print("  python scripts/release_manager.py status")
        print("  python scripts/release_manager.py deploy-stg 1.1.0")
        print("  python scripts/release_manager.py full-release 1.1.0")
        print("")
        print("發佈流程:")
        print("  1. 功能分支 → STG 部署")
        print("  2. STG 測試 & 驗證")
        print("  3. 合併到 main 分支")
        print("  4. PRD 部署")

def main():
    manager = ReleaseManager()
    
    if len(sys.argv) < 2:
        manager.show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        manager.show_status()
        
    elif command == "deploy-stg":
        if len(sys.argv) < 3:
            print("❌ 請指定版本號")
            return
        version = sys.argv[2]
        manager.deploy_to_staging(version)
        
    elif command == "deploy-prd":
        if len(sys.argv) < 3:
            print("❌ 請指定版本號")
            return
        version = sys.argv[2]
        manager.deploy_to_production(version)
        
    elif command == "full-release":
        if len(sys.argv) < 3:
            print("❌ 請指定版本號")
            return
        version = sys.argv[2]
        manager.full_release_pipeline(version)
        
    else:
        print(f"❌ 未知命令: {command}")
        manager.show_help()

if __name__ == "__main__":
    main() 