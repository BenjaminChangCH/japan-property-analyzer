"""
Google OAuth 認證功能測試
測試用戶登入、登出、會話管理等功能
"""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from flask import url_for
from main import create_app
from models import db, User
import uuid

class AuthTestCase(unittest.TestCase):
    """認證功能測試案例"""
    
    def setUp(self):
        """測試前準備"""
        # 創建臨時資料庫
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # 設定測試環境變數
        os.environ['DATABASE_URL'] = f'sqlite:///{self.db_path}'
        os.environ['SECRET_KEY'] = 'test-secret-key'
        os.environ['GOOGLE_CLIENT_ID'] = 'test-client-id'
        os.environ['GOOGLE_CLIENT_SECRET'] = 'test-client-secret'
        
        # 創建測試應用
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        
        # 創建資料庫表
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """測試後清理"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_login_redirect(self):
        """測試登入重定向"""
        response = self.client.get('/auth/login')
        # 應該重定向到 Google OAuth
        self.assertEqual(response.status_code, 302)
    
    def test_auth_status_not_logged_in(self):
        """測試未登入狀態"""
        response = self.client.get('/auth/status')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertFalse(data['authenticated'])
        self.assertIsNone(data['user'])
    
    @patch('auth.google')
    def test_oauth_callback_success(self, mock_google):
        """測試 OAuth 回調成功"""
        # 模擬 Google OAuth 回應
        mock_token = {
            'userinfo': {
                'sub': 'test-google-id',
                'email': 'test@example.com',
                'name': 'Test User',
                'picture': 'https://example.com/avatar.jpg'
            }
        }
        mock_google.authorize_access_token.return_value = mock_token
        
        with self.client.session_transaction() as sess:
            sess['oauth_state'] = 'test-state'
        
        response = self.client.get('/auth/callback?state=test-state')
        self.assertEqual(response.status_code, 302)
        
        # 檢查用戶是否已創建
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'Test User')
    
    def test_profile_requires_login(self):
        """測試個人資料頁面需要登入"""
        response = self.client.get('/auth/profile')
        self.assertEqual(response.status_code, 401)
    
    def create_test_user(self):
        """創建測試用戶"""
        with self.app.app_context():
            user = User(
                id=str(uuid.uuid4()),
                google_id='test-google-id',
                email='test@example.com',
                name='Test User'
            )
            db.session.add(user)
            db.session.commit()
            return user
    
    def test_user_model_methods(self):
        """測試用戶模型方法"""
        with self.app.app_context():
            user = self.create_test_user()
            
            # 測試偏好設定
            preferences = {'theme': 'dark', 'language': 'zh-TW'}
            user.set_preferences(preferences)
            db.session.commit()
            
            retrieved_prefs = user.get_preferences()
            self.assertEqual(retrieved_prefs, preferences)
            
            # 測試 to_dict 方法
            user_dict = user.to_dict()
            self.assertEqual(user_dict['email'], 'test@example.com')
            self.assertEqual(user_dict['name'], 'Test User')

if __name__ == '__main__':
    unittest.main() 