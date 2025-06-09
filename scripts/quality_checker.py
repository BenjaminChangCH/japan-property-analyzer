#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
程式碼品質和安全掃描工具
"""

import os
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime

class QualityChecker:
    def __init__(self):
        self.project_root = Path('.')
        self.python_files = list(self.project_root.rglob('*.py'))
        
    def check_dependencies_security(self):
        """檢查依賴安全性"""
        print("🔒 檢查依賴安全性...")
        
        try:
            # 安裝 safety 如果不存在
            subprocess.run(['pip', 'install', 'safety'], 
                         capture_output=True, check=False)
            
            # 執行安全掃描
            result = subprocess.run(
                ['safety', 'check', '--json'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                print("✅ 依賴安全檢查通過")
                return {'status': 'safe', 'vulnerabilities': []}
            else:
                try:
                    vulnerabilities = json.loads(result.stdout)
                    print(f"⚠️  發現 {len(vulnerabilities)} 個安全漏洞")
                    for vuln in vulnerabilities:
                        print(f"  - {vuln['package']}: {vuln['vulnerability']}")
                    return {'status': 'vulnerable', 'vulnerabilities': vulnerabilities}
                except json.JSONDecodeError:
                    print("❌ 無法解析安全掃描結果")
                    return {'status': 'error', 'error': result.stderr}
                    
        except Exception as e:
            print(f"❌ 安全檢查失敗: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def check_code_style(self):
        """檢查代碼風格"""
        print("🎨 檢查代碼風格...")
        
        try:
            # 安裝 flake8 如果不存在
            subprocess.run(['pip', 'install', 'flake8'], 
                         capture_output=True, check=False)
            
            # 執行代碼風格檢查
            result = subprocess.run(
                ['flake8', '--max-line-length=100', '--ignore=E203,W503'] + 
                [str(f) for f in self.python_files],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                print("✅ 代碼風格檢查通過")
                return {'status': 'pass', 'issues': []}
            else:
                issues = result.stdout.strip().split('\n') if result.stdout.strip() else []
                print(f"⚠️  發現 {len(issues)} 個代碼風格問題")
                for issue in issues[:5]:  # 只顯示前 5 個
                    print(f"  - {issue}")
                if len(issues) > 5:
                    print(f"  ... 和其他 {len(issues) - 5} 個問題")
                return {'status': 'issues', 'issues': issues}
                
        except Exception as e:
            print(f"❌ 代碼風格檢查失敗: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def check_complexity(self):
        """檢查代碼複雜度"""
        print("📊 檢查代碼複雜度...")
        
        complex_functions = []
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 簡單的複雜度檢查：查找嵌套層級過深的代碼
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    indent_level = (len(line) - len(line.lstrip())) // 4
                    if indent_level > 4:  # 嵌套超過 4 層
                        complex_functions.append({
                            'file': str(py_file),
                            'line': i,
                            'indent_level': indent_level
                        })
                        
            except Exception as e:
                print(f"❌ 無法分析檔案 {py_file}: {e}")
        
        if not complex_functions:
            print("✅ 代碼複雜度檢查通過")
            return {'status': 'pass', 'complex_functions': []}
        else:
            print(f"⚠️  發現 {len(complex_functions)} 個高複雜度區域")
            return {'status': 'complex', 'complex_functions': complex_functions}
    
    def check_secrets(self):
        """檢查敏感資訊洩漏"""
        print("🔐 檢查敏感資訊...")
        
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', 'password'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'api_key'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'secret'),
            (r'token\s*=\s*["\'][^"\']+["\']', 'token'),
            (r'G-[A-Z0-9]{10}', 'ga_tracking_id'),
            (r'[a-zA-Z0-9]{32,}', 'potential_hash_or_key')
        ]
        
        secrets_found = []
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern, secret_type in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # 排除明顯的範例或註解
                        if 'example' in match.group().lower() or '#' in match.group():
                            continue
                            
                        line_num = content[:match.start()].count('\n') + 1
                        secrets_found.append({
                            'file': str(py_file),
                            'line': line_num,
                            'type': secret_type,
                            'match': match.group()[:20] + '...' if len(match.group()) > 20 else match.group()
                        })
                        
            except Exception as e:
                print(f"❌ 無法檢查檔案 {py_file}: {e}")
        
        if not secrets_found:
            print("✅ 敏感資訊檢查通過")
            return {'status': 'safe', 'secrets': []}
        else:
            print(f"⚠️  發現 {len(secrets_found)} 個潛在敏感資訊")
            for secret in secrets_found[:3]:  # 只顯示前 3 個
                print(f"  - {secret['file']}:{secret['line']} - {secret['type']}")
            return {'status': 'found', 'secrets': secrets_found}
    
    def check_imports(self):
        """檢查導入語句"""
        print("📦 檢查導入語句...")
        
        unused_imports = []
        missing_imports = []
        
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 查找導入語句
                import_lines = []
                for i, line in enumerate(content.split('\n'), 1):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        import_lines.append((i, line.strip()))
                
                # 簡單檢查：查找可能未使用的導入
                for line_num, import_line in import_lines:
                    if 'import ' in import_line:
                        module_name = import_line.split()[-1].split('.')[0]
                        if content.count(module_name) == 1:  # 只出現在導入行
                            unused_imports.append({
                                'file': str(py_file),
                                'line': line_num,
                                'import': import_line
                            })
                            
            except Exception as e:
                print(f"❌ 無法檢查檔案 {py_file}: {e}")
        
        if not unused_imports:
            print("✅ 導入語句檢查通過")
        else:
            print(f"⚠️  發現 {len(unused_imports)} 個可能未使用的導入")
        
        return {
            'status': 'checked',
            'unused_imports': unused_imports,
            'missing_imports': missing_imports
        }
    
    def generate_quality_report(self):
        """生成完整的品質報告"""
        print("📋 生成品質報告...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_stats': {
                'total_python_files': len(self.python_files),
                'total_lines': 0
            },
            'security': self.check_dependencies_security(),
            'style': self.check_code_style(),
            'complexity': self.check_complexity(),
            'secrets': self.check_secrets(),
            'imports': self.check_imports()
        }
        
        # 計算總行數
        total_lines = 0
        for py_file in self.python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    total_lines += len(f.readlines())
            except:
                pass
        report['project_stats']['total_lines'] = total_lines
        
        # 儲存報告
        report_file = f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 品質報告已保存: {report_file}")
        
        # 計算總分
        total_score = self.calculate_quality_score(report)
        print(f"📊 整體品質評分: {total_score}/100")
        
        return report
    
    def calculate_quality_score(self, report):
        """計算品質評分"""
        score = 100
        
        # 安全性扣分
        if report['security']['status'] == 'vulnerable':
            score -= len(report['security']['vulnerabilities']) * 10
        elif report['security']['status'] == 'error':
            score -= 5
        
        # 代碼風格扣分
        if report['style']['status'] == 'issues':
            score -= min(len(report['style']['issues']) * 2, 20)
        elif report['style']['status'] == 'error':
            score -= 5
        
        # 複雜度扣分
        if report['complexity']['status'] == 'complex':
            score -= min(len(report['complexity']['complex_functions']) * 3, 15)
        
        # 敏感資訊扣分
        if report['secrets']['status'] == 'found':
            score -= len(report['secrets']['secrets']) * 5
        
        # 導入問題扣分
        score -= min(len(report['imports']['unused_imports']) * 1, 10)
        
        return max(score, 0)

def main():
    """主要函數"""
    import sys
    
    if len(sys.argv) < 2:
        print("🔍 程式碼品質和安全掃描工具")
        print("=" * 50)
        print("用法:")
        print("  python scripts/quality_checker.py security    - 檢查依賴安全性")
        print("  python scripts/quality_checker.py style      - 檢查代碼風格")
        print("  python scripts/quality_checker.py complexity - 檢查代碼複雜度")
        print("  python scripts/quality_checker.py secrets    - 檢查敏感資訊")
        print("  python scripts/quality_checker.py all        - 執行所有檢查")
        return
    
    command = sys.argv[1].lower()
    checker = QualityChecker()
    
    if command == 'security':
        checker.check_dependencies_security()
    elif command == 'style':
        checker.check_code_style()
    elif command == 'complexity':
        checker.check_complexity()
    elif command == 'secrets':
        checker.check_secrets()
    elif command == 'all':
        checker.generate_quality_report()
    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    main() 