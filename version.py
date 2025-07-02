#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本號管理
Japan Property Analyzer 版本資訊
"""

# 版本號遵循 Semantic Versioning (SemVer): MAJOR.MINOR.PATCH
# MAJOR: 重大功能變更或不相容的 API 變更
# MINOR: 新增功能，向後相容
# PATCH: 錯誤修復，向後相容

__version__ = "1.1.3"
__version_info__ = tuple(map(int, __version__.split('.')))

# 應用程式資訊
APP_NAME = "NIPPON PROPERTY ANALYTICS"
APP_DESCRIPTION = "Professional Investment Intelligence - 日本不動產投資專業分析平台"
APP_AUTHOR = "Benjamin Chang"
APP_URL = "https://github.com/your-username/nippon-property-analytics"

# 發佈資訊
RELEASE_DATE = "2025-07-02"
BUILD_NUMBER = None  # 將由 CI/CD 系統自動設定

def get_version():
    """獲取完整版本字串"""
    version_str = __version__
    if BUILD_NUMBER:
        version_str += f".{BUILD_NUMBER}"
    return version_str

def get_version_info():
    """獲取版本資訊字典"""
    return {
        "version": get_version(),
        "version_info": __version_info__,
        "app_name": APP_NAME,
        "description": APP_DESCRIPTION,
        "author": APP_AUTHOR,
        "url": APP_URL,
        "release_date": RELEASE_DATE,
        "build_number": BUILD_NUMBER
    }

def print_version():
    """列印版本資訊"""
    info = get_version_info()
    print(f"{info['app_name']} v{info['version']}")
    print(f"Description: {info['description']}")
    print(f"Author: {info['author']}")
    print(f"Release Date: {info['release_date']}")
    if info['build_number']:
        print(f"Build: {info['build_number']}")

if __name__ == "__main__":
    print_version() 