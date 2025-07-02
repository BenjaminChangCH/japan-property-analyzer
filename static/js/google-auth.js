/**
 * Google OAuth Authentication Module
 * 獨立的 Google 登入功能模組，避免與主程式碼耦合
 * 
 * @author Benjamin Chang
 * @version 1.0.0
 * @date 2025-07-02
 */

class GoogleAuthManager {
    constructor() {
        this.isInitialized = false;
        this.clientId = null;
        this.currentUser = null;
        this.config = {
            auto_select: false,
            cancel_on_tap_outside: true,
            use_fedcm_for_prompt: false,  // 暫時禁用 FedCM 以避免兼容性問題
            ux_mode: 'popup',
            context: 'signin',
            itp_support: true
        };
        
        // 綁定 this 上下文
        this.handleSignIn = this.handleSignIn.bind(this);
        this.logout = this.logout.bind(this);
    }

    /**
     * 初始化 Google OAuth
     */
    async init() {
        try {
            // 檢查 Google SDK 是否載入
            if (!this.isGoogleSDKLoaded()) {
                console.warn('Google Identity Services SDK 尚未載入');
                setTimeout(() => this.init(), 1000);
                return false;
            }

            // 獲取 Client ID
            this.clientId = this.getClientId();
            if (!this.clientId) {
                this.showSetupInstructions();
                return false;
            }

            // 初始化 Google OAuth
            google.accounts.id.initialize({
                client_id: this.clientId,
                callback: this.handleSignIn,
                ...this.config
            });

            this.isInitialized = true;
            this.setupEventListeners();
            this.checkExistingAuth();
            
            console.log('Google OAuth 初始化成功');
            return true;

        } catch (error) {
            console.error('Google OAuth 初始化失敗:', error);
            this.showError('初始化失敗', error.message);
            return false;
        }
    }

    /**
     * 檢查 Google SDK 是否載入
     */
    isGoogleSDKLoaded() {
        return typeof google !== 'undefined' && 
               google.accounts && 
               google.accounts.id;
    }

    /**
     * 獲取 Google Client ID
     */
    getClientId() {
        // 1. 從全域變數獲取
        if (typeof GOOGLE_CLIENT_ID !== 'undefined' && GOOGLE_CLIENT_ID) {
            return GOOGLE_CLIENT_ID;
        }
        
        // 2. 從 meta 標籤獲取
        const metaClientId = document.querySelector('meta[name="google-client-id"]');
        if (metaClientId && metaClientId.content && metaClientId.content !== 'YOUR_GOOGLE_CLIENT_ID') {
            return metaClientId.content;
        }
        
        // 3. 從環境變數獲取（如果後端有傳入）
        if (typeof window.googleClientId !== 'undefined' && window.googleClientId) {
            return window.googleClientId;
        }
        
        return null;
    }

    /**
     * 設置事件監聽器
     */
    setupEventListeners() {
        // 嘗試使用 Google 的原生按鈕渲染
        this.setupGoogleButtons();

        // 導航列登出按鈕
        const headerLogoutBtn = document.getElementById('logoutBtnHeader');
        if (headerLogoutBtn) {
            headerLogoutBtn.addEventListener('click', () => this.logout());
        }

        // 分析頁面登出按鈕
        const analysisLogoutBtn = document.getElementById('logoutBtn');
        if (analysisLogoutBtn) {
            analysisLogoutBtn.addEventListener('click', () => this.logout());
        }
    }

    /**
     * 設置 Google 原生登入按鈕
     */
    setupGoogleButtons() {
        try {
            // 為導航列按鈕創建 Google 原生按鈕
            const headerBtn = document.getElementById('googleLoginBtnHeader');
            if (headerBtn && google.accounts.id.renderButton) {
                // 創建一個隱藏的容器來放置 Google 按鈕
                const hiddenContainer = document.createElement('div');
                hiddenContainer.style.position = 'absolute';
                hiddenContainer.style.left = '-9999px';
                hiddenContainer.id = 'google-signin-header';
                document.body.appendChild(hiddenContainer);

                google.accounts.id.renderButton(hiddenContainer, {
                    theme: 'outline',
                    size: 'medium',
                    type: 'standard',
                    text: 'signin_with',
                    shape: 'rectangular',
                    logo_alignment: 'left'
                });

                // 點擊自定義按鈕時觸發 Google 按鈕
                headerBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    const googleBtn = hiddenContainer.querySelector('div[role="button"]');
                    if (googleBtn) {
                        googleBtn.click();
                    } else {
                        this.login();
                    }
                });
            }

            // 為分析頁面按鈕做同樣的處理
            const analysisBtn = document.getElementById('googleLoginBtn');
            if (analysisBtn && google.accounts.id.renderButton) {
                const hiddenContainer2 = document.createElement('div');
                hiddenContainer2.style.position = 'absolute';
                hiddenContainer2.style.left = '-9999px';
                hiddenContainer2.id = 'google-signin-analysis';
                document.body.appendChild(hiddenContainer2);

                google.accounts.id.renderButton(hiddenContainer2, {
                    theme: 'outline',
                    size: 'medium',
                    type: 'standard',
                    text: 'signin_with',
                    shape: 'rectangular',
                    logo_alignment: 'left'
                });

                analysisBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    const googleBtn = hiddenContainer2.querySelector('div[role="button"]');
                    if (googleBtn) {
                        googleBtn.click();
                    } else {
                        this.login();
                    }
                });
            }

        } catch (error) {
            console.warn('無法設置 Google 原生按鈕，使用備用方案:', error);
        }
    }

    /**
     * 執行登入
     */
    login() {
        if (!this.isInitialized) {
            this.showError('登入失敗', '系統尚未初始化，請稍後再試');
            return;
        }

        try {
            console.log('開始 Google 登入流程...');
            
            // 直接使用 Google 登入提示
            google.accounts.id.prompt((notification) => {
                console.log('Google 登入提示狀態:', notification);
                
                if (notification.isNotDisplayed()) {
                    const reason = notification.getNotDisplayedReason();
                    console.log('登入提示未顯示，原因:', reason);
                    this.handleLoginPromptError(reason);
                } else if (notification.isSkippedMoment()) {
                    const reason = notification.getSkippedReason();
                    console.log('登入提示被跳過，原因:', reason);
                    this.handleLoginPromptError(reason);
                }
            });
        } catch (error) {
            console.error('Google 登入錯誤:', error);
            this.showError('登入失敗', '請檢查網路連接並重試');
        }
    }

    /**
     * 重新嘗試登入
     */
    retryLogin() {
        console.log('重新嘗試 Google 登入...');
        
        // 等待一秒後重試
        setTimeout(() => {
            this.login();
        }, 1000);
    }

    /**
     * 執行登出
     */
    logout() {
        try {
            // 清除本地存儲
            localStorage.removeItem('googleUser');
            this.currentUser = null;

            // 更新 UI
            this.updateUI(false);

            // Google Analytics 追蹤
            this.trackEvent('logout');

            console.log('已登出 Google 帳戶');
            
        } catch (error) {
            console.error('登出錯誤:', error);
        }
    }

    /**
     * 處理登入成功
     */
    handleSignIn(response) {
        try {
            // 解析 JWT token
            const payload = JSON.parse(atob(response.credential.split('.')[1]));
            console.log('解析的 Google 用戶數據:', payload);
            
            this.currentUser = {
                name: payload.name,
                email: payload.email,
                picture: payload.picture,
                credential: response.credential
            };

            console.log('設置的 currentUser:', this.currentUser);

            // 儲存到本地存儲
            localStorage.setItem('googleUser', JSON.stringify(this.currentUser));

            // 更新 UI
            this.updateUI(true);

            // Google Analytics 追蹤
            this.trackEvent('login');

            console.log('Google 登入成功，用戶:', this.currentUser.name, '頭像URL:', this.currentUser.picture);

            // 觸發自定義事件
            this.dispatchEvent('auth:login', this.currentUser);
            
        } catch (error) {
            console.error('Google 登入處理錯誤:', error);
            this.showError('登入處理失敗', '請稍後再試');
        }
    }

    /**
     * 檢查現有的登入狀態
     */
    checkExistingAuth() {
        try {
            const savedUser = localStorage.getItem('googleUser');
            if (savedUser) {
                this.currentUser = JSON.parse(savedUser);
                console.log('從本地存儲載入的用戶數據:', this.currentUser);
                this.updateUI(true);
                console.log('檢測到已登入的用戶:', this.currentUser.name, '頭像URL:', this.currentUser.picture);
            } else {
                console.log('本地存儲中沒有用戶數據');
            }
        } catch (error) {
            console.error('檢查登入狀態失敗:', error);
            localStorage.removeItem('googleUser');
        }
    }

    /**
     * 更新 UI 顯示
     */
    updateUI(isLoggedIn) {
        console.log('updateUI 被調用，isLoggedIn:', isLoggedIn, 'currentUser:', this.currentUser);
        
        if (isLoggedIn && this.currentUser) {
            // 導航列
            this.hideElement('googleLoginBtnHeader');
            this.showElement('userInfoHeader');
            
            // 更新用戶頭像 - 找到 img 元素並設置 src
            const avatarImg = document.querySelector('#userAvatarHeader');
            console.log('找到頭像元素:', avatarImg);
            console.log('用戶圖片URL:', this.currentUser.picture);
            
            if (avatarImg) {
                if (this.currentUser.picture) {
                    avatarImg.src = this.currentUser.picture;
                    avatarImg.alt = `${this.currentUser.name}的頭像`;
                    avatarImg.style.display = 'block';
                    
                    // 添加載入錯誤處理
                    avatarImg.onerror = function() {
                        console.warn('用戶頭像載入失敗，URL:', this.src);
                        this.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTYiIGZpbGw9IiNGM0Y0RjYiLz4KPGNpcmNsZSBjeD0iMTYiIGN5PSIxMiIgcj0iNSIgZmlsbD0iIzlDQTNBRiIvPgo8cGF0aCBkPSJNNiAyNmMwLTUuNTIzIDQuNDc3LTEwIDEwLTEwczEwIDQuNDc3IDEwIDEwIiBmaWxsPSIjOUNBM0FGIi8+Cjwvc3ZnPgo=';
                    };
                    
                    avatarImg.onload = function() {
                        console.log('用戶頭像載入成功:', this.src);
                    };
                    
                    console.log('用戶頭像已設置:', this.currentUser.picture);
                } else {
                    console.warn('用戶沒有圖片URL，使用預設頭像');
                    avatarImg.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTYiIGZpbGw9IiNGM0Y0RjYiLz4KPGNpcmNsZSBjeD0iMTYiIGN5PSIxMiIgcj0iNSIgZmlsbD0iIzlDQTNBRiIvPgo8cGF0aCBkPSJNNiAyNmMwLTUuNTIzIDQuNDc3LTEwIDEwLTEwczEwIDQuNDc3IDEwIDEwIiBmaWxsPSIjOUNBM0FGIi8+Cjwvc3ZnPgo=';
                    avatarImg.alt = '預設頭像';
                }
            } else {
                console.error('無法找到用戶頭像元素 #userAvatarHeader');
            }
            
            this.updateElement('userNameHeader', 'textContent', this.currentUser.name);

            // 分析頁面 - 隱藏整個登入區域
            this.hideElement('loginSection');
            
            // 如果有單獨的用戶信息區域，也更新它（備用）
            this.hideElement('googleLoginBtn');
            this.showElement('userInfo');
            this.updateElement('userAvatar', 'src', this.currentUser.picture);
            this.updateElement('userName', 'textContent', this.currentUser.name);
            this.updateElement('userEmail', 'textContent', this.currentUser.email);
        } else {
            // 導航列
            this.showElement('googleLoginBtnHeader');
            this.hideElement('userInfoHeader');

            // 分析頁面 - 顯示登入區域
            this.showElement('loginSection');
            this.showElement('googleLoginBtn');
            this.hideElement('userInfo');
        }
    }

    /**
     * 工具方法：隱藏元素
     */
    hideElement(id) {
        const element = document.getElementById(id);
        if (element) element.classList.add('hidden');
    }

    /**
     * 工具方法：顯示元素
     */
    showElement(id) {
        const element = document.getElementById(id);
        if (element) element.classList.remove('hidden');
    }

    /**
     * 工具方法：更新元素屬性
     */
    updateElement(id, property, value) {
        const element = document.getElementById(id);
        if (element && value) {
            element[property] = value;
        }
    }

    /**
     * 處理登入提示錯誤
     */
    handleLoginPromptError(reason) {
        console.error('Google 登入錯誤原因:', reason);
        
        switch (reason) {
            case 'browser_not_supported':
                this.showError('瀏覽器不支援', '請使用現代瀏覽器（Chrome、Firefox、Safari、Edge）');
                break;
            case 'invalid_client':
                this.showError('OAuth 設定錯誤', 
                    `Client ID 無效或未正確設定。\n\n` +
                    `請檢查：\n` +
                    `1. Google Cloud Console 中的 Client ID 是否正確\n` +
                    `2. 是否已添加 ${window.location.origin} 到授權的 JavaScript 來源\n` +
                    `3. OAuth 同意畫面是否已設定\n\n` +
                    `當前 Client ID: ${this.getClientId()}`);
                break;
            case 'missing_client_id':
                this.showError('缺少 Client ID', '請聯絡開發者設定 Google OAuth Client ID');
                break;
            case 'opt_out_or_no_session':
                this.showError('需要授權', '請點擊登入按鈕並選擇您的 Google 帳戶進行授權');
                break;
            case 'secure_http_required':
                this.showError('需要安全連接', '請使用 HTTPS 或 localhost 訪問此網站');
                break;
            case 'suppressed_by_user':
                this.showError('登入被取消', '您取消了登入，請重新點擊登入按鈕');
                break;
            case 'unregistered_origin':
                this.showError('網域未授權', 
                    `當前網域未在 Google Cloud Console 中授權。\n\n` +
                    `請在 Google Cloud Console 的 OAuth 設定中添加：\n` +
                    `${window.location.origin}\n\n` +
                    `到「授權的 JavaScript 來源」列表中。`);
                break;
            case 'unknown_reason':
            default:
                this.showError('登入失敗', 
                    `未知錯誤，請嘗試：\n` +
                    `1. 重新整理頁面\n` +
                    `2. 清除瀏覽器快取\n` +
                    `3. 檢查網路連接\n` +
                    `4. 如問題持續，請聯絡技術支援`);
                break;
        }
    }

    /**
     * 顯示設置說明
     */
    showSetupInstructions() {
        if (this.isDevelopmentMode()) {
            console.info(`
=== Google OAuth 設置說明 ===

要啟用 Google 登入功能，請：

1. 前往 Google Cloud Console: https://console.cloud.google.com/
2. 創建新專案或選擇現有專案
3. 啟用 Google Identity Services API
4. 創建 OAuth 2.0 客戶端 ID
5. 將 Client ID 設置為 HTML meta 標籤

設置方式：
<meta name="google-client-id" content="您的真實Client ID">

⚠️ FedCM 問題解決方案：
- 在瀏覽器地址欄左側點擊鎖頭圖示
- 選擇「網站設定」
- 啟用「第三方登入」選項

詳細說明請參考：docs/GOOGLE_OAUTH_SETUP_GUIDE.md
            `);
            
            // 顯示友善的用戶提示
            this.showFriendlySetupMessage();
        }
    }

    /**
     * 顯示友善的設置訊息
     */
    showFriendlySetupMessage() {
        const message = `
🔧 Google 登入設置中...

這是開發環境，需要設置 Google OAuth Client ID 才能使用登入功能。

目前您仍可以使用所有分析功能，只是無法儲存結果到雲端。

如需啟用登入功能，請參考控制台中的設置說明。
        `.trim();
        
        // 使用溫和的提示方式
        console.log('%c' + message, 'color: #4285f4; font-size: 12px;');
    }

    /**
     * 顯示錯誤訊息
     */
    showError(title, message) {
        console.error(`${title}: ${message}`);
        
        if (this.isDevelopmentMode()) {
            // 開發模式：顯示詳細錯誤
            alert(`${title}\n\n${message}\n\n請檢查控制台獲取更多資訊。`);
        } else {
            // 生產模式：顯示友善訊息
            alert('Google 登入暫時無法使用，請稍後再試。');
        }
    }

    /**
     * 檢查是否為開發模式
     */
    isDevelopmentMode() {
        return window.location.hostname === 'localhost' || 
               window.location.hostname === '127.0.0.1' ||
               window.location.hostname.includes('localhost');
    }

    /**
     * Google Analytics 事件追蹤
     */
    trackEvent(action) {
        if (typeof gtag === 'function') {
            gtag('event', action, {
                'method': 'Google',
                'event_category': 'User Authentication'
            });
        }
    }

    /**
     * 觸發自定義事件
     */
    dispatchEvent(eventName, data) {
        const event = new CustomEvent(eventName, {
            detail: data
        });
        window.dispatchEvent(event);
    }

    /**
     * 獲取當前用戶
     */
    getCurrentUser() {
        return this.currentUser;
    }

    /**
     * 檢查是否已登入
     */
    isLoggedIn() {
        return this.currentUser !== null;
    }

    /**
     * 檢查是否已初始化
     */
    getInitializationStatus() {
        return this.isInitialized;
    }

    /**
     * 儲存分析結果（如果用戶已登入）
     */
    saveAnalysisResults(results) {
        if (!this.isLoggedIn()) {
            return false;
        }

        try {
            const analysisHistory = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
            
            const analysisRecord = {
                timestamp: new Date().toISOString(),
                user: {
                    name: this.currentUser.name,
                    email: this.currentUser.email
                },
                results: results,
                id: Date.now().toString()
            };

            analysisHistory.unshift(analysisRecord);
            
            // 保留最近 10 次分析
            if (analysisHistory.length > 10) {
                analysisHistory.splice(10);
            }

            localStorage.setItem('analysisHistory', JSON.stringify(analysisHistory));
            console.log('分析結果已儲存');
            return true;
            
        } catch (error) {
            console.error('儲存分析結果失敗:', error);
            return false;
        }
    }
}

// 創建全域實例
window.GoogleAuth = new GoogleAuthManager();

// 等待 Google SDK 載入完成後初始化
function initGoogleAuthWhenReady() {
    if (typeof google !== 'undefined' && google.accounts && google.accounts.id) {
        // Google SDK 已載入，立即初始化
        window.GoogleAuth.init();
    } else {
        // Google SDK 尚未載入，繼續等待
        setTimeout(initGoogleAuthWhenReady, 200);
    }
}

// 當 DOM 載入完成後開始檢查 Google SDK
document.addEventListener('DOMContentLoaded', () => {
    initGoogleAuthWhenReady();
});

// 也監聽 window load 事件作為備用
window.addEventListener('load', () => {
    // 如果 DOM ready 時沒有成功初始化，再試一次
    if (!window.GoogleAuth.getInitializationStatus()) {
        setTimeout(initGoogleAuthWhenReady, 1000);
    }
});

// 導出供其他模組使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GoogleAuthManager;
} 