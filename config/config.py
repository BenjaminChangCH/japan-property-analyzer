#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
環境配置管理
管理不同環境的配置參數
"""

import os

# 環境配置
ENVIRONMENTS = {
    'development': {
        'ga_tracking_id': '',  # 開發環境不需要 GA
        'environment_name': 'development',
        'debug_mode': True,
        'url': 'http://localhost:5000'
    },
    'staging': {
        'ga_tracking_id': 'G-59XMZ0SZ0G',
        'environment_name': 'staging', 
        'debug_mode': True,
        'url': 'https://japan-property-analyzer-2dal3iq3qa-an.a.run.app'
    },
    'production': {
        'ga_tracking_id': 'G-94SVDFL5YN',  # PRD 環境獨立的 GA 追蹤 ID
        'environment_name': 'production',
        'debug_mode': False,
        'url': 'https://japan-property-analyzer-prod-2dal3iq3qa-an.a.run.app'
    }
}

def get_environment_config(env_name=None):
    """
    獲取環境配置
    
    Args:
        env_name (str): 環境名稱，如果為 None 則從環境變數讀取
    
    Returns:
        dict: 環境配置
    """
    if env_name is None:
        env_name = os.environ.get('ENVIRONMENT', 'development')
    
    return ENVIRONMENTS.get(env_name, ENVIRONMENTS['development'])

def get_ga_tracking_id(env_name=None):
    """
    獲取指定環境的 GA 追蹤 ID
    
    Args:
        env_name (str): 環境名稱
    
    Returns:
        str: GA 追蹤 ID
    """
    # 優先從環境變數讀取
    env_ga_id = os.environ.get('GA_TRACKING_ID')
    if env_ga_id:
        return env_ga_id
    
    # 否則從配置檔讀取
    config = get_environment_config(env_name)
    return config['ga_tracking_id']

def update_production_ga_id(new_ga_id):
    """
    更新生產環境的 GA 追蹤 ID
    
    Args:
        new_ga_id (str): 新的 GA 追蹤 ID
    """
    ENVIRONMENTS['production']['ga_tracking_id'] = new_ga_id
    print(f"✅ 已更新 PRD 環境 GA 追蹤 ID: {new_ga_id}")

def get_environment_comparison():
    """
    獲取環境對比資訊
    
    Returns:
        dict: 環境對比表
    """
    comparison = {}
    for env_name, config in ENVIRONMENTS.items():
        comparison[env_name] = {
            'GA 追蹤 ID': config['ga_tracking_id'] or '未設定',
            '環境名稱': config['environment_name'],
            '除錯模式': '啟用' if config['debug_mode'] else '關閉',
            '網址': config['url']
        }
    return comparison

if __name__ == "__main__":
    # 顯示目前環境配置
    print("🌍 環境配置總覽")
    print("=" * 60)
    
    comparison = get_environment_comparison()
    
    for env, config in comparison.items():
        print(f"\n📋 {env.upper()} 環境:")
        for key, value in config.items():
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    print("💡 使用說明:")
    print("   1. 在 Cloud Build 中設定 GA_TRACKING_ID 環境變數")
    print("   2. 在 Cloud Build 中設定 ENVIRONMENT 環境變數") 
    print("   3. Flask 應用會自動讀取對應的配置") 