#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本號管理工具
自動化版本號更新、Git 標籤和發佈流程
"""

import subprocess
import sys
import re
import os
from datetime import datetime
from pathlib import Path

def run_command(command, capture_output=True):
    """執行命令並返回結果"""
    try:
        result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def get_current_version():
    """從 version.py 讀取當前版本"""
    version_file = Path("version.py")
    if not version_file.exists():
        return None
    
    content = version_file.read_text(encoding='utf-8')
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else None

def update_version_file(new_version):
    """更新 version.py 中的版本號"""
    version_file = Path("version.py")
    content = version_file.read_text(encoding='utf-8')
    
    # 更新版本號
    content = re.sub(
        r'(__version__\s*=\s*["\'])([^"\']+)(["\'])',
        rf'\g<1>{new_version}\g<3>',
        content
    )
    
    # 更新發佈日期
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r'(RELEASE_DATE\s*=\s*["\'])([^"\']+)(["\'])',
        rf'\g<1>{today}\g<3>',
        content
    )
    
    version_file.write_text(content, encoding='utf-8')
    print(f"✅ 更新 version.py: {new_version}")

def increment_version(current_version, bump_type):
    """遞增版本號"""
    major, minor, patch = map(int, current_version.split('.'))
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        raise ValueError(f"未知的版本類型: {bump_type}")
    
    return f"{major}.{minor}.{patch}"

def create_git_tag(version, message=""):
    """創建 Git 標籤"""
    tag_name = f"v{version}"
    tag_message = message or f"Release version {version}"
    
    # 創建標籤
    success, _, error = run_command(f'git tag -a {tag_name} -m "{tag_message}"')
    if not success:
        print(f"❌ 創建標籤失敗: {error}")
        return False
    
    print(f"✅ 創建 Git 標籤: {tag_name}")
    return True

def push_tag(version):
    """推送標籤到遠端"""
    tag_name = f"v{version}"
    success, _, error = run_command(f"git push origin {tag_name}")
    if success:
        print(f"✅ 推送標籤到遠端: {tag_name}")
        return True
    else:
        print(f"❌ 推送標籤失敗: {error}")
        return False

def get_git_info():
    """獲取 Git 資訊"""
    # 檢查是否有未提交的變更
    success, status, _ = run_command("git status --porcelain")
    has_changes = bool(status.strip()) if success else True
    
    # 獲取當前分支
    success, branch, _ = run_command("git branch --show-current")
    current_branch = branch if success else "unknown"
    
    # 獲取最新的標籤
    success, latest_tag, _ = run_command("git describe --tags --abbrev=0")
    latest_tag = latest_tag if success else "無標籤"
    
    return {
        "has_changes": has_changes,
        "current_branch": current_branch,
        "latest_tag": latest_tag
    }

def show_version_status():
    """顯示版本狀態"""
    print("📊 版本號狀態")
    print("=" * 50)
    
    current_version = get_current_version()
    if current_version:
        print(f"當前版本: {current_version}")
    else:
        print("當前版本: 未設定")
    
    git_info = get_git_info()
    print(f"當前分支: {git_info['current_branch']}")
    print(f"最新標籤: {git_info['latest_tag']}")
    print(f"工作目錄: {'有未提交變更' if git_info['has_changes'] else '乾淨'}")

def release_version(bump_type, message="", auto_push=False):
    """發佈新版本"""
    print(f"🚀 開始發佈新版本 ({bump_type})")
    print("=" * 50)
    
    # 檢查 Git 狀態
    git_info = get_git_info()
    if git_info["has_changes"]:
        print("⚠️  警告: 工作目錄有未提交的變更")
        print("建議先提交所有變更後再發佈版本")
        return False
    
    if git_info["current_branch"] != "main":
        print(f"⚠️  警告: 您不在 main 分支 (當前: {git_info['current_branch']})")
        print("建議在 main 分支進行版本發佈")
        return False
    
    # 獲取當前版本
    current_version = get_current_version()
    if not current_version:
        print("❌ 無法讀取當前版本")
        return False
    
    # 計算新版本
    try:
        new_version = increment_version(current_version, bump_type)
    except ValueError as e:
        print(f"❌ {e}")
        return False
    
    print(f"版本更新: {current_version} → {new_version}")
    
    # 更新版本檔案
    update_version_file(new_version)
    
    # 提交版本更新
    commit_message = f"chore: bump version to {new_version}"
    if message:
        commit_message += f"\n\n{message}"
    
    success, _, error = run_command("git add version.py")
    if not success:
        print(f"❌ 添加檔案失敗: {error}")
        return False
    
    success, _, error = run_command(f'git commit -m "{commit_message}"')
    if not success:
        print(f"❌ 提交失敗: {error}")
        return False
    
    print(f"✅ 提交版本更新: {new_version}")
    
    # 創建 Git 標籤
    tag_message = message or f"Release {new_version}"
    if not create_git_tag(new_version, tag_message):
        return False
    
    # 推送變更
    if auto_push:
        print("🚀 推送變更到遠端...")
        
        # 推送提交
        success, _, error = run_command("git push origin main")
        if not success:
            print(f"❌ 推送提交失敗: {error}")
            return False
        
        # 推送標籤
        if not push_tag(new_version):
            return False
        
        print(f"🎉 版本 {new_version} 發佈完成！")
    else:
        print(f"✅ 版本 {new_version} 準備完成")
        print("🔄 使用以下命令推送到遠端:")
        print(f"   git push origin main")
        print(f"   git push origin v{new_version}")
    
    return True

def show_help():
    """顯示使用說明"""
    print("📖 版本號管理工具")
    print("=" * 50)
    print("用法:")
    print("  python scripts/version_manager.py <command> [options]")
    print("")
    print("命令:")
    print("  status                    - 顯示當前版本狀態")
    print("  release <type> [message]  - 發佈新版本")
    print("    type: major|minor|patch")
    print("    message: 發佈說明 (可選)")
    print("  push <version>           - 推送指定版本標籤")
    print("")
    print("範例:")
    print("  python scripts/version_manager.py status")
    print("  python scripts/version_manager.py release patch")
    print("  python scripts/version_manager.py release minor \"新增計算功能\"")
    print("  python scripts/version_manager.py release major \"重大更新\"")
    print("")
    print("版本號規則 (Semantic Versioning):")
    print("  MAJOR.MINOR.PATCH")
    print("  - MAJOR: 重大功能變更或不相容的 API 變更")
    print("  - MINOR: 新增功能，向後相容")
    print("  - PATCH: 錯誤修復，向後相容")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        show_version_status()
        
    elif command == "release":
        if len(sys.argv) < 3:
            print("❌ 請指定版本類型: major, minor, 或 patch")
            return
        
        bump_type = sys.argv[2].lower()
        if bump_type not in ['major', 'minor', 'patch']:
            print("❌ 版本類型必須是: major, minor, 或 patch")
            return
        
        message = sys.argv[3] if len(sys.argv) > 3 else ""
        release_version(bump_type, message, auto_push=False)
        
    elif command == "push":
        if len(sys.argv) < 3:
            print("❌ 請指定版本號")
            return
        
        version = sys.argv[2]
        push_tag(version)
        
    else:
        print(f"❌ 未知命令: {command}")
        show_help()

if __name__ == "__main__":
    main() 