#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
開發完成檢查腳本
實現 /complete 指令的核心功能
確保開發完成後各環境資料一致，並準備下一次開發
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path

class DevCompleteChecker:
    """開發完成檢查器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.current_branch = None
        self.feature_name = None
        self.check_results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        
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
                return False, result.stderr
            return True, result.stdout
        except Exception as e:
            return False, str(e)
    
    def _add_result(self, category, message):
        """添加檢查結果"""
        self.check_results[category].append(message)
        
        if category == 'passed':
            print(f"✅ {message}")
        elif category == 'failed':
            print(f"❌ {message}")
        elif category == 'warnings':
            print(f"⚠️  {message}")
    
    def get_current_branch_info(self):
        """獲取當前分支信息"""
        print("🔍 檢查當前分支信息...")
        
        # 獲取當前分支
        success, branch = self._run_command("git branch --show-current")
        if not success:
            self._add_result('failed', "無法獲取當前分支信息")
            return False
        
        self.current_branch = branch.strip()
        
        # 判斷功能名稱
        if self.current_branch.startswith('feature/'):
            self.feature_name = self.current_branch.replace('feature/', '').replace('-', ' ').title()
        else:
            self.feature_name = "當前功能"
        
        self._add_result('passed', f"當前分支: {self.current_branch}")
        self._add_result('passed', f"功能名稱: {self.feature_name}")
        
        return True
    
    def check_code_quality(self):
        """檢查程式碼品質"""
        print("\n🔍 檢查程式碼品質...")
        
        # 檢查 Python 語法錯誤
        python_files = list(self.project_root.glob("**/*.py"))
        syntax_errors = 0
        
        for py_file in python_files:
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
                
            success, output = self._run_command(f"python -m py_compile {py_file}", check=False)
            if not success:
                syntax_errors += 1
                self._add_result('failed', f"語法錯誤: {py_file.name}")
        
        if syntax_errors == 0:
            self._add_result('passed', f"Python 語法檢查通過 ({len(python_files)} 個文件)")
        
        # 檢查 main.py 的函數長度
        main_file = self.project_root / "main.py"
        if main_file.exists():
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 檢查 calculate 函數是否過長
            if 'def calculate(' in content:
                lines = content.split('\n')
                in_calculate = False
                calculate_lines = 0
                
                for line in lines:
                    if 'def calculate(' in line:
                        in_calculate = True
                        calculate_lines = 1
                    elif in_calculate:
                        if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                            break
                        calculate_lines += 1
                
                if calculate_lines > 100:
                    self._add_result('warnings', f"calculate 函數過長 ({calculate_lines} 行)，建議重構")
                else:
                    self._add_result('passed', f"calculate 函數長度合理 ({calculate_lines} 行)")
        
        return True
    
    def check_tests(self):
        """檢查測試狀態"""
        print("\n🧪 檢查測試狀態...")
        
        # 檢查測試文件是否存在
        test_dirs = ['tests/unit', 'tests/integration']
        test_files_found = 0
        
        for test_dir in test_dirs:
            test_path = self.project_root / test_dir
            if test_path.exists():
                test_files = list(test_path.glob("test_*.py"))
                test_files_found += len(test_files)
        
        if test_files_found > 0:
            self._add_result('passed', f"找到 {test_files_found} 個測試文件")
            
            # 嘗試運行測試
            success, output = self._run_command("python -m pytest tests/ -v", check=False)
            if success:
                self._add_result('passed', "測試執行成功")
            else:
                self._add_result('warnings', "測試執行有問題，請檢查")
        else:
            self._add_result('warnings', "未找到測試文件，建議添加測試")
        
        return True
    
    def check_documentation(self):
        """檢查文檔完整性"""
        print("\n📚 檢查文檔完整性...")
        
        # 檢查必要文檔
        required_docs = [
            ('README.md', '專案說明文檔'),
            ('docs/PRD.md', '產品需求文檔'),
            ('docs/CODE_ANALYSIS.md', '程式碼分析文檔'),
            ('.cursorrules', 'Cursor 規則文檔')
        ]
        
        for doc_file, description in required_docs:
            doc_path = self.project_root / doc_file
            if doc_path.exists():
                self._add_result('passed', f"{description} 存在")
            else:
                self._add_result('failed', f"{description} 缺失: {doc_file}")
        
        # 檢查功能相關文檔
        if self.current_branch.startswith('feature/'):
            feature_slug = self.current_branch.replace('feature/', '')
            feature_docs = [
                f"docs/{feature_slug}_implementation.md",
                f"docs/{feature_slug}_api.md"
            ]
            
            for doc in feature_docs:
                doc_path = self.project_root / doc
                if doc_path.exists():
                    self._add_result('passed', f"功能文檔存在: {doc}")
                else:
                    self._add_result('warnings', f"功能文檔缺失: {doc}")
        
        return True
    
    def check_git_status(self):
        """檢查 Git 狀態"""
        print("\n📝 檢查 Git 狀態...")
        
        # 檢查是否有未提交的變更
        success, status = self._run_command("git status --porcelain")
        if not success:
            self._add_result('failed', "無法檢查 Git 狀態")
            return False
        
        if status.strip():
            self._add_result('warnings', "有未提交的變更")
            print("   未提交的文件:")
            for line in status.strip().split('\n'):
                print(f"   {line}")
        else:
            self._add_result('passed', "所有變更已提交")
        
        # 檢查是否與遠端同步
        success, _ = self._run_command(f"git fetch origin {self.current_branch}", check=False)
        success, behind = self._run_command(f"git rev-list --count HEAD..origin/{self.current_branch}", check=False)
        success, ahead = self._run_command(f"git rev-list --count origin/{self.current_branch}..HEAD", check=False)
        
        if success:
            behind_count = int(behind.strip()) if behind.strip().isdigit() else 0
            ahead_count = int(ahead.strip()) if ahead.strip().isdigit() else 0
            
            if behind_count > 0:
                self._add_result('warnings', f"落後遠端 {behind_count} 個提交")
            elif ahead_count > 0:
                self._add_result('warnings', f"領先遠端 {ahead_count} 個提交，建議推送")
            else:
                self._add_result('passed', "與遠端同步")
        
        return True
    
    def check_deployment_readiness(self):
        """檢查部署準備狀態"""
        print("\n🚀 檢查部署準備狀態...")
        
        # 檢查必要的配置文件
        config_files = [
            ('requirements.txt', '依賴配置'),
            ('Dockerfile', 'Docker 配置'),
            ('.github/workflows/deploy.yml', 'CI/CD 配置')
        ]
        
        for config_file, description in config_files:
            config_path = self.project_root / config_file
            if config_path.exists():
                self._add_result('passed', f"{description} 存在")
            else:
                self._add_result('warnings', f"{description} 缺失: {config_file}")
        
        # 檢查環境變數文檔
        env_example = self.project_root / ".env.example"
        if env_example.exists():
            self._add_result('passed', "環境變數範例文件存在")
        else:
            self._add_result('warnings', "建議創建 .env.example 文件")
        
        return True
    
    def update_prd_progress(self):
        """更新 PRD 進度"""
        print("\n📊 更新 PRD 進度...")
        
        prd_file = self.project_root / "docs" / "PRD.md"
        if not prd_file.exists():
            self._add_result('failed', "PRD.md 文件不存在")
            return False
        
        # 讀取 PRD 內容
        with open(prd_file, 'r', encoding='utf-8') as f:
            prd_content = f.read()
        
        # 添加完成記錄
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 檢查是否已有進度更新區塊
        if "## 📊 最新進度更新" in prd_content:
            # 在現有區塊中添加新記錄
            progress_update = f"""
**{timestamp}**: 完成 {self.feature_name} 開發檢查
- 狀態: 🔵 開發完成
- 分支: {self.current_branch}
- 檢查結果: ✅ {len(self.check_results['passed'])} 項通過, ⚠️ {len(self.check_results['warnings'])} 項警告, ❌ {len(self.check_results['failed'])} 項失敗
"""
            
            # 在最新進度更新區塊後添加
            updated_content = prd_content.replace(
                "## 📊 最新進度更新",
                f"## 📊 最新進度更新{progress_update}"
            )
        else:
            # 創建新的進度更新區塊
            progress_update = f"""

## 📊 最新進度更新

**{timestamp}**: 完成 {self.feature_name} 開發檢查
- 狀態: 🔵 開發完成
- 分支: {self.current_branch}
- 檢查結果: ✅ {len(self.check_results['passed'])} 項通過, ⚠️ {len(self.check_results['warnings'])} 項警告, ❌ {len(self.check_results['failed'])} 項失敗
"""
            updated_content = prd_content + progress_update
        
        with open(prd_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        self._add_result('passed', "PRD 進度已更新")
        return True
    
    def generate_completion_report(self):
        """生成完成報告"""
        print("\n📋 生成完成報告...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = self.project_root / "docs" / f"completion_report_{timestamp}.md"
        
        report_content = f"""# 開發完成報告

**功能名稱**: {self.feature_name}  
**分支**: {self.current_branch}  
**檢查時間**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 檢查結果總覽

- ✅ **通過項目**: {len(self.check_results['passed'])} 項
- ⚠️  **警告項目**: {len(self.check_results['warnings'])} 項  
- ❌ **失敗項目**: {len(self.check_results['failed'])} 項

## 詳細結果

### ✅ 通過項目
"""
        
        for item in self.check_results['passed']:
            report_content += f"- {item}\n"
        
        if self.check_results['warnings']:
            report_content += "\n### ⚠️ 警告項目\n"
            for item in self.check_results['warnings']:
                report_content += f"- {item}\n"
        
        if self.check_results['failed']:
            report_content += "\n### ❌ 失敗項目\n"
            for item in self.check_results['failed']:
                report_content += f"- {item}\n"
        
        report_content += f"""

## 下一步建議

### 如果準備部署到 STG
```bash
# 推送到當前分支觸發 STG 部署
git push origin {self.current_branch}
```

### 如果準備合併到 main
1. 確保所有警告和失敗項目都已解決
2. 創建 Pull Request
3. 等待代碼審查
4. 合併到 main 分支觸發 PRD 部署

## 環境 URL

- **STG 環境**: https://japan-property-analyzer-864942598341.asia-northeast1.run.app
- **PRD 環境**: https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app

## 相關指令

- `/deploy-stg` - 部署到 STG 環境
- `/deploy-prd` - 部署到 PRD 環境（需先合併到 main）
- `/test` - 運行測試
- `/review` - 代碼審查

---

**報告生成時間**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self._add_result('passed', f"完成報告已生成: {report_file.name}")
        return report_file
    
    def prepare_next_development(self):
        """準備下一次開發"""
        print("\n🔄 準備下一次開發...")
        
        # 清理臨時文件
        temp_patterns = ['*.pyc', '__pycache__', '.pytest_cache', '*.log']
        cleaned_files = 0
        
        for pattern in temp_patterns:
            for temp_file in self.project_root.rglob(pattern):
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
        
        if cleaned_files > 0:
            self._add_result('passed', f"清理了 {cleaned_files} 個臨時文件")
        
        # 檢查虛擬環境
        venv_path = self.project_root / ".venv"
        if venv_path.exists():
            self._add_result('passed', "虛擬環境存在")
        else:
            self._add_result('warnings', "虛擬環境不存在，建議創建")
        
        # 檢查依賴更新
        success, outdated = self._run_command("pip list --outdated", check=False)
        if success and outdated.strip():
            outdated_count = len(outdated.strip().split('\n')) - 2  # 減去標題行
            if outdated_count > 0:
                self._add_result('warnings', f"有 {outdated_count} 個套件可以更新")
        
        return True
    
    def run_complete_check(self):
        """執行完整的開發完成檢查"""
        print("🎯 開始執行開發完成檢查")
        print("=" * 60)
        
        checks = [
            ("獲取分支信息", self.get_current_branch_info),
            ("檢查程式碼品質", self.check_code_quality),
            ("檢查測試狀態", self.check_tests),
            ("檢查文檔完整性", self.check_documentation),
            ("檢查 Git 狀態", self.check_git_status),
            ("檢查部署準備", self.check_deployment_readiness),
            ("更新 PRD 進度", self.update_prd_progress),
            ("準備下一次開發", self.prepare_next_development)
        ]
        
        for check_name, check_func in checks:
            try:
                check_func()
            except Exception as e:
                self._add_result('failed', f"{check_name} 執行異常: {e}")
        
        # 生成完成報告
        report_file = self.generate_completion_report()
        
        # 總結
        print("\n" + "=" * 60)
        print("📊 開發完成檢查總結")
        print(f"✅ 通過: {len(self.check_results['passed'])} 項")
        print(f"⚠️  警告: {len(self.check_results['warnings'])} 項")
        print(f"❌ 失敗: {len(self.check_results['failed'])} 項")
        
        if len(self.check_results['failed']) == 0:
            print("\n🎉 恭喜！開發檢查全部通過")
            print("📝 建議下一步:")
            if len(self.check_results['warnings']) == 0:
                print("   1. 推送代碼到遠端分支")
                print("   2. 部署到 STG 環境測試")
                print("   3. 創建 Pull Request 準備合併")
            else:
                print("   1. 處理警告項目（可選）")
                print("   2. 推送代碼到遠端分支")
                print("   3. 部署到 STG 環境測試")
        else:
            print("\n⚠️  請先解決失敗項目再進行部署")
        
        # 檢查 Git 狀態
        has_uncommitted_changes = False
        for msg in self.check_results['warnings']:
            if "有未提交的變更" in msg:
                has_uncommitted_changes = True
                break
        
        print("\n📝 下一步行動建議：")

        if has_uncommitted_changes:
            print("   您有未提交的變更。請先提交這些變更，這是部署前的必要步驟。")
            print("   1. 暫存所有變更：`git add .`")
            print("   2. 提交變更：`git commit -m \"feat: [您的提交訊息，請遵循 Commit 訊息規範]\"`")
            print("      - Commit 訊息規範：`feat:` 新功能, `fix:` 錯誤修復, `docs:` 文檔更新, `style:` 程式碼格式調整, `refactor:` 程式碼重構, `test:` 測試相關, `chore:` 建置工具或輔助工具的變動")
            print("   **請在提交變更後再次執行 `/complete` 指令，以更新專案狀態。**")
        else:
            if self.current_branch.startswith('feature/'):
                print("   當前為功能開發分支 (`feature/{}`)。".format(self.current_branch.split('/', 1)[1]))
                print("   1. 推送代碼到遠端：`git push origin {}`".format(self.current_branch))
                print("      - 這將會自動觸發 STG 測試環境的部署。")
                print("      - STG 網址：https://japan-property-analyzer-864942598341.asia-northeast1.run.app")
                print("   2. 在 STG 環境進行功能測試和審查。")
                print("   3. 測試通過後，請創建 Pull Request (PR) 到 `main` 分支。")
                print("      - PRD 部署將在 PR 合併到 `main` 分支後自動觸發。")
                print("      - PRD 網址：https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app")
            elif self.current_branch == 'main':
                print("   當前為 `main` 分支。")
                print("   `main` 分支的部署是通過合併 Pull Request (PR) 到 `main` 分支自動觸發的。")
                print("   1. 確保所有功能已在 STG 環境充分測試。")
                print("   2. 確保相關的 Pull Request 已被審查並合併。")
                print("   3. 確認 PRD 環境已自動部署並正常運行：https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app")
            else:
                print("   當前分支 (`{}`) 不屬於標準功能或主分支，請手動進行後續操作。".format(self.current_branch))
            
            print("\n💡 最佳實踐建議：")
            print("   - 每次主要功能開發完成後，請執行 `python scripts/cursor_commands.py complete` 進行全面檢查。")
            print("   - 定期查看 `docs/PRD.md` 和 `docs/CHANGELOG.md` 確保文檔同步更新。")
            print("   - 遵循 `.cursorrules` 中定義的程式碼風格、版本控制和部署規範。")
        
        print("\n---\n")
        print("📋 詳細報告: docs/completion_report_{}.md".format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
        
        return len(self.check_results['failed']) == 0

def main():
    """主函數"""
    checker = DevCompleteChecker()
    success = checker.run_complete_check()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 