#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全性配置管理
"""

import os
import secrets
from flask import request
import time
from functools import wraps

# 安全性常數
MAX_REQUESTS_PER_MINUTE = 60
MAX_CALCULATION_REQUESTS_PER_MINUTE = 20
ALLOWED_ORIGINS = [
    'https://japan-property-analyzer-prod-864942598341.asia-northeast1.run.app',
    'https://japan-property-analyzer-864942598341.asia-northeast1.run.app',
    'http://localhost:8080',
    'http://127.0.0.1:8080'
]

# 請求限制追蹤
request_counts = {}
calculation_counts = {}

def setup_security_headers(app):
    """設定安全性標頭"""
    
    @app.after_request
    def add_security_headers(response):
        # 防止 XSS 攻擊
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # HTTPS 重導向 (生產環境)
        if os.environ.get('ENVIRONMENT') == 'production':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # CSP 設定 - 支援 Google OAuth 和 Google Fonts
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://www.google-analytics.com https://cdnjs.cloudflare.com https://accounts.google.com; "
            "script-src-elem 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com https://cdnjs.cloudflare.com https://accounts.google.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://accounts.google.com; "
            "style-src-elem 'self' 'unsafe-inline' https://fonts.googleapis.com https://accounts.google.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https://www.google-analytics.com https://lh3.googleusercontent.com https://accounts.google.com; "
            "connect-src 'self' https://www.google-analytics.com https://accounts.google.com https://identitytoolkit.googleapis.com; "
            "frame-src https://accounts.google.com; "
            "object-src 'none'; "
            "base-uri 'self'; "
        )
        response.headers['Content-Security-Policy'] = csp
        
        return response

def rate_limit(max_requests=MAX_REQUESTS_PER_MINUTE):
    """請求頻率限制裝飾器"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # 清理舊記錄
            cleanup_old_requests()
            
            # 檢查請求頻率
            if client_ip in request_counts:
                requests_in_minute = len([
                    req_time for req_time in request_counts[client_ip]
                    if current_time - req_time < 60
                ])
                
                if requests_in_minute >= max_requests:
                    return {
                        'error': '請求過於頻繁，請稍後再試',
                        'retry_after': 60
                    }, 429
            
            # 記錄請求
            if client_ip not in request_counts:
                request_counts[client_ip] = []
            request_counts[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

def calculation_rate_limit(f):
    """計算 API 專用頻率限制"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()
        
        # 清理舊記錄
        cleanup_old_calculations()
        
        # 檢查計算請求頻率
        if client_ip in calculation_counts:
            calc_requests_in_minute = len([
                req_time for req_time in calculation_counts[client_ip]
                if current_time - req_time < 60
            ])
            
            if calc_requests_in_minute >= MAX_CALCULATION_REQUESTS_PER_MINUTE:
                return {
                    'error': '計算請求過於頻繁，請稍後再試',
                    'retry_after': 60
                }, 429
        
        # 記錄計算請求
        if client_ip not in calculation_counts:
            calculation_counts[client_ip] = []
        calculation_counts[client_ip].append(current_time)
        
        return f(*args, **kwargs)
    return wrapper

def cleanup_old_requests():
    """清理超過一分鐘的請求記錄"""
    current_time = time.time()
    for client_ip in list(request_counts.keys()):
        request_counts[client_ip] = [
            req_time for req_time in request_counts[client_ip]
            if current_time - req_time < 60
        ]
        if not request_counts[client_ip]:
            del request_counts[client_ip]

def cleanup_old_calculations():
    """清理超過一分鐘的計算請求記錄"""
    current_time = time.time()
    for client_ip in list(calculation_counts.keys()):
        calculation_counts[client_ip] = [
            req_time for req_time in calculation_counts[client_ip]
            if current_time - req_time < 60
        ]
        if not calculation_counts[client_ip]:
            del calculation_counts[client_ip]

def validate_request_data(data, required_fields):
    """驗證請求資料"""
    missing_fields = []
    invalid_fields = []
    
    def safe_float_check(val):
        """安全轉換為float並檢查"""
        if val is None or val == '':
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None
    
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
            continue
            
        value = data[field]
        
        # 對於字符串類型的選擇字段，直接檢查不為空
        if field in ['monetizationModel', 'purchaseType', 'loanOrigin', 'buildingStructure']:
            if not value or value.strip() == '':
                invalid_fields.append(f"{field} 不能為空")
            continue
        
        # 檢查數值範圍
        if field.endswith('Ratio') or field.endswith('Rate'):
            num_value = safe_float_check(value)
            if num_value is None:
                invalid_fields.append(f"{field} 必須是有效數值")
            elif num_value < 0 or num_value > 100:
                invalid_fields.append(f"{field} 必須在 0-100 之間")
        
        elif field.endswith('Price') or field.endswith('Cost') or field.endswith('Amount'):
            num_value = safe_float_check(value)
            if num_value is None:
                invalid_fields.append(f"{field} 必須是有效數值")
            elif num_value < 0:
                invalid_fields.append(f"{field} 必須大於等於 0")
    
    errors = []
    if missing_fields:
        errors.append(f"缺少必要欄位: {', '.join(missing_fields)}")
    if invalid_fields:
        errors.extend(invalid_fields)
    
    return errors

def log_security_event(event_type, details, client_ip=None):
    """記錄安全事件"""
    security_log = {
        'timestamp': time.time(),
        'event_type': event_type,
        'client_ip': client_ip or request.remote_addr,
        'details': details
    }
    
    # 在生產環境應該發送到監控系統
    print(f"SECURITY EVENT: {security_log}")

def setup_cors_security(app):
    """設定 CORS 安全性"""
    from flask_cors import CORS
    
    # 根據環境設定 CORS
    environment = os.environ.get('ENVIRONMENT', 'development')
    
    if environment == 'production':
        # 生產環境：限制來源
        CORS(app, origins=ALLOWED_ORIGINS)
    else:
        # 開發/測試環境：允許所有來源
        CORS(app, origins="*") 