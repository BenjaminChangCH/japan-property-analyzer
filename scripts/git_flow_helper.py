#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Flow 助手工具
協助正確執行 Git Flow 開發流程
"""

import subprocess
import sys
import re
from datetime import datetime

def run_command(command, capture_output=True):
    """執行命令並返回結果"""
    try:
        result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def get_current_branch():
    """獲取當前分支名稱"""
    success, output, _ = run_command("git branch --show-current")
    return output if success else "unknown"

def check_git_status():
    """檢查 Git 狀態"""
    success, output, _ = run_command("git status --porcelain")
    return success, output

def create_feature_branch(feature_name):
    """創建新的 feature branch"""
    print(f"🌿 創建新分支: feature/{feature_name}")
    
    # 確保在 main 分支
    current_branch = get_current_branch()
    if current_branch != "main":
        print(f"⚠️  當前分支: {current_branch}，切換到 main 分支...")
        success, _, error = run_command("git checkout main")
        if not success:
            print(f"❌ 切換到 main 分支失敗: {error}")
            return False
    
    # 拉取最新變更
    print("📥 拉取最新變更...")
    success, _, error = run_command("git pull origin main")
    if not success:
        print(f"⚠️  拉取失敗: {error}")
    
    # 創建並切換到新分支
    branch_name = f"feature/{feature_name}"
    success, _, error = run_command(f"git checkout -b {branch_name}")
    if success:
        print(f"✅ 成功創建並切換到分支: {branch_name}")
        return True
    else:
        print(f"❌ 創建分支失敗: {error}")
        return False

def commit_and_push(message, description=""):
    """提交並推送變更"""
    current_branch = get_current_branch()
    
    if current_branch == "main":
        print("🚨 警告: 您正在 main 分支上操作！")
        print("建議創建 feature branch 進行開發")
        return False
    
    # 檢查是否有變更
    success, status = check_git_status()
    if not status:
        print("📝 沒有檔案變更需要提交")
        return False
    
    print(f"📁 檔案變更:")
    print(status)
    
    # 添加檔案
    print("📤 添加變更...")
    success, _, error = run_command("git add -A")
    if not success:
        print(f"❌ 添加檔案失敗: {error}")
        return False
    
    # 提交變更
    commit_msg = message
    if description:
        commit_msg += f"\n\n{description}"
    
    print("💾 提交變更...")
    success, _, error = run_command(f'git commit -m "{commit_msg}"')
    if not success:
        print(f"❌ 提交失敗: {error}")
        return False
    
    # 推送到遠端
    print("🚀 推送到遠端...")
    success, output, error = run_command(f"git push origin {current_branch}")
    if success:
        print(f"✅ 成功推送到 {current_branch}")
        
        # 提取 PR 連結
        if "Create a pull request" in output:
            pr_match = re.search(r'https://[^\s]+/pull/new/[^\s]+', output)
            if pr_match:
                pr_url = pr_match.group()
                print(f"\n🔗 創建 Pull Request:")
                print(f"   {pr_url}")
        return True
    else:
        print(f"❌ 推送失敗: {error}")
        return False

def show_git_flow_guide():
    """顯示 Git Flow 指引"""
    print("📖 Git Flow 開發流程指引")
    print("=" * 60)
    print("1. 創建 Feature Branch:")
    print("   python scripts/git_flow_helper.py create <feature-name>")
    print("")
    print("2. 開發完成後提交:")
    print("   python scripts/git_flow_helper.py commit '<commit-message>'")
    print("")
    print("3. 創建 Pull Request (自動顯示連結)")
    print("")
    print("4. 在 GitHub 上審查並合併 PR")
    print("")
    print("5. 合併後會自動觸發 CI/CD 部署")
    print("=" * 60)
    
    print("\n🛡️  安全性保護說明:")
    print("- main 分支受到保護，不能直接推送")
    print("- 所有變更必須通過 Pull Request")
    print("- 確保代碼審查和 CI/CD 流程")

def main():
    if len(sys.argv) < 2:
        show_git_flow_guide()
        return
    
    action = sys.argv[1].lower()
    
    if action == "create":
        if len(sys.argv) < 3:
            print("❌ 請提供 feature 名稱")
            print("用法: python scripts/git_flow_helper.py create <feature-name>")
            return
        
        feature_name = sys.argv[2]
        # 清理 feature 名稱
        feature_name = re.sub(r'[^a-zA-Z0-9\-_]', '-', feature_name).lower()
        create_feature_branch(feature_name)
        
    elif action == "commit":
        if len(sys.argv) < 3:
            print("❌ 請提供提交訊息")
            print("用法: python scripts/git_flow_helper.py commit '<commit-message>'")
            return
        
        message = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        commit_and_push(message, description)
        
    elif action == "status":
        current_branch = get_current_branch()
        success, status = check_git_status()
        
        print(f"🌿 當前分支: {current_branch}")
        if status:
            print("📁 待提交的變更:")
            print(status)
        else:
            print("✅ 工作目錄乾淨")
            
    else:
        print(f"❌ 未知動作: {action}")
        show_git_flow_guide()

if __name__ == "__main__":
    main() 