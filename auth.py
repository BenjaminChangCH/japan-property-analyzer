"""
日本不動產投資分析工具 - 用戶認證模組
處理 Google OAuth 2.0 登入、登出和會話管理
"""

import os
import uuid
from flask import Blueprint, request, redirect, url_for, session, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from models import db, User
import secrets

# 創建認證藍圖
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_oauth(app):
    """初始化 OAuth 配置"""
    global oauth, google
    
    oauth = OAuth(app)
    
    # 配置 Google OAuth
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        access_token_url='https://oauth2.googleapis.com/token',
        access_token_params=None,
        refresh_token_url=None,
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
    return oauth, google

# 全域變數，將在 main.py 中初始化
oauth = None
google = None

@auth_bp.route('/login')
def login():
    """開始 Google OAuth 登入流程"""
    if not google:
        return jsonify({'error': '認證服務未正確配置'}), 500
    
    # 生成隨機 state 參數防止 CSRF 攻擊
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # 設定回調 URL
    redirect_uri = url_for('auth.callback', _external=True)
    
    return google.authorize_redirect(redirect_uri, state=state)

@auth_bp.route('/callback')
def callback():
    """處理 Google OAuth 回調"""
    if not google:
        return jsonify({'error': '認證服務未正確配置'}), 500
    
    # 驗證 state 參數
    if request.args.get('state') != session.get('oauth_state'):
        flash('認證失敗：安全驗證錯誤', 'error')
        return redirect(url_for('index'))
    
    try:
        # 獲取 access token
        token = google.authorize_access_token()
        
        # 獲取用戶資訊
        user_info = token.get('userinfo')
        if not user_info:
            flash('認證失敗：無法獲取用戶資訊', 'error')
            return redirect(url_for('index'))
        
        # 檢查用戶是否已存在
        user = User.query.filter_by(google_id=user_info['sub']).first()
        
        if not user:
            # 創建新用戶
            user = User(
                id=str(uuid.uuid4()),
                google_id=user_info['sub'],
                email=user_info['email'],
                name=user_info['name'],
                avatar_url=user_info.get('picture', '')
            )
            db.session.add(user)
            db.session.commit()
            flash(f'歡迎加入！{user.name}', 'success')
        else:
            # 更新現有用戶資訊
            user.name = user_info['name']
            user.avatar_url = user_info.get('picture', '')
            db.session.commit()
            flash(f'歡迎回來！{user.name}', 'success')
        
        # 登入用戶
        login_user(user, remember=True)
        
        # 清除 OAuth state
        session.pop('oauth_state', None)
        
        # 重定向到原本要訪問的頁面或首頁
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index'))
        
    except Exception as e:
        flash(f'登入失敗：{str(e)}', 'error')
        return redirect(url_for('index'))

@auth_bp.route('/logout')
@login_required
def logout():
    """用戶登出"""
    user_name = current_user.name
    logout_user()
    flash(f'再見！{user_name}', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """用戶個人資料頁面"""
    return jsonify(current_user.to_dict())

@auth_bp.route('/profile', methods=['POST'])
@login_required
def update_profile():
    """更新用戶個人資料"""
    try:
        data = request.get_json()
        
        # 更新用戶偏好設定
        if 'preferences' in data:
            current_user.set_preferences(data['preferences'])
            db.session.commit()
            return jsonify({'message': '偏好設定已更新', 'user': current_user.to_dict()})
        
        return jsonify({'error': '無效的請求資料'}), 400
        
    except Exception as e:
        return jsonify({'error': f'更新失敗：{str(e)}'}), 500

@auth_bp.route('/status')
def status():
    """檢查用戶登入狀態"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        })
    else:
        return jsonify({
            'authenticated': False,
            'user': None
        })

# 用戶載入回調函數
def load_user(user_id):
    """Flask-Login 用戶載入回調"""
    return User.query.get(user_id)

# 未授權訪問處理
def unauthorized():
    """處理未授權訪問"""
    if request.is_json:
        return jsonify({'error': '需要登入才能訪問此功能'}), 401
    else:
        flash('請先登入才能使用此功能', 'warning')
        return redirect(url_for('auth.login', next=request.url)) 