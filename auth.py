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
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
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
    
    # 設定回調 URL - 根據環境決定協議
    import os
    environment = os.getenv('ENVIRONMENT', 'development')
    if environment == 'development':
        # 開發環境使用 HTTP
        redirect_uri = url_for('auth.callback', _external=True, _scheme='http')
    else:
        # 生產環境使用 HTTPS
        redirect_uri = url_for('auth.callback', _external=True, _scheme='https')
    
    return google.authorize_redirect(redirect_uri, state=state)

@auth_bp.route('/callback')
def callback():
    """處理 Google OAuth 回調"""
    from flask import current_app
    
    current_app.logger.info("OAuth 回調函數開始執行")
    current_app.logger.info(f"接收到的參數: {dict(request.args)}")
    
    if not google:
        current_app.logger.error("Google OAuth 未正確配置")
        return jsonify({'error': '認證服務未正確配置'}), 500
    
    # 檢查是否有錯誤參數
    error = request.args.get('error')
    if error:
        current_app.logger.error(f"OAuth 錯誤: {error}")
        error_description = request.args.get('error_description', '')
        flash(f'登入失敗：{error_description or error}', 'error')
        return redirect(url_for('index'))
    
    # 檢查是否有授權碼
    code = request.args.get('code')
    if not code:
        current_app.logger.error("缺少授權碼")
        flash('登入失敗：缺少授權碼', 'error')
        return redirect(url_for('index'))
    
    # 驗證 state 參數
    received_state = request.args.get('state')
    session_state = session.get('oauth_state')
    current_app.logger.info(f"State 驗證 - 接收: {received_state}, 會話: {session_state}")
    
    if received_state != session_state:
        current_app.logger.error("State 參數驗證失敗")
        flash('認證失敗：安全驗證錯誤', 'error')
        return redirect(url_for('index'))
    
    try:
        current_app.logger.info("開始獲取 access token")
        # 獲取 access token
        token = google.authorize_access_token()
        current_app.logger.info(f"Token 獲取成功: {bool(token)}")
        
        # 獲取用戶資訊
        user_info = token.get('userinfo')
        current_app.logger.info(f"用戶資訊: {user_info}")
        
        if not user_info:
            current_app.logger.error("無法獲取用戶資訊")
            flash('認證失敗：無法獲取用戶資訊', 'error')
            return redirect(url_for('index'))
        
        # 檢查用戶是否已存在
        google_id = user_info['sub']
        user = User.query.filter_by(google_id=google_id).first()
        current_app.logger.info(f"檢查現有用戶 (Google ID: {google_id}): {bool(user)}")
        
        if not user:
            # 創建新用戶
            current_app.logger.info("創建新用戶")
            user = User(
                id=str(uuid.uuid4()),
                google_id=user_info['sub'],
                email=user_info['email'],
                name=user_info['name'],
                avatar_url=user_info.get('picture', '')
            )
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(f"新用戶創建成功: {user.email}")
            flash(f'歡迎加入！{user.name}', 'success')
        else:
            # 更新現有用戶資訊
            current_app.logger.info("更新現有用戶資訊")
            user.name = user_info['name']
            user.avatar_url = user_info.get('picture', '')
            db.session.commit()
            current_app.logger.info(f"用戶資訊更新成功: {user.email}")
            flash(f'歡迎回來！{user.name}', 'success')
        
        # 登入用戶
        current_app.logger.info("執行用戶登入")
        # Flask-Login 會自動處理認證狀態，不需要手動設置
        login_result = login_user(user, remember=True, duration=None, force=False, fresh=True)
        current_app.logger.info(f"登入結果: {login_result}")
        current_app.logger.info(f"會話中的用戶: {session.get('_user_id', 'None')}")
        
        # 清除 OAuth state
        session.pop('oauth_state', None)
        
        # 重定向到原本要訪問的頁面或首頁，並添加登入成功參數
        next_page = request.args.get('next')
        redirect_url = next_page if next_page else url_for('index', login='success')
        current_app.logger.info(f"準備重定向到: {redirect_url}")
        
        return redirect(redirect_url)
        
    except Exception as e:
        current_app.logger.error(f"OAuth 回調處理發生錯誤: {str(e)}", exc_info=True)
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
    from flask import current_app, session
    
    current_app.logger.info(f"檢查認證狀態 - current_user: {current_user}")
    current_app.logger.info(f"current_user.is_authenticated: {current_user.is_authenticated}")
    current_app.logger.info(f"會話資料: {dict(session)}")
    
    if current_user.is_authenticated:
        current_app.logger.info(f"用戶已認證: {current_user.email}")
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        })
    else:
        current_app.logger.info("用戶未認證")
        return jsonify({
            'authenticated': False,
            'user': None
        })

# 用戶載入回調函數
def load_user(user_id):
    """Flask-Login 用戶載入回調"""
    from flask import current_app
    current_app.logger.info(f"load_user 被調用，用戶ID: {user_id}")
    
    try:
        user = User.query.get(user_id)
        current_app.logger.info(f"load_user 結果: {user.email if user else None}")
        return user
    except Exception as e:
        current_app.logger.error(f"load_user 錯誤: {str(e)}")
        return None

# 未授權訪問處理
def unauthorized():
    """處理未授權訪問"""
    if request.is_json:
        return jsonify({'error': '需要登入才能訪問此功能'}), 401
    else:
        flash('請先登入才能使用此功能', 'warning')
        return redirect(url_for('auth.login', next=request.url)) 