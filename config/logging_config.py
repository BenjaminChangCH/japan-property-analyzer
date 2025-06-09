#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日誌和錯誤監控配置
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """設定應用程式日誌"""
    
    # 設定日誌等級
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    app.logger.setLevel(getattr(logging, log_level))
    
    # 移除預設的 handler
    app.logger.handlers.clear()
    
    # 建立格式化器
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # 控制台輸出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
    
    # 只在非 Cloud Run 環境寫入檔案日誌
    if not os.environ.get('K_SERVICE'):  # Cloud Run 環境變數
        # 檔案日誌（最大 10MB，保留 5 個檔案）
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        file_handler = RotatingFileHandler(
            'logs/app.log', 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    
    # 設定其他日誌器
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    
    app.logger.info(f"日誌系統已啟動 - 等級: {log_level}")

def log_error(app, error, request=None, additional_info=None):
    """統一錯誤日誌記錄"""
    error_info = {
        'timestamp': datetime.utcnow().isoformat(),
        'error_type': type(error).__name__,
        'error_message': str(error),
        'additional_info': additional_info or {}
    }
    
    if request:
        error_info.update({
            'method': request.method,
            'url': request.url,
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')
        })
    
    app.logger.error(f"錯誤詳情: {error_info}")
    
    # 在生產環境可以整合到外部監控系統
    environment = os.environ.get('ENVIRONMENT', 'development')
    if environment == 'production':
        # TODO: 整合到 Google Cloud Logging 或其他監控系統
        pass

def setup_error_handlers(app):
    """設定錯誤處理器"""
    from flask import request
    
    @app.errorhandler(404)
    def not_found_error(error):
        log_error(app, error, request=request)
        return {'error': '頁面未找到'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        log_error(app, error, request=request)
        return {'error': '伺服器內部錯誤'}, 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        log_error(app, error, request=request)
        
        # 在開發環境顯示詳細錯誤
        if app.debug:
            return {'error': str(error)}, 500
        else:
            return {'error': '伺服器發生錯誤，請稍後再試'}, 500 