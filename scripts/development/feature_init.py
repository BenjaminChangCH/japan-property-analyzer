#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新功能開發初始化腳本
實現 /init [功能名稱] 指令的核心功能
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

class FeatureInitializer:
    """新功能初始化器"""
    
    def __init__(self, feature_name):
        self.feature_name = feature_name
        self.feature_slug = self._create_slug(feature_name)
        self.branch_name = f"feature/{self.feature_slug}"
        self.project_root = Path(__file__).parent.parent
        
    def _create_slug(self, name):
        """創建功能名稱的 slug"""
        return name.lower().replace(' ', '-').replace('_', '-')
    
    def _run_command(self, command, check=True):
        """執行命令並返回結果"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                cwd=self.project_root
            )
            if check and result.returncode != 0:
                print(f"❌ 命令執行失敗: {command}")
                print(f"錯誤: {result.stderr}")
                return False, result.stderr
            return True, result.stdout
        except Exception as e:
            print(f"❌ 命令執行異常: {e}")
            return False, str(e)
    
    def check_prd_status(self):
        """檢查 PRD 狀態和需求定義"""
        print("📊 檢查 PRD 狀態和需求定義...")
        
        prd_file = self.project_root / "docs" / "PRD.md"
        if not prd_file.exists():
            print("⚠️  PRD.md 文件不存在，請先創建產品需求文檔")
            return False
        
        # 讀取 PRD 內容
        with open(prd_file, 'r', encoding='utf-8') as f:
            prd_content = f.read()
        
        # 檢查功能是否在 PRD 中定義
        if self.feature_name.lower() in prd_content.lower():
            print(f"✅ 功能 '{self.feature_name}' 已在 PRD 中定義")
        else:
            print(f"⚠️  功能 '{self.feature_name}' 未在 PRD 中找到")
            print("建議先在 PRD.md 中定義此功能的需求")
        
        return True
    
    def create_feature_branch(self):
        """創建 feature branch"""
        print(f"🌿 創建 feature branch: {self.branch_name}")
        
        # 檢查當前分支
        success, current_branch = self._run_command("git branch --show-current")
        if not success:
            return False
        
        current_branch = current_branch.strip()
        print(f"當前分支: {current_branch}")
        
        # 創建新分支
        success, _ = self._run_command(f"git checkout -b {self.branch_name}")
        if not success:
            # 如果分支已存在，切換到該分支
            print(f"分支 {self.branch_name} 已存在，切換到該分支...")
            success, _ = self._run_command(f"git checkout {self.branch_name}")
            if not success:
                return False
        
        print(f"✅ 成功創建/切換到分支: {self.branch_name}")
        return True
    
    def initialize_feature(self):
        """執行完整的功能初始化流程"""
        print(f"🚀 開始初始化新功能: {self.feature_name}")
        print("=" * 60)
        
        steps = [
            ("檢查 PRD 狀態", self.check_prd_status),
            ("創建 feature branch", self.create_feature_branch),
        ]
        
        completed_steps = 0
        total_steps = len(steps)
        
        for step_name, step_func in steps:
            print(f"\n{completed_steps + 1}/{total_steps} {step_name}...")
            try:
                if step_func():
                    completed_steps += 1
                    print(f"✅ {step_name} 完成")
                else:
                    print(f"❌ {step_name} 失敗")
                    break
            except Exception as e:
                print(f"❌ {step_name} 異常: {e}")
                break
        
        # 總結
        print("\n" + "=" * 60)
        print(f"📊 初始化總結: {completed_steps}/{total_steps} 步驟完成")
        
        if completed_steps == total_steps:
            print(f"🎉 功能 '{self.feature_name}' 初始化完成！")
            print(f"🌿 開發分支: {self.branch_name}")
            print(f"📝 下一步: 使用 /feature {self.feature_name} 開始開發")
            return True
        else:
            print(f"⚠️  初始化未完全完成，請檢查上述錯誤")
            return False

def main():
    """主函數"""
    if len(sys.argv) != 2:
        print("使用方法: python feature_init.py '功能名稱'")
        print("範例: python feature_init.py 'Google OAuth 登入'")
        sys.exit(1)
    
    feature_name = sys.argv[1]
    initializer = FeatureInitializer(feature_name)
    
    success = initializer.initialize_feature()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 