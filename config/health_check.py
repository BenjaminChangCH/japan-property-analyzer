#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康檢查和監控系統
"""

import os
import time
import psutil
import requests
from datetime import datetime, timedelta
from version import get_version_info

class HealthChecker:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        self.last_errors = []
        
    def record_request(self):
        """記錄請求"""
        self.request_count += 1
    
    def record_error(self, error):
        """記錄錯誤"""
        self.error_count += 1
        self.last_errors.append({
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(error)
        })
        
        # 只保留最近 10 個錯誤
        if len(self.last_errors) > 10:
            self.last_errors = self.last_errors[-10:]
    
    def get_system_metrics(self):
        """獲取系統指標"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_available': memory.available,
                'disk_usage': disk.percent,
                'disk_free': disk.free
            }
        except Exception as e:
            return {'error': f'無法獲取系統指標: {str(e)}'}
    
    def get_application_metrics(self):
        """獲取應用程式指標"""
        uptime = time.time() - self.start_time
        
        return {
            'uptime_seconds': uptime,
            'uptime_human': str(timedelta(seconds=int(uptime))),
            'total_requests': self.request_count,
            'total_errors': self.error_count,
            'error_rate': (self.error_count / max(self.request_count, 1)) * 100,
            'last_errors': self.last_errors[-5:]  # 最近 5 個錯誤
        }
    
    def get_environment_info(self):
        """獲取環境資訊"""
        return {
            'environment': os.environ.get('ENVIRONMENT', 'unknown'),
            'ga_tracking_id': os.environ.get('GA_TRACKING_ID', 'not_set'),
            'build_number': os.environ.get('BUILD_NUMBER', 'unknown'),
            'k_service': os.environ.get('K_SERVICE', 'not_cloud_run'),
            'k_revision': os.environ.get('K_REVISION', 'unknown')
        }
    
    def check_external_dependencies(self):
        """檢查外部依賴"""
        dependencies = {}
        
        # 檢查 Google Analytics
        try:
            response = requests.get(
                'https://www.google-analytics.com/analytics.js',
                timeout=5
            )
            dependencies['google_analytics'] = {
                'status': 'ok' if response.status_code == 200 else 'error',
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            dependencies['google_analytics'] = {
                'status': 'error',
                'error': str(e)
            }
        
        return dependencies
    
    def get_health_status(self):
        """獲取完整健康狀態"""
        try:
            system_metrics = self.get_system_metrics()
            app_metrics = self.get_application_metrics()
            env_info = self.get_environment_info()
            dependencies = self.check_external_dependencies()
            version_info = get_version_info()
            
            # 判斷整體健康狀態
            is_healthy = True
            issues = []
            
            # 檢查 CPU 使用率
            if 'cpu_usage' in system_metrics and system_metrics['cpu_usage'] > 80:
                is_healthy = False
                issues.append(f"CPU 使用率過高: {system_metrics['cpu_usage']:.1f}%")
            
            # 檢查記憶體使用率
            if 'memory_usage' in system_metrics and system_metrics['memory_usage'] > 90:
                is_healthy = False
                issues.append(f"記憶體使用率過高: {system_metrics['memory_usage']:.1f}%")
            
            # 檢查錯誤率
            if app_metrics['error_rate'] > 5:  # 錯誤率超過 5%
                is_healthy = False
                issues.append(f"錯誤率過高: {app_metrics['error_rate']:.1f}%")
            
            # 檢查外部依賴
            for dep_name, dep_status in dependencies.items():
                if dep_status['status'] != 'ok':
                    issues.append(f"外部依賴異常: {dep_name}")
            
            return {
                'status': 'healthy' if is_healthy else 'unhealthy',
                'timestamp': datetime.utcnow().isoformat(),
                'version': version_info,
                'system': system_metrics,
                'application': app_metrics,
                'environment': env_info,
                'dependencies': dependencies,
                'issues': issues
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }

# 全域健康檢查器實例
health_checker = HealthChecker()

def setup_health_endpoints(app):
    """設定健康檢查端點"""
    
    @app.route('/health')
    def health_check():
        """簡單健康檢查"""
        return {'status': 'ok', 'timestamp': datetime.utcnow().isoformat()}
    
    @app.route('/health/detailed')
    def detailed_health_check():
        """詳細健康檢查"""
        return health_checker.get_health_status()
    
    @app.route('/health/live')
    def liveness_probe():
        """Kubernetes liveness probe"""
        return {'status': 'alive', 'uptime': time.time() - health_checker.start_time}
    
    @app.route('/health/ready')
    def readiness_probe():
        """Kubernetes readiness probe"""
        health_status = health_checker.get_health_status()
        
        if health_status['status'] == 'healthy':
            return {'status': 'ready'}
        else:
            return {'status': 'not_ready', 'issues': health_status.get('issues', [])}, 503

def setup_request_tracking(app):
    """設定請求追蹤"""
    
    @app.before_request
    def before_request():
        health_checker.record_request()
    
    @app.errorhandler(Exception)
    def track_errors(error):
        health_checker.record_error(error)
        raise 