#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cursor 指令包裝腳本
統一管理所有簡化指令 (Slash Commands)
"""

import sys
import subprocess
from pathlib import Path

def show_help():
    """顯示幫助信息"""
    help_text = """
🚀 Cursor 簡化指令系統

使用方法: python scripts/cursor_commands.py <指令> [參數]

📋 可用指令:

🔧 開發相關指令:
  init <功能名稱>     - 一鍵初始化新功能開發環境
  complete            - 開發完成檢查，確保環境一致性

📊 專案管理指令:
  status              - 檢查專案整體狀態和進度
  clean               - 清理暫存檔案和無用程式碼

📚 文件管理指令:
  prd                 - 檢查 PRD 狀態
  changelog           - 更新版本變更記錄

🔖 版本控制指令:
  version             - 檢查當前版本信息
  release <版本號>    - 準備版本發布

🎓 學習支援指令:
  help                - 顯示此幫助信息

範例:
  python scripts/cursor_commands.py init "Google OAuth 登入"
  python scripts/cursor_commands.py complete
  python scripts/cursor_commands.py changelog
  python scripts/cursor_commands.py release v1.2.0
  python scripts/cursor_commands.py help
"""
    print(help_text)

def run_init(feature_name):
    """執行功能初始化"""
    if not feature_name:
        print("❌ 請提供功能名稱")
        print("範例: python scripts/cursor_commands.py init 'Google OAuth 登入'")
        return False
    
    script_path = Path(__file__).parent / "feature_init.py"
    result = subprocess.run([sys.executable, str(script_path), feature_name])
    return result.returncode == 0

def run_complete():
    """執行開發完成檢查"""
    script_path = Path(__file__).parent / "dev_complete_check.py"
    result = subprocess.run([sys.executable, str(script_path)])
    return result.returncode == 0

def run_status():
    """檢查專案狀態"""
    print("📊 專案狀態檢查")
    print("=" * 40)
    
    # 檢查當前分支
    result = subprocess.run(["git", "branch", "--show-current"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(f"🌿 當前分支: {result.stdout.strip()}")
    
    # 檢查 Git 狀態
    result = subprocess.run(["git", "status", "--porcelain"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        if result.stdout.strip():
            print("📝 有未提交的變更")
        else:
            print("✅ 所有變更已提交")
    
    # 檢查 PRD 文件
    prd_file = Path("docs/PRD.md")
    if prd_file.exists():
        print("✅ PRD 文檔存在")
    else:
        print("❌ PRD 文檔缺失")
    
    print("\n💡 使用 'python scripts/cursor_commands.py complete' 進行詳細檢查")

def run_clean():
    """清理專案"""
    print("🧹 清理專案文件...")
    
    project_root = Path(__file__).parent.parent
    temp_patterns = ['*.pyc', '__pycache__', '.pytest_cache', '*.log']
    cleaned_files = 0
    
    for pattern in temp_patterns:
        for temp_file in project_root.rglob(pattern):
            try:
                if temp_file.is_file():
                    temp_file.unlink()
                    cleaned_files += 1
                elif temp_file.is_dir():
                    import shutil
                    shutil.rmtree(temp_file)
                    cleaned_files += 1
            except:
                pass
    
    print(f"✅ 清理了 {cleaned_files} 個臨時文件")

def run_prd():
    """檢查 PRD 狀態"""
    prd_file = Path("docs/PRD.md")
    if not prd_file.exists():
        print("❌ PRD.md 文件不存在")
        return False
    
    print("📊 PRD 狀態檢查")
    print("=" * 40)
    
    with open(prd_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 統計狀態標記
    status_counts = {
        '🔴': content.count('🔴'),
        '🟡': content.count('🟡'),
        '🟢': content.count('🟢'),
        '🔵': content.count('🔵'),
        '⚠️': content.count('⚠️'),
        '📋': content.count('📋')
    }
    
    print("狀態統計:")
    for status, count in status_counts.items():
        if count > 0:
            print(f"  {status} {count} 項")
    
    print(f"\n📄 PRD 文件大小: {len(content)} 字符")
    print("💡 使用文本編輯器打開 docs/PRD.md 查看詳細內容")

def run_changelog():
    """更新版本變更記錄"""
    changelog_file = Path("docs/CHANGELOG.md")
    if not changelog_file.exists():
        print("❌ CHANGELOG.md 文件不存在")
        return False
    
    print("📝 版本變更記錄狀態")
    print("=" * 40)
    
    with open(changelog_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查是否有未發布的變更
    if "[未發布]" in content:
        print("✅ 有未發布的變更記錄")
    else:
        print("⚠️  沒有未發布的變更記錄")
    
    # 統計版本數量
    import re
    versions = re.findall(r'\[v?\d+\.\d+\.\d+\]', content)
    print(f"📊 已記錄版本數量: {len(versions)}")
    
    if versions:
        latest_version = versions[0]
        print(f"🏷️  最新版本: {latest_version}")
    
    print("\n💡 編輯 docs/CHANGELOG.md 來更新變更記錄")
    return True

def run_version():
    """檢查當前版本信息"""
    print("🔖 版本信息檢查")
    print("=" * 40)
    
    # 檢查 Git 標籤
    result = subprocess.run(["git", "tag", "--sort=-version:refname"], 
                          capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        tags = result.stdout.strip().split('\n')
        latest_tag = tags[0]
        print(f"🏷️  最新 Git 標籤: {latest_tag}")
        print(f"📊 總標籤數量: {len(tags)}")
    else:
        print("⚠️  沒有找到 Git 標籤")
    
    # 檢查當前分支
    result = subprocess.run(["git", "branch", "--show-current"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        current_branch = result.stdout.strip()
        print(f"🌿 當前分支: {current_branch}")
    
    # 檢查提交數量
    result = subprocess.run(["git", "rev-list", "--count", "HEAD"], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        commit_count = result.stdout.strip()
        print(f"📝 總提交數量: {commit_count}")
    
    # 檢查 CHANGELOG
    changelog_file = Path("docs/CHANGELOG.md")
    if changelog_file.exists():
        print("✅ CHANGELOG.md 存在")
        with open(changelog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if "[未發布]" in content:
            print("📋 有未發布的變更")
    else:
        print("❌ CHANGELOG.md 不存在")
    
    return True

def run_release(version):
    """準備版本發布"""
    if not version:
        print("❌ 請提供版本號")
        print("範例: python scripts/cursor_commands.py release v1.2.0")
        return False
    
    print(f"🚀 準備發布版本 {version}")
    print("=" * 40)
    
    # 檢查版本號格式
    import re
    if not re.match(r'^v?\d+\.\d+\.\d+$', version):
        print("❌ 版本號格式不正確，應為 vX.Y.Z 或 X.Y.Z")
        return False
    
    # 確保版本號以 v 開頭
    if not version.startswith('v'):
        version = 'v' + version
    
    # 檢查 CHANGELOG
    changelog_file = Path("docs/CHANGELOG.md")
    if not changelog_file.exists():
        print("❌ CHANGELOG.md 文件不存在，請先創建")
        return False
    
    # 檢查是否有未提交的變更
    result = subprocess.run(["git", "status", "--porcelain"], 
                          capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        print("⚠️  有未提交的變更，建議先提交所有變更")
        print("未提交的文件:")
        for line in result.stdout.strip().split('\n'):
            print(f"   {line}")
        
        response = input("\n是否繼續發布？(y/N): ")
        if response.lower() != 'y':
            print("❌ 發布已取消")
            return False
    
    # 更新 CHANGELOG
    with open(changelog_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "[未發布]" in content:
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        updated_content = content.replace("[未發布]", f"[{version}] - {today}")
        
        with open(changelog_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ 已更新 CHANGELOG.md，將 [未發布] 改為 [{version}] - {today}")
    else:
        print("⚠️  CHANGELOG.md 中沒有 [未發布] 區塊")
    
    # 提供發布步驟指引
    print(f"\n📋 發布步驟指引:")
    print(f"1. 檢查並提交所有變更:")
    print(f"   git add .")
    print(f"   git commit -m 'chore: prepare release {version}'")
    print(f"")
    print(f"2. 創建 Git 標籤:")
    print(f"   git tag {version}")
    print(f"")
    print(f"3. 推送到遠端:")
    print(f"   git push origin {version}")
    print(f"   git push origin main")
    print(f"")
    print(f"4. 部署將自動觸發")
    
    return True

def main():
    """主函數"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help" or command == "-h" or command == "--help":
        show_help()
    elif command == "init":
        feature_name = sys.argv[2] if len(sys.argv) > 2 else None
        run_init(feature_name)
    elif command == "complete":
        run_complete()
    elif command == "status":
        run_status()
    elif command == "clean":
        run_clean()
    elif command == "prd":
        run_prd()
    elif command == "changelog":
        run_changelog()
    elif command == "version":
        run_version()
    elif command == "release":
        version = sys.argv[2] if len(sys.argv) > 2 else None
        run_release(version)
    else:
        print(f"❌ 未知指令: {command}")
        print("使用 'python scripts/cursor_commands.py help' 查看可用指令")

if __name__ == "__main__":
    main() 