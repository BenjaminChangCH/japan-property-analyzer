// 用戶認證相關函數
let currentUser = null;

// 臨時測試函數 - 模擬用戶登入狀態
function testUserMode() {
    const testUser = {
        name: 'ChunHao Chang',
        avatar_url: 'https://lh3.googleusercontent.com/a/ACg8ocIa-osqIhhCfm_jr8E_-Mc23g9WlNY4FLMdM31C1JZ3rfPW2A=s96-c',
        email: 'benjamin.chang10@gmail.com'
    };
    
    console.log('測試用戶模式，設置頭像:', testUser.avatar_url);
    showUserMode(testUser);
}

// 檢查用戶登入狀態
async function checkAuthStatus() {
    try {
        const response = await fetch('/auth/status');
        const data = await response.json();
        
        if (data.authenticated) {
            currentUser = data.user;
            showUserMode(data.user);
            
            // 如果是剛登入，顯示成功提示
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('login') === 'success') {
                showLoginSuccessToast(data.user.name);
                // 清除 URL 參數
                window.history.replaceState({}, document.title, window.location.pathname);
            }
        } else {
            currentUser = null;
            showGuestMode();
        }
    } catch (error) {
        console.error('檢查認證狀態失敗:', error);
        showGuestMode();
    }
}

// 顯示用戶模式
function showUserMode(user) {
    console.log('顯示用戶模式，用戶資料:', user);
    
    document.getElementById('guestMode').classList.add('hidden');
    document.getElementById('userMode').classList.remove('hidden');
    document.getElementById('userName').textContent = user.name;
    
    const avatarElement = document.getElementById('userAvatar');
    const avatarUrl = user.avatar_url || '/static/images/default-avatar.svg';
    
    console.log('設置頭像 URL:', avatarUrl);
    console.log('頭像元素:', avatarElement);
    
    if (avatarElement) {
        // 防止無限重試的標誌
        let hasTriedDefault = false;
        
        avatarElement.src = avatarUrl;
        avatarElement.onerror = function() {
            if (!hasTriedDefault && this.src !== '/static/images/default-avatar.svg') {
                console.log('頭像載入失敗，嘗試使用預設頭像');
                hasTriedDefault = true;
                this.src = '/static/images/default-avatar.svg';
            } else {
                // 如果預設頭像也失敗，使用文字頭像
                console.log('預設頭像也載入失敗，使用文字頭像');
                this.style.display = 'none';
                const textAvatar = document.createElement('div');
                textAvatar.className = 'text-avatar';
                textAvatar.style.cssText = 'width: 32px; height: 32px; background: #3b82f6; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; color: white; font-weight: bold;';
                textAvatar.textContent = user.name ? user.name.charAt(0).toUpperCase() : 'U';
                this.parentNode.insertBefore(textAvatar, this);
            }
        };
        avatarElement.onload = function() {
            console.log('頭像載入成功:', this.src);
        };
    } else {
        console.error('找不到 userAvatar 元素');
    }
}

// 顯示訪客模式
function showGuestMode() {
    document.getElementById('guestMode').classList.remove('hidden');
    document.getElementById('userMode').classList.add('hidden');
}

// 顯示登入成功提示
function showLoginSuccessToast(userName) {
    const toast = document.getElementById('loginSuccessToast');
    const toastText = toast.querySelector('span:last-child');
    toastText.textContent = `登入成功！歡迎回來，${userName}`;
    
    toast.classList.add('show');
    
    // 3秒後自動隱藏
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Google 登入
function login(event) {
    console.log('登入按鈕被點擊');
    
    // 防止表單提交或其他預設行為
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    try {
        console.log('正在重定向到 Google 登入頁面...');
        window.location.href = '/auth/login';
    } catch (error) {
        console.error('登入重定向失敗:', error);
        alert('登入功能暫時無法使用，請稍後再試');
    }
}

// 登出
function logout() {
    if (confirm('確定要登出嗎？')) {
        window.location.href = '/auth/logout';
    }
}

// 顯示用戶選單
function showUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    dropdown.classList.toggle('hidden');
}

// 顯示個人資料
function showProfile() {
    const dropdown = document.getElementById('userDropdown');
    dropdown.classList.add('hidden');
    alert('個人資料管理功能開發中...\n\n將包含以下功能：\n• 編輯個人資訊\n• 修改偏好設定\n• 查看登入記錄');
}

// 顯示我的案件
function showProperties() {
    const dropdown = document.getElementById('userDropdown');
    dropdown.classList.add('hidden');
    alert('案件管理功能開發中...\n\n將包含以下功能：\n• 儲存分析案件\n• 案件比較分析\n• 投資組合管理\n• 收藏案件追蹤');
}

// 點擊其他地方時隱藏下拉選單
document.addEventListener('click', function(event) {
    const userMenu = document.querySelector('.user-menu');
    const dropdown = document.getElementById('userDropdown');
    
    if (userMenu && !userMenu.contains(event.target)) {
        dropdown.classList.add('hidden');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // 初始化認證狀態
    checkAuthStatus();
    
    // 綁定 Google 登入按鈕事件
    const googleLoginBtn = document.getElementById('googleLoginBtn');
    if (googleLoginBtn) {
        googleLoginBtn.addEventListener('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            login(event);
        });
    }
    const expertValues = {
        propertyTypes: {
            '1LDK': {
                priceModifier: 1,
                rentModifier: 1,
                adrModifier: 1,
                structure: 'rc',
                buildingRatio: 65,
                maxOccupancy: 4,
                managementFeeRatio: 12.5,
                utilitiesAirbnb: 2.5,
                utilitiesLease: 0.5,
                managementFeeTooltip: '1LDK公寓的管理費與修繕金佔比較高，通常在10-15%。',
                structureTooltip: '1LDK通常為RC/SRC構造，法定耐用年限47年。',
                buildingRatioTooltip: '中小型公寓的建物價值佔比約60-70%。'
            },
            '2LDK': {
                priceModifier: 1.8,
                rentModifier: 1.6,
                adrModifier: 1.5,
                structure: 'rc',
                buildingRatio: 60,
                maxOccupancy: 6,
                managementFeeRatio: 10,
                utilitiesAirbnb: 3.5,
                utilitiesLease: 0.6,
                managementFeeTooltip: '2LDK公寓的管理費與修繕金佔比約8-12%。',
                structureTooltip: '2LDK通常為RC/SRC構造，法定耐用年限47年。',
                buildingRatioTooltip: '大型公寓的建物價值佔比約55-65%。'
            },
            'tower': {
                priceModifier: 2.5,
                rentModifier: 2.2,
                adrModifier: 2,
                structure: 'rc',
                buildingRatio: 70,
                maxOccupancy: 5,
                managementFeeRatio: 15,
                utilitiesAirbnb: 4,
                utilitiesLease: 0.8,
                managementFeeTooltip: '塔樓因公共設施豐富(如健身房、接待櫃台)，管理費與修繕金最高，通常佔15-20%。',
                structureTooltip: '塔樓均為RC/SRC構造，法定耐用年限47年。',
                buildingRatioTooltip: '塔樓的建物價值佔比最高，因為其建築成本和附加價值高，通常在70-80%。'
            },
            'house': {
                priceModifier: 2.2,
                rentModifier: 2,
                adrModifier: 2.5,
                structure: 'wood',
                buildingRatio: 40,
                maxOccupancy: 10,
                managementFeeRatio: 5,
                utilitiesAirbnb: 5,
                utilitiesLease: 0.2,
                managementFeeTooltip: '一戶建沒有管理費，但需自行提撥修繕金，建議每年提撥房價的0.5% (約5%的租金)做為長期維護基金。',
                structureTooltip: '一戶建多為木造，法定耐用年限22年，折舊速度快，有利於早期節稅。',
                buildingRatioTooltip: '一戶建的土地價值佔比較高，建物價值佔比通常在30-50%，這有助於降低固定資產稅。'
            }
        },
        locations: {
            'Minato':    { basePrice: 8000, baseRent: 30, baseADR: 25000 },
            'Chiyoda':   { basePrice: 9000, baseRent: 32, baseADR: 28000 },
            'Chuo':      { basePrice: 8500, baseRent: 31, baseADR: 27000 },
            'Shibuya':   { basePrice: 8200, baseRent: 29, baseADR: 26000 },
            'Shinjuku':  { basePrice: 7500, baseRent: 28, baseADR: 24000 },
            'Meguro':    { basePrice: 7000, baseRent: 26, baseADR: 22000 },
            'Setagaya':  { basePrice: 6500, baseRent: 24, baseADR: 20000 },
            'Shinagawa': { basePrice: 6800, baseRent: 25, baseADR: 21000 },
            'Bunkyo':    { basePrice: 7200, baseRent: 27, baseADR: 23000 },
            'Taito':     { basePrice: 5800, baseRent: 22, baseADR: 19000 },
            'Toshima':   { basePrice: 6000, baseRent: 23, baseADR: 19500 },
            'Koto':      { basePrice: 5500, baseRent: 20, baseADR: 18000 },
            'Ota':       { basePrice: 5300, baseRent: 19, baseADR: 17000 },
            'Suginami':  { basePrice: 5600, baseRent: 21, baseADR: 18500 },
            'Nakano':    { basePrice: 5700, baseRent: 21.5, baseADR: 18800},
            'Arakawa':   { basePrice: 4800, baseRent: 18, baseADR: 16000 },
            'Sumida':    { basePrice: 5000, baseRent: 18.5, baseADR: 16500},
            'Itabashi':  { basePrice: 4500, baseRent: 17, baseADR: 15000 },
            'Nerima':    { basePrice: 4600, baseRent: 17.5, baseADR: 15500},
            'Kita':      { basePrice: 4700, baseRent: 17.8, baseADR: 15800},
            'Adachi':    { basePrice: 4000, baseRent: 15, baseADR: 14000 },
            'Katsushika':{ basePrice: 3800, baseRent: 14, baseADR: 13500 },
            'Edogawa':   { basePrice: 4200, baseRent: 16, baseADR: 14500 }
        },
        monetizationModels: {
            'airbnb': {},
            'personalLease': {},
            'commercialLease': {}
        }
    };

    const propertyForm = document.getElementById('property-form');
    const calculateBtn = document.getElementById('calculateBtn');
    const resultsContainer = document.getElementById('resultsContainer');
    const downloadBtn = document.getElementById('downloadBtn');
    const loadingOverlay = document.getElementById('loading-overlay');

    // --- DOM Element Selections ---
    const purchaseTypeSelect = document.getElementById('purchaseType');
    const monetizationModelSelect = document.getElementById('monetizationModel');
    const propertyTypeSelect = document.getElementById('propertyType');
    const locationSelect = document.getElementById('location');
    const loanOriginSelect = document.getElementById('loanOrigin');

    // --- Input Fields ---
    const allInputs = propertyForm.querySelectorAll('input, select');
    const allLoanParams = document.querySelectorAll('.loan-param');
    const allCorporateParams = document.querySelectorAll('.corporate-param');

    // --- Expert Advice Tooltips ---
    const managementFeeTooltip = document.getElementById('managementFeeTooltip');
    const buildingStructureTooltip = document.getElementById('buildingStructureTooltip');
    const buildingRatioTooltip = document.getElementById('buildingRatioTooltip');

    // ===================================================================================
    //                                  EVENT LISTENERS
    // ===================================================================================

    /**
     * Updates the UI and expert default values when the purchase type changes.
     */
    purchaseTypeSelect.addEventListener('change', function () {
        const isCorporate = this.value === 'corporate';
        allCorporateParams.forEach(el => el.classList.toggle('hidden', !isCorporate));
        updateExpertValues();
    });

    /**
     * Updates the UI when the monetization model changes.
     */
    monetizationModelSelect.addEventListener('change', function () {
        const model = this.value;
        document.getElementById('airbnbParams').style.display = model === 'airbnb' ? 'block' : 'none';
        document.getElementById('personalLeaseParams').style.display = model === 'personalLease' ? 'block' : 'none';
        document.getElementById('commercialLeaseParams').style.display = model === 'commercialLease' ? 'block' : 'none';
        updateExpertValues();
    });
    
    /**
     * Updates expert default values when property type or location changes.
     */
    propertyTypeSelect.addEventListener('change', updateExpertValues);
    locationSelect.addEventListener('change', updateExpertValues);

    /**
     * Updates the visibility of loan-related input fields based on the selected loan origin.
     */
    loanOriginSelect.addEventListener('change', function() {
        const selectedLoan = this.value;
        allLoanParams.forEach(param => {
            const loanTypes = param.getAttribute('data-loan-type').split(' ');
            param.classList.toggle('hidden', !loanTypes.includes(selectedLoan));
        });
    });

    /**
     * Handles the main calculation logic when the form is submitted.
     */
    calculateBtn.addEventListener('click', async function (e) {
        e.preventDefault();
        showLoading(true, "參數驗證中...");
        
        // Basic form validation
        if (!propertyForm.checkValidity()) {
            propertyForm.reportValidity();
            showLoading(false);
            return;
        }

        const formData = getFormData();
        
        // Log event to Google Analytics
        if (typeof gtag === 'function') {
            gtag('event', 'generate_report', {
                'event_category': 'Financial Analysis',
                'event_label': `Model: ${formData.monetizationModel}, Type: ${formData.propertyType}, Location: ${formData.location}`,
                'value': formData.propertyPrice
            });
        }
        
        showLoading(true, "正在與後端伺服器進行財務計算...");
        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const results = await response.json();
            showLoading(true, "報告生成中，請稍候...");
            displayResults(results);
            resultsContainer.classList.remove('hidden');
            downloadBtn.classList.remove('hidden');
            
            // Scroll to results after a short delay to allow for rendering
            setTimeout(() => {
                 resultsContainer.scrollIntoView({ behavior: 'smooth' });
            }, 300);

        } catch (error) {
            console.error('Calculation Error:', error);
            alert(`計算失敗，請檢查輸入參數或稍後再試。\n錯誤詳情: ${error.message}`);
        } finally {
            showLoading(false);
        }
    });

    /**
     * Handles the PDF download functionality.
     */
    downloadBtn.addEventListener('click', function () {
        showLoading(true, "正在準備PDF文件，請稍候...");
        const { jsPDF } = window.jspdf;
        const reportElement = document.getElementById('reportToPrint');

        // Temporarily hide buttons for printing
        const buttons = reportElement.querySelectorAll('.btn-group, .expert-marker, .info-icon');
        buttons.forEach(btn => btn.style.display = 'none');
        
        html2canvas(reportElement, {
            scale: 1.5, // 降低畫質以減少檔案大小 (從2降到1.5)
            useCORS: true,
            logging: false, // 關閉log以提升效能
            windowWidth: document.documentElement.offsetWidth,
            windowHeight: document.documentElement.offsetHeight,
            backgroundColor: '#ffffff', // 設定背景色
            removeContainer: true,
            onclone: (doc) => {
                 // Ensure styles are applied in the cloned document
                const clonedButtons = doc.querySelectorAll('.btn-group, .expert-marker, .info-icon');
                clonedButtons.forEach(btn => btn.style.display = 'none');
            }
        }).then(canvas => {
            // 使用JPEG格式並降低品質以減少檔案大小
            const imgData = canvas.toDataURL('image/jpeg', 0.8);
            const pdf = new jsPDF({
                orientation: 'p',
                unit: 'pt',
                format: 'a4',
                putOnlyUsedFonts: true,
                floatPrecision: 16
            });

            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = pdf.internal.pageSize.getHeight();
            const canvasWidth = canvas.width;
            const canvasHeight = canvas.height;
            const ratio = canvasHeight / canvasWidth;
            const imgHeight = pdfWidth * ratio;
            
            let heightLeft = imgHeight;
            let position = 0;

            pdf.addImage(imgData, 'JPEG', 0, position, pdfWidth, imgHeight);
            heightLeft -= pdfHeight;

            while (heightLeft > 0) {
                position = heightLeft - imgHeight;
                pdf.addPage();
                pdf.addImage(imgData, 'JPEG', 0, position, pdfWidth, imgHeight);
                heightLeft -= pdfHeight;
            }
            
            pdf.save('日本不動產投資分析報告.pdf');
            
        }).catch(error => {
            console.error("PDF generation failed:", error);
            alert("PDF生成失敗，請再試一次。");
        }).finally(() => {
            // Restore button visibility
            buttons.forEach(btn => btn.style.display = '');
            showLoading(false);
        });
    });

    // ===================================================================================
    //                                  HELPER FUNCTIONS
    // ===================================================================================
    
    /**
     * Shows or hides the loading overlay.
     * @param {boolean} show - True to show, false to hide.
     * @param {string} [message] - The message to display on the loading overlay.
     */
    function showLoading(show, message = "分析報告生成中，請稍候...") {
        const loadingMessage = document.getElementById('loading-message');
        if (loadingMessage) {
            loadingMessage.textContent = message;
        }
        loadingOverlay.style.display = show ? 'flex' : 'none';
    }

    /**
     * Gathers all data from the form inputs.
     * @returns {object} An object containing all form data.
     */
    function getFormData() {
        const formData = {};
        allInputs.forEach(input => {
            // 跳過隱藏的字段以避免重複
            if (input.closest('.hidden')) {
                return;
            }
            
            if (input.type === 'number' || input.inputmode === 'decimal') {
                formData[input.id] = parseFloat(input.value) || 0;
            } else if (input.type === 'checkbox') {
                 formData[input.id] = input.checked;
            }
            else {
                formData[input.id] = input.value;
            }
        });
        
        // 調試：顯示收集到的數據
        console.log('收集到的表單數據:', formData);
        return formData;
    }
    
    /**
     * Formats a number into a currency string (e.g., 1,234.5).
     * @param {number} num - The number to format.
     * @param {number} [digits=1] - The number of decimal places.
     * @returns {string} The formatted currency string.
     */
    function formatCurrency(num, digits = 1) {
        if (typeof num !== 'number' || isNaN(num)) {
            return '-';
        }
        return num.toLocaleString(undefined, {
            minimumFractionDigits: digits,
            maximumFractionDigits: digits
        });
    }

    /**
     * 根據指標值返回健康度 CSS 類別
     * @param {number} value - 指標值
     * @param {number} excellentThreshold - 優秀門檻
     * @param {number} warningThreshold - 警告門檻
     * @returns {string} - CSS 類別名稱
     */
    function getHealthClass(value, excellentThreshold, warningThreshold) {
        if (value >= excellentThreshold) {
            return 'excellent';
        } else if (value >= warningThreshold) {
            return 'good';
        } else {
            return 'danger';
        }
    }

    /**
     * LTV 特殊的健康度分級（數值越低越好）
     * @param {number} ltv - LTV 百分比
     * @returns {string} - CSS 類別名稱
     */
    function getLTVHealthClass(ltv) {
        if (ltv <= 75) {
            return 'excellent';
        } else if (ltv <= 85) {
            return 'good';
        } else {
            return 'danger';
        }
    }

    /**
     * Creates a standard table row for financial data.
     * @param {string} label - The label for the data point.
     * @param {number} valueJPY - The value in JPY (万円).
     * @param {number} valueTWD - The value in TWD (萬台幣).
     * @param {string} tooltipText - The help text for the tooltip.
     * @returns {HTMLTableRowElement} The created table row element.
     */
    function createRow(label, valueJPY, valueTWD, tooltipText) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                ${label}
                <div class="tooltip">
                    <span class="info-icon">i</span>
                    <span class="tooltiptext">${tooltipText}</span>
                </div>
            </td>
            <td class="value-cell ${valueJPY > 0 ? 'positive' : valueJPY < 0 ? 'negative' : ''}">${formatCurrency(valueJPY)}</td>
            <td class="value-cell ${valueTWD > 0 ? 'positive' : valueTWD < 0 ? 'negative' : ''}">${formatCurrency(valueTWD)}</td>
        `;
        return tr;
    }

    /**
     * Displays the financial analysis results in the UI.
     * @param {object} results - The analysis results from the backend.
     */
    function displayResults(results) {
        // 儲存計算結果供指標調整功能使用
        lastCalculationData = results;
        
        // --- 1. 投資健康度評估 ---
        const healthBadge = document.getElementById('healthBadge');
        const healthRating = document.getElementById('healthRating');
        const healthDescription = document.getElementById('healthDescription');
        
        healthRating.textContent = results.leverage_metrics.health_rating;
        healthDescription.textContent = results.leverage_metrics.health_description;
        
        // 設定健康度顏色
        healthBadge.className = `health-badge ${results.leverage_metrics.health_color}`;
        
        // --- 2. 基本投資人版本 KPIs ---
        const cashOnCashEl = document.getElementById('cashOnCashReturn');
        cashOnCashEl.textContent = `${formatCurrency(results.kpi.cash_on_cash_return, 2)}%`;
        cashOnCashEl.className = `value-cell ${getHealthClassDynamic(results.kpi.cash_on_cash_return, 'cocr')}`;
        
        const dcrEl = document.getElementById('dcrValue');
        dcrEl.textContent = formatCurrency(results.leverage_metrics.dcr, 2);
        dcrEl.className = `value-cell ${getHealthClassDynamic(results.leverage_metrics.dcr, 'dcr')}`;
        
        const ltvEl = document.getElementById('ltvValue');
        ltvEl.textContent = `${formatCurrency(results.leverage_metrics.ltv, 1)}%`;
        ltvEl.className = `value-cell ${getHealthClassDynamic(results.leverage_metrics.ltv, 'ltv')}`;
        
        const totalROIEl = document.getElementById('totalROI');
        totalROIEl.textContent = `${formatCurrency(results.kpi.irr, 2)}%`;
        totalROIEl.className = `value-cell ${getHealthClassDynamic(results.kpi.irr, 'irr')}`;
        
        // --- 3. 專業投資人版本指標 ---
        const dscrEl = document.getElementById('dscrValue');
        dscrEl.textContent = formatCurrency(results.leverage_metrics.dscr, 2);
        dscrEl.className = `value-cell ${getHealthClassDynamic(results.leverage_metrics.dscr, 'dscr')}`;
        
        const leverageEl = document.getElementById('leverageRatio');
        leverageEl.textContent = formatCurrency(results.leverage_metrics.leverage_ratio, 2);
        leverageEl.className = `value-cell ${getHealthClassDynamic(results.leverage_metrics.leverage_ratio, 'leverage')}`;
        
        const leveragedROEEl = document.getElementById('leveragedROE');
        leveragedROEEl.textContent = `${formatCurrency(results.leverage_metrics.leveraged_roe, 2)}%`;
        leveragedROEEl.className = `value-cell ${getHealthClassDynamic(results.leverage_metrics.leveraged_roe, 'irr')}`;
        document.getElementById('annualDebtService').textContent = `${formatCurrency(results.leverage_metrics.annual_debt_service_jpy)}萬円 (${formatCurrency(results.leverage_metrics.annual_debt_service_twd)}萬台幣)`;
        document.getElementById('annualNOI').textContent = `${formatCurrency(results.leverage_metrics.annual_noi_jpy)}萬円 (${formatCurrency(results.leverage_metrics.annual_noi_twd)}萬台幣)`;
        document.getElementById('paybackPeriod').textContent = `${results.kpi.payback_period > 0 ? formatCurrency(results.kpi.payback_period, 1) + ' 年' : '無法回收'}`;

        // --- 2. Initial Investment ---
        document.getElementById('totalInvestmentJPY').textContent = formatCurrency(results.initial_investment.total_investment_jpy);
        document.getElementById('totalInvestmentTWD').textContent = formatCurrency(results.initial_investment.total_investment_twd);
        document.getElementById('acquisitionCostsJPY').textContent = formatCurrency(results.initial_investment.acquisition_costs_jpy);
        document.getElementById('acquisitionCostsTWD').textContent = formatCurrency(results.initial_investment.acquisition_costs_twd);
        document.getElementById('initialSetupCostsJPY').textContent = formatCurrency(results.initial_investment.initial_setup_costs_jpy);
        document.getElementById('initialSetupCostsTWD').textContent = formatCurrency(results.initial_investment.initial_setup_costs_twd);

        document.getElementById('downPaymentOwnCapitalJPY').textContent = formatCurrency(results.initial_investment.down_payment_own_capital_jpy);
        document.getElementById('downPaymentOwnCapitalTWD').textContent = formatCurrency(results.initial_investment.down_payment_own_capital_twd);
        document.getElementById('downPaymentCreditLoanJPY').textContent = formatCurrency(results.initial_investment.down_payment_credit_loan_jpy);
        document.getElementById('downPaymentCreditLoanTWD').textContent = formatCurrency(results.initial_investment.down_payment_credit_loan_twd);
        document.getElementById('loanAmountJPY').textContent = formatCurrency(results.initial_investment.loan_amount_jpy);
        document.getElementById('loanAmountTWD').textContent = formatCurrency(results.initial_investment.loan_amount_twd);
        document.getElementById('totalLoanAmountJPY').textContent = formatCurrency(results.initial_investment.loan_amount_jpy + results.initial_investment.down_payment_credit_loan_jpy);
        document.getElementById('totalLoanAmountTWD').textContent = formatCurrency(results.initial_investment.loan_amount_twd + results.initial_investment.down_payment_credit_loan_twd);
        
        // --- 3. Cash Flow Breakdown (Dual Column Format: JPY + TWD) ---
        const cashFlowBody = document.getElementById('cashFlowBreakdown');
        cashFlowBody.innerHTML = ''; // Clear previous results
        
        const cf = results.cash_flow;
        
        // 1. 總租金收入
        cashFlowBody.appendChild(createRow('總租金收入', cf.total_revenue_jpy, cf.total_revenue_twd, '根據您的營運模式、入住率、租金等參數計算出的年度總收入。'));
        
        // 2. 營運總支出（僅包含直接營運費用）
        cashFlowBody.appendChild(createRow('營運總支出', -cf.operating_expenses_jpy, -cf.operating_expenses_twd, '包含平台費、清潔費、水電費等直接營運相關的年度開銷。'));
        
        // 3. EBITDA
        const ebitdaRow = createRow('稅息折舊及攤銷前利潤 (EBITDA)', cf.ebitda_jpy, cf.ebitda_twd, 'EBITDA = 總收入 - 營運總支出。此數據反映了房產本身的核心獲利能力，排除了融資和稅務結構的影響。');
        ebitdaRow.classList.add('highlight-row');
        cashFlowBody.appendChild(ebitdaRow);
        
        // 4. 建物折舊
        if (cf.depreciation_jpy > 0) {
            cashFlowBody.appendChild(createRow('建物折舊', -cf.depreciation_jpy, -cf.depreciation_twd, '法規允許的非現金開銷，可在帳面上用來抵稅，但不會實際支付現金。'));
        }
        
        // 5. 貸款利息
        if (cf.interest_payment_jpy > 0) {
            cashFlowBody.appendChild(createRow('貸款利息', -cf.interest_payment_jpy, -cf.interest_payment_twd, '每年支付給銀行的貸款利息，隨著本金償還會逐年減少。'));
        }
        
        // 6. 其他費用（管理費、房屋稅、保險、會計師費等）
        if (cf.other_expenses_jpy > 0) {
            cashFlowBody.appendChild(createRow('其他費用 (管理費、稅費等)', -cf.other_expenses_jpy, -cf.other_expenses_twd, '包含物業管理費、房屋稅、保險費、會計師費等其他必要支出。'));
        }
        
        // 7. 稅前淨利 (EBT)
        const ebtRow = createRow('稅前淨利 (EBT)', cf.ebt_jpy, cf.ebt_twd, 'EBT = EBITDA - 折舊 - 利息 - 其他費用。這是計算應繳稅款的基礎。');
        ebtRow.classList.add('highlight-row');
        cashFlowBody.appendChild(ebtRow);
        
        // 8. 應繳稅款
        if (cf.tax_jpy > 0) {
            cashFlowBody.appendChild(createRow('應繳稅款', -cf.tax_jpy, -cf.tax_twd, '根據您的稅前淨利與稅率計算出的應繳稅額。'));
        }

        // Net Cash Flow Totals (Dual Column)
        document.getElementById('netCashFlow_stable_jpy').textContent = formatCurrency(cf.net_cash_flow_jpy);
        document.getElementById('netCashFlow_stable_jpy').className = `value-cell ${cf.net_cash_flow_jpy > 0 ? 'positive' : cf.net_cash_flow_jpy < 0 ? 'negative' : ''}`;
        document.getElementById('netCashFlow_stable_twd').textContent = formatCurrency(cf.net_cash_flow_twd);
        document.getElementById('netCashFlow_stable_twd').className = `value-cell ${cf.net_cash_flow_twd > 0 ? 'positive' : cf.net_cash_flow_twd < 0 ? 'negative' : ''}`;


        // --- 4. Annual Projections Table ---
        const annualTableBody = document.getElementById('annualTableBody');
        annualTableBody.innerHTML = ''; // Clear previous
        results.annual_projections.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.year}</td>
                <td class="value-cell ${item.net_cash_flow > 0 ? 'positive' : item.net_cash_flow < 0 ? 'negative' : ''}">${formatCurrency(item.net_cash_flow)}</td>
                <td class="value-cell">${formatCurrency(item.property_value)}</td>
                <td class="value-cell">${formatCurrency(item.loan_balance)}</td>
                <td class="value-cell ${item.net_equity > 0 ? 'positive' : item.net_equity < 0 ? 'negative' : ''}">${formatCurrency(item.net_equity)}</td>
                <td class="value-cell ${item.net_equity_twd > 0 ? 'positive' : item.net_equity_twd < 0 ? 'negative' : ''}">${formatCurrency(item.net_equity_twd)}</td>
            `;
            annualTableBody.appendChild(row);
        });

        // --- 5. Expert Suggestions ---
        const suggestionText = document.getElementById('suggestionText');
        const expertSuggestionsSection = document.getElementById('expertSuggestions');
        if (results.suggestions && results.suggestions.length > 0) {
            suggestionText.innerHTML = `<p>基於您的輸入參數與分析結果，我們提供以下幾點客製化建議：</p><ul>` + results.suggestions.map(s => `<li>${s}</li>`).join('') + `</ul>`;
            expertSuggestionsSection.classList.remove('hidden');
        } else {
            expertSuggestionsSection.classList.add('hidden');
        }
    }

    // ===================================================================================
    //                                  EXPERT VALUES LOGIC
    // ===================================================================================
    
    /**
     * Main function to update form fields with expert-recommended values.
     * This function is called when key parameters like property type or location change.
     */
    function updateExpertValues() {
        const propertyType = propertyTypeSelect.value;
        const location = locationSelect.value;
        const monetizationModel = monetizationModelSelect.value;
        const purchaseType = purchaseTypeSelect.value;

        // Fetch the base configs for property and location
        const propertyConfig = expertValues.propertyTypes[propertyType] || {};
        const locationConfig = expertValues.locations[location] || {};
        const modelConfig = expertValues.monetizationModels[monetizationModel] || {};

        // --- Update financial parameters based on property and location ---
        const basePrice = locationConfig.basePrice || 0;
        const priceModifier = propertyConfig.priceModifier || 1;
        document.getElementById('propertyPrice').value = Math.round(basePrice * priceModifier);
        
        // --- Update operational parameters based on the monetization model ---
        if (monetizationModel === 'airbnb') {
            document.getElementById('dailyRate').value = Math.round((locationConfig.baseADR || 0) * (propertyConfig.adrModifier || 1));
            document.getElementById('monthlyUtilities').value = propertyConfig.utilitiesAirbnb || 2.5;
            document.getElementById('maxOccupancy').value = propertyConfig.maxOccupancy || 4;
        } else if (monetizationModel === 'personalLease') {
            document.getElementById('monthlyRent').value = Math.round((locationConfig.baseRent || 0) * (propertyConfig.rentModifier || 1));
             document.getElementById('leaseUtilities').value = propertyConfig.utilitiesLease || 0.5;
        }

        // --- Update structural and tax-related parameters ---
        document.getElementById('buildingStructure').value = propertyConfig.structure || 'rc';
        document.getElementById('buildingRatio').value = propertyConfig.buildingRatio || 60;
        document.getElementById('managementFeeRatio').value = propertyConfig.managementFeeRatio || 8;
        
        // --- Update tooltip content ---
        if(managementFeeTooltip) {
            managementFeeTooltip.textContent = propertyConfig.managementFeeTooltip || '此建議值會根據房產類型自動調整。';
        }
        if(buildingStructureTooltip) {
            buildingStructureTooltip.textContent = propertyConfig.structureTooltip || '此建議值會根據房產類型自動調整。';
        }
        if(buildingRatioTooltip) {
             buildingRatioTooltip.textContent = propertyConfig.buildingRatioTooltip || '此建議值會根據房產類型自動調整。';
        }
        
        // Trigger change event to re-evaluate dependent fields like loan visibility
        loanOriginSelect.dispatchEvent(new Event('change'));
    }

    // --- Initial setup on page load ---
    function initialize() {
        // Set initial visibility of sections based on default selections
        monetizationModelSelect.dispatchEvent(new Event('change'));
        purchaseTypeSelect.dispatchEvent(new Event('change'));
        
        // Populate form with expert values
        updateExpertValues();

        showLoading(false); // Hide loading overlay once everything is ready
    }

    // 全域變數儲存指標閾值
    let thresholds = {
        dcr: { safe: 1.25, warning: 1.10 },
        cocr: { excellent: 5, good: 3 },
        ltv: { conservative: 75, moderate: 85 },
        irr: { excellent: 8, good: 5 },
        dscr: { healthy: 1.30, warning: 1.15 },
        leverage: { conservative: 3.0, moderate: 5.0 }
    };

    // 儲存最後一次計算結果，用於重新評估健康度
    let lastCalculationData = null;

    // 更新健康度分類函數以使用動態閾值
    function getHealthClassDynamic(value, type) {
        switch(type) {
            case 'cocr':
                if (value >= thresholds.cocr.excellent) return 'excellent';
                if (value >= thresholds.cocr.good) return 'good';
                return 'danger';
            case 'dcr':
                if (value >= thresholds.dcr.safe) return 'excellent';
                if (value >= thresholds.dcr.warning) return 'good';
                return 'danger';
            case 'ltv':
                if (value <= thresholds.ltv.conservative) return 'excellent';
                if (value <= thresholds.ltv.moderate) return 'good';
                return 'danger';
            case 'irr':
                if (value >= thresholds.irr.excellent) return 'excellent';
                if (value >= thresholds.irr.good) return 'good';
                return 'danger';
            case 'dscr':
                if (value >= thresholds.dscr.healthy) return 'excellent';
                if (value >= thresholds.dscr.warning) return 'good';
                return 'danger';
            case 'leverage':
                if (value <= thresholds.leverage.conservative) return 'excellent';
                if (value <= thresholds.leverage.moderate) return 'good';
                return 'danger';
            default:
                return 'good';
        }
    }

    // 更新健康指標顯示
    function updateHealthIndicators(results) {
        if (!results) return;
        
        // 更新基本投資人版本的健康度顏色
        const cashOnCashEl = document.getElementById('cashOnCashReturn');
        if (cashOnCashEl) {
            cashOnCashEl.className = `value-cell ${getHealthClassDynamic(results.kpi.cash_on_cash_return, 'cocr')}`;
        }
        
        const dcrEl = document.getElementById('dcrValue');
        if (dcrEl) {
            dcrEl.className = `value-cell ${getHealthClassDynamic(results.leverage_metrics.dcr, 'dcr')}`;
        }
        
        const ltvEl = document.getElementById('ltvValue');
        if (ltvEl) {
            ltvEl.className = `value-cell ${getHealthClassDynamic(results.leverage_metrics.ltv, 'ltv')}`;
        }
        
        const totalROIEl = document.getElementById('totalROI');
        if (totalROIEl) {
            totalROIEl.className = `value-cell ${getHealthClassDynamic(results.kpi.irr, 'irr')}`;
        }

        // 更新專業投資人版本的健康度顏色
        const dscrEl = document.getElementById('dscrValue');
        if (dscrEl) {
            dscrEl.className = `value-cell ${getHealthClassDynamic(results.leverage_metrics.dscr, 'dscr')}`;
        }
        
        const leverageEl = document.getElementById('leverageRatio');
        if (leverageEl) {
            leverageEl.className = `value-cell ${getHealthClassDynamic(results.leverage_metrics.leverage_ratio, 'leverage')}`;
        }
        
        const leveragedROEEl = document.getElementById('leveragedROE');
        if (leveragedROEEl) {
            leveragedROEEl.className = `value-cell ${getHealthClassDynamic(results.leverage_metrics.leveraged_roe, 'irr')}`;
        }
    }

    // 切換基本版和專業版顯示
    function setupViewToggle() {
        const basicViewBtn = document.getElementById('basicViewBtn');
        const professionalViewBtn = document.getElementById('professionalViewBtn');
        const basicView = document.getElementById('basicInvestorView');
        const professionalView = document.getElementById('professionalInvestorView');

        if (basicViewBtn && professionalViewBtn && basicView && professionalView) {
            basicViewBtn.addEventListener('click', () => {
                // 顯示/隱藏內容
                basicView.style.display = 'block';
                professionalView.style.display = 'none';
                
                // 更新按鍵狀態
                basicViewBtn.classList.add('active');
                professionalViewBtn.classList.remove('active');
                
                // 平滑滾動到內容區域
                basicView.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });

            professionalViewBtn.addEventListener('click', () => {
                // 顯示/隱藏內容
                basicView.style.display = 'none';
                professionalView.style.display = 'block';
                
                // 更新按鍵狀態
                professionalViewBtn.classList.add('active');
                basicViewBtn.classList.remove('active');
                
                // 平滑滾動到內容區域
                professionalView.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
        }

        // 指標調整角落按鈕功能
        const adjustmentToggleBtn = document.getElementById('adjustmentToggleBtn');
        const adjustmentPanel = document.getElementById('adjustmentPanel');
        const closeAdjustmentBtn = document.getElementById('closeAdjustmentBtn');

        if (adjustmentToggleBtn && adjustmentPanel) {
            adjustmentToggleBtn.addEventListener('click', () => {
                adjustmentPanel.classList.remove('hidden');
                adjustmentToggleBtn.classList.add('active');
                
                // 平滑滾動到調整面板
                adjustmentPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
        }

        if (closeAdjustmentBtn && adjustmentPanel) {
            closeAdjustmentBtn.addEventListener('click', () => {
                adjustmentPanel.classList.add('hidden');
                adjustmentToggleBtn.classList.remove('active');
            });
        }

        // 指標調整功能
        const resetBtn = document.getElementById('resetThresholdsBtn');
        const applyBtn = document.getElementById('applyThresholdsBtn');

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                // 重設為預設值
                document.getElementById('dcrSafeThreshold').value = 1.25;
                document.getElementById('dcrWarningThreshold').value = 1.10;
                document.getElementById('cocrExcellentThreshold').value = 5;
                document.getElementById('cocrGoodThreshold').value = 3;
                document.getElementById('ltvConservativeThreshold').value = 75;
                document.getElementById('ltvModerateThreshold').value = 85;
                document.getElementById('irrExcellentThreshold').value = 8;
                document.getElementById('irrGoodThreshold').value = 5;
                document.getElementById('dscrHealthyThreshold').value = 1.30;
                document.getElementById('dscrWarningThreshold').value = 1.15;
                document.getElementById('leverageConservativeThreshold').value = 3.0;
                document.getElementById('leverageModerateThreshold').value = 5.0;
                
                // 更新全域閾值
                thresholds = {
                    dcr: { safe: 1.25, warning: 1.10 },
                    cocr: { excellent: 5, good: 3 },
                    ltv: { conservative: 75, moderate: 85 },
                    irr: { excellent: 8, good: 5 },
                    dscr: { healthy: 1.30, warning: 1.15 },
                    leverage: { conservative: 3.0, moderate: 5.0 }
                };
                
                alert('已重設為預設值！請點擊「套用調整」以更新指標評級。');
            });
        }

        if (applyBtn) {
            applyBtn.addEventListener('click', () => {
                // 讀取用戶設定的閾值
                thresholds.dcr.safe = parseFloat(document.getElementById('dcrSafeThreshold').value);
                thresholds.dcr.warning = parseFloat(document.getElementById('dcrWarningThreshold').value);
                thresholds.cocr.excellent = parseFloat(document.getElementById('cocrExcellentThreshold').value);
                thresholds.cocr.good = parseFloat(document.getElementById('cocrGoodThreshold').value);
                thresholds.ltv.conservative = parseFloat(document.getElementById('ltvConservativeThreshold').value);
                thresholds.ltv.moderate = parseFloat(document.getElementById('ltvModerateThreshold').value);
                thresholds.irr.excellent = parseFloat(document.getElementById('irrExcellentThreshold').value);
                thresholds.irr.good = parseFloat(document.getElementById('irrGoodThreshold').value);
                thresholds.dscr.healthy = parseFloat(document.getElementById('dscrHealthyThreshold').value);
                thresholds.dscr.warning = parseFloat(document.getElementById('dscrWarningThreshold').value);
                thresholds.leverage.conservative = parseFloat(document.getElementById('leverageConservativeThreshold').value);
                thresholds.leverage.moderate = parseFloat(document.getElementById('leverageModerateThreshold').value);
                
                // 重新計算並更新顯示
                if (lastCalculationData) {
                    updateHealthIndicators(lastCalculationData);
                    
                    // 收折調整面板
                    const adjustmentPanel = document.getElementById('adjustmentPanel');
                    const adjustmentToggleBtn = document.getElementById('adjustmentToggleBtn');
                    const basicViewBtn = document.getElementById('basicViewBtn');
                    const professionalViewBtn = document.getElementById('professionalViewBtn');
                    const basicView = document.getElementById('basicInvestorView');
                    const professionalView = document.getElementById('professionalInvestorView');
                    
                    if (adjustmentPanel && adjustmentToggleBtn) {
                        adjustmentPanel.classList.add('hidden');
                        adjustmentToggleBtn.classList.remove('active');
                    }
                    
                    // 切換回基本投資人版
                    if (basicViewBtn && professionalViewBtn && basicView && professionalView) {
                        basicView.style.display = 'block';
                        professionalView.style.display = 'none';
                        basicViewBtn.classList.add('active');
                        professionalViewBtn.classList.remove('active');
                        
                        // 平滑滾動到基本投資人版
                        setTimeout(() => {
                            basicView.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }, 300);
                    }
                    
                    alert('✅ 指標調整已套用！\n\n所有健康評級已根據新標準更新，已自動切換回基本投資人版供您查看結果。');
                } else {
                    alert('⚠️ 請先進行財務計算，再套用指標調整。');
                }
            });
        }
    }

    initialize();
    setupViewToggle();
}); 