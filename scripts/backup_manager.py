#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
備份和災難恢復管理工具
"""

import os
import json
import subprocess
import shutil
import tarfile
from datetime import datetime, timedelta
from pathlib import Path

class BackupManager:
    def __init__(self):
        self.backup_dir = Path('backups')
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_code_backup(self, version_tag=None):
        """創建代碼備份"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        version_tag = version_tag or self.get_current_version()
        
        backup_filename = f"code_backup_{version_tag}_{timestamp}.tar.gz"
        backup_path = self.backup_dir / backup_filename
        
        # 創建 tar 壓縮檔
        with tarfile.open(backup_path, 'w:gz') as tar:
            # 添加主要檔案
            files_to_backup = [
                'main.py',
                'version.py',
                'config/',
                'scripts/',
                'templates/',
                'deployment/',
                'docs/',
                'tests/',
                '.gitignore',
                'env.example'
            ]
            
            for file_path in files_to_backup:
                if os.path.exists(file_path):
                    tar.add(file_path)
        
        # 創建備份清單
        backup_info = {
            'timestamp': timestamp,
            'version': version_tag,
            'filename': backup_filename,
            'size_bytes': backup_path.stat().st_size,
            'files': files_to_backup
        }
        
        # 儲存備份資訊
        info_file = self.backup_dir / f"backup_info_{timestamp}.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 代碼備份完成: {backup_path}")
        print(f"📋 備份資訊: {info_file}")
        return backup_path
    
    def create_environment_backup(self):
        """創建環境配置備份"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        env_backup = {
            'timestamp': timestamp,
            'environment_variables': {},
            'cloud_run_config': {},
            'git_info': {}
        }
        
        # 備份環境變數 (不包含敏感資訊)
        safe_env_vars = [
            'ENVIRONMENT',
            'GCP_PROJECT_ID',
            'GCP_REGION',
            'CLOUD_RUN_SERVICE_NAME',
            'LOG_LEVEL'
        ]
        
        for var in safe_env_vars:
            if var in os.environ:
                env_backup['environment_variables'][var] = os.environ[var]
        
        # 備份 Git 資訊
        try:
            git_branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
            git_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
            git_tags = subprocess.check_output(['git', 'tag', '--list'], text=True).strip().split('\n')
            
            env_backup['git_info'] = {
                'current_branch': git_branch,
                'current_commit': git_commit,
                'tags': [tag for tag in git_tags if tag]
            }
        except subprocess.CalledProcessError:
            env_backup['git_info'] = {'error': '無法獲取 Git 資訊'}
        
        # 儲存環境備份
        env_backup_file = self.backup_dir / f"env_backup_{timestamp}.json"
        with open(env_backup_file, 'w', encoding='utf-8') as f:
            json.dump(env_backup, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 環境配置備份完成: {env_backup_file}")
        return env_backup_file
    
    def cleanup_old_backups(self, keep_days=30):
        """清理舊備份"""
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        deleted_count = 0
        
        for backup_file in self.backup_dir.glob('*backup*'):
            if backup_file.stat().st_mtime < cutoff_date.timestamp():
                backup_file.unlink()
                deleted_count += 1
        
        print(f"🗑️  清理 {deleted_count} 個超過 {keep_days} 天的舊備份")
        return deleted_count
    
    def list_backups(self):
        """列出所有備份"""
        backups = []
        
        for backup_file in sorted(self.backup_dir.glob('*backup*.tar.gz')):
            stat = backup_file.stat()
            backups.append({
                'filename': backup_file.name,
                'size_mb': stat.st_size / 1024 / 1024,
                'created': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return backups
    
    def get_current_version(self):
        """獲取當前版本"""
        try:
            with open('version.py', 'r', encoding='utf-8') as f:
                content = f.read()
                import re
                match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
                return match.group(1) if match else 'unknown'
        except:
            return 'unknown'

class DisasterRecoveryPlan:
    """災難恢復計畫"""
    
    @staticmethod
    def create_recovery_checklist():
        """創建災難恢復檢查清單"""
        checklist = {
            "immediate_response": [
                "確認服務中斷範圍和影響",
                "通知相關人員",
                "啟動緊急回應程序",
                "評估資料完整性"
            ],
            "system_recovery": [
                "檢查 Cloud Run 服務狀態",
                "檢查 Container Registry 映像",
                "驗證 DNS 和域名設定",
                "檢查 Cloud Build 流水線",
                "驗證環境變數設定"
            ],
            "data_recovery": [
                "檢查最新代碼備份",
                "驗證 Git repository 完整性",
                "恢復環境配置",
                "重新部署最後已知良好版本"
            ],
            "testing_and_validation": [
                "執行健康檢查",
                "驗證 API 功能",
                "測試 GA 追蹤",
                "檢查所有環境 (STG/PRD)",
                "確認用戶功能正常"
            ],
            "post_incident": [
                "記錄事件詳情",
                "分析根本原因",
                "更新災難恢復程序",
                "改進監控和警報",
                "進行事後檢討會議"
            ]
        }
        
        return checklist
    
    @staticmethod
    def create_rollback_script():
        """創建回滾腳本"""
        rollback_script = """#!/bin/bash
# 緊急回滾腳本

set -e

echo "🚨 開始緊急回滾程序..."

# 檢查參數
if [ -z "$1" ]; then
    echo "❌ 請提供要回滾的版本標籤"
    echo "用法: ./rollback.sh v1.0.0"
    exit 1
fi

VERSION_TAG=$1

echo "📋 回滾到版本: $VERSION_TAG"

# 檢查標籤是否存在
if ! git tag | grep -q "^$VERSION_TAG$"; then
    echo "❌ 版本標籤 $VERSION_TAG 不存在"
    exit 1
fi

# 創建緊急分支
EMERGENCY_BRANCH="emergency-rollback-$(date +%Y%m%d-%H%M%S)"
echo "🌿 創建緊急分支: $EMERGENCY_BRANCH"
git checkout -b $EMERGENCY_BRANCH

# 回滾到指定版本
echo "⏪ 回滾代碼到 $VERSION_TAG"
git reset --hard $VERSION_TAG

# 推送緊急分支
echo "🚀 推送緊急分支"
git push origin $EMERGENCY_BRANCH

echo "✅ 回滾完成"
echo "📝 請手動觸發 CI/CD 部署緊急分支"
echo "🔗 或使用 Cloud Console 手動部署"

echo ""
echo "📋 後續步驟:"
echo "1. 手動觸發部署"
echo "2. 驗證服務恢復"
echo "3. 通知相關人員"
echo "4. 分析問題原因"
"""
        
        return rollback_script

def main():
    """主要函數"""
    import sys
    
    if len(sys.argv) < 2:
        print("🔧 備份和災難恢復管理工具")
        print("=" * 50)
        print("用法:")
        print("  python scripts/backup_manager.py backup [version]  - 創建完整備份")
        print("  python scripts/backup_manager.py list             - 列出所有備份")
        print("  python scripts/backup_manager.py cleanup [days]   - 清理舊備份")
        print("  python scripts/backup_manager.py recovery-plan    - 顯示災難恢復計畫")
        return
    
    command = sys.argv[1].lower()
    backup_manager = BackupManager()
    
    if command == 'backup':
        version = sys.argv[2] if len(sys.argv) > 2 else None
        backup_manager.create_code_backup(version)
        backup_manager.create_environment_backup()
        
    elif command == 'list':
        backups = backup_manager.list_backups()
        if backups:
            print("📦 可用備份:")
            for backup in backups:
                print(f"  📄 {backup['filename']}")
                print(f"     大小: {backup['size_mb']:.2f} MB")
                print(f"     建立時間: {backup['created']}")
                print()
        else:
            print("📭 沒有找到備份檔案")
    
    elif command == 'cleanup':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        backup_manager.cleanup_old_backups(days)
        
    elif command == 'recovery-plan':
        dr_plan = DisasterRecoveryPlan()
        checklist = dr_plan.create_recovery_checklist()
        
        print("🚨 災難恢復檢查清單")
        print("=" * 50)
        
        for phase, tasks in checklist.items():
            print(f"\n📋 {phase.replace('_', ' ').title()}:")
            for i, task in enumerate(tasks, 1):
                print(f"  {i}. {task}")
    
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main() 