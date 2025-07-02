// ===== NAVIGATION AND PAGE MANAGEMENT =====
let currentSection = 'home';

/**
 * 顯示指定的頁面區塊
 */
function showSection(sectionId) {
    // Hide all sections
    const sections = ['home', 'analysis', 'market', 'portfolio', 'about'];
    sections.forEach(id => {
        const section = document.getElementById(id);
        if (section) {
            section.classList.add('hidden');
        }
    });
    
    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.remove('hidden');
        currentSection = sectionId;
    }
    
    // Update navigation active state
    updateNavigation(sectionId);
    
    // Update page title
    updatePageTitle(sectionId);
    
    // Update URL with proper routing
    updateURL(sectionId);
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * 更新導航選單的啟用狀態
 */
function updateNavigation(activeSection) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        const section = link.getAttribute('data-section');
        if (section === activeSection) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * 更新頁面標題
 */
function updatePageTitle(sectionId) {
    const titles = {
        'home': 'NIPPON PROPERTY ANALYTICS - Professional Investment Intelligence',
        'analysis': 'NIPPON PROPERTY ANALYTICS - 財務分析工具',
        'market': 'NIPPON PROPERTY ANALYTICS - 市場洞察',
        'portfolio': 'NIPPON PROPERTY ANALYTICS - 投資組合',
        'about': 'NIPPON PROPERTY ANALYTICS - 關於我們'
    };
    
    document.title = titles[sectionId] || titles['home'];
}

/**
 * 更新 URL 以反映當前頁面
 */
function updateURL(sectionId) {
    const urlPaths = {
        'home': '/',
        'analysis': '/analysis',
        'market': '/market',
        'portfolio': '/portfolio',
        'about': '/about'
    };
    
    const newPath = urlPaths[sectionId] || '/';
    
    // 使用 History API 更新 URL 而不重新載入頁面
    if (window.location.pathname !== newPath) {
        window.history.pushState({ section: sectionId }, '', newPath);
    }
    
    // Google Analytics 頁面瀏覽追蹤
    if (typeof gtag === 'function') {
        gtag('event', 'page_view', {
            'page_title': document.title,
            'page_location': window.location.href
        });
    }
}

/**
 * 開始分析 - 導航到分析頁面
 */
function startAnalysis() {
    showSection('analysis');
    
    // Google Analytics tracking
    if (typeof gtag === 'function') {
        gtag('event', 'start_analysis', {
            'event_category': 'User Interaction',
            'event_label': 'Start Financial Analysis'
        });
    }
}

/**
 * 滾動到功能介紹區塊
 */
function scrollToFeatures() {
    const featuresSection = document.getElementById('features');
    if (featuresSection) {
        featuresSection.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * 顯示即將推出的功能頁面
 */
function showComingSoonPage(featureName) {
    // 這裡可以顯示一個模態視窗或特殊頁面
    alert(`${featureName} 功能即將推出，敬請期待！`);
    
    // Google Analytics tracking
    if (typeof gtag === 'function') {
        gtag('event', 'coming_soon_click', {
            'event_category': 'User Interaction',
            'event_label': featureName
        });
    }
}

/**
 * 更新載入動畫狀態
 */
function updateLoadingState(show, message = "處理中...") {
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingMessage = document.getElementById('loading-message');
    
    if (loadingOverlay) {
        if (show) {
            loadingOverlay.classList.add('show');
            if (loadingMessage && message) {
                loadingMessage.textContent = message;
            }
        } else {
            loadingOverlay.classList.remove('show');
        }
    }
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function () {
    // 設置導航事件監聽器
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('data-section');
            
            // 檢查是否為即將推出的功能
            if ((sectionId === 'market' || sectionId === 'portfolio') && sectionId !== 'analysis') {
                showComingSoonPage(sectionId === 'market' ? '市場洞察' : '投資組合');
                return;
            }
            
            showSection(sectionId);
        });
    });
    
    // 設置 Hero 區域的按鈕事件
    const heroButtons = document.querySelectorAll('.hero-actions .btn');
    heroButtons.forEach(button => {
        if (button.textContent.includes('開始財務分析')) {
            button.addEventListener('click', startAnalysis);
        } else if (button.textContent.includes('了解更多')) {
            button.addEventListener('click', scrollToFeatures);
        }
    });
    
    // 設置功能卡片的按鈕事件
    const featureButtons = document.querySelectorAll('.feature-cta');
    featureButtons.forEach(button => {
        if (button.textContent.includes('開始分析')) {
            button.addEventListener('click', startAnalysis);
        }
    });
    
    // 初始化頁面狀態 - 根據 URL 路徑確定顯示的頁面
    const pathToSection = {
        '/': 'home',
        '/analysis': 'analysis',
        '/market': 'market',
        '/portfolio': 'portfolio',
        '/about': 'about'
    };
    
    const currentPath = window.location.pathname;
    const initialSection = pathToSection[currentPath] || 'home';
    showSection(initialSection);
    
    // 監聽瀏覽器的前進後退按鈕
    window.addEventListener('popstate', function(e) {
        const path = window.location.pathname;
        const section = pathToSection[path] || 'home';
        
        // 直接更新頁面，不再次更新 URL（避免無限循環）
        const sections = ['home', 'analysis', 'market', 'portfolio', 'about'];
        sections.forEach(id => {
            const sectionEl = document.getElementById(id);
            if (sectionEl) {
                sectionEl.classList.add('hidden');
            }
        });
        
        const targetSection = document.getElementById(section);
        if (targetSection) {
            targetSection.classList.remove('hidden');
        }
        
        updateNavigation(section);
        updatePageTitle(section);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

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
    const downloadBtn = document.getElementById('downloadPdfBtn');
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
        const airbnbParams = document.getElementById('airbnbParams');
        const personalLeaseParams = document.getElementById('personalLeaseParams');
        const commercialLeaseParams = document.getElementById('commercialLeaseParams');
        
        // 隱藏所有營運參數區塊
        const allMonetizationParams = document.querySelectorAll('.monetization-params');
        allMonetizationParams.forEach(param => param.classList.add('hidden'));
        
        // 顯示對應的營運參數區塊
        if (model === 'airbnb' && airbnbParams) {
            airbnbParams.classList.remove('hidden');
        } else if (model === 'personalLease' && personalLeaseParams) {
            personalLeaseParams.classList.remove('hidden');
        } else if (model === 'commercialLease' && commercialLeaseParams) {
            commercialLeaseParams.classList.remove('hidden');
        }
        
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
        updateLoadingState(true, "參數驗證中...");
        
        // Basic form validation
        if (!propertyForm.checkValidity()) {
            propertyForm.reportValidity();
            updateLoadingState(false);
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
        
        updateLoadingState(true, "正在與後端伺服器進行財務計算...");
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
            updateLoadingState(true, "報告生成中，請稍候...");
            displayResults(results);
            resultsContainer.classList.remove('hidden');
            // 下載按鈕永遠顯示在底部，不需要手動顯示
            
            // 自動儲存分析結果（如果用戶已登入）
            // 使用獨立的 Google Auth 模組儲存結果
            if (window.GoogleAuth && window.GoogleAuth.saveAnalysisResults) {
                window.GoogleAuth.saveAnalysisResults(results);
            }
            
            // Scroll to results after a short delay to allow for rendering
            setTimeout(() => {
                 resultsContainer.scrollIntoView({ behavior: 'smooth' });
            }, 300);

        } catch (error) {
            console.error('Calculation Error:', error);
            alert(`計算失敗，請檢查輸入參數或稍後再試。\n錯誤詳情: ${error.message}`);
        } finally {
            updateLoadingState(false);
        }
    });

    /**
     * Handles the PDF download functionality.
     */
    downloadBtn.addEventListener('click', function () {
        updateLoadingState(true, "正在準備PDF文件，請稍候...");
        const { jsPDF } = window.jspdf;
        const reportElement = document.getElementById('reportToPrint');

        // Temporarily hide buttons for printing
        const buttons = reportElement.querySelectorAll('.btn-group, .expert-marker, .info-icon');
        buttons.forEach(btn => btn.style.display = 'none');
        
        html2canvas(reportElement, {
            scale: 1.2, // 進一步降低畫質以減少檔案大小
            useCORS: true,
            logging: false,
            windowWidth: 1200, // 固定寬度提升效能
            windowHeight: window.innerHeight,
            backgroundColor: '#ffffff',
            removeContainer: true,
            allowTaint: false,
            foreignObjectRendering: false, // 禁用外部物件渲染提升效能
            onclone: (doc) => {
                // 隱藏不需要的元素
                const clonedButtons = doc.querySelectorAll('.btn-group, .expert-marker, .info-icon, .download-section');
                clonedButtons.forEach(btn => btn.style.display = 'none');
                
                // 優化字體大小以減少渲染複雜度
                const elements = doc.querySelectorAll('*');
                elements.forEach(el => {
                    const fontSize = window.getComputedStyle(el).fontSize;
                    if (fontSize && parseFloat(fontSize) < 10) {
                        el.style.fontSize = '10px';
                    }
                });
            }
        }).then(canvas => {
            // 使用JPEG格式並大幅降低品質以減少檔案大小
            const imgData = canvas.toDataURL('image/jpeg', 0.6);
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
            updateLoadingState(false);
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
        // --- 1. Basic Analysis Metrics ---
        updateMetricValue('cashOnCashReturn', results.kpi.cash_on_cash_return, 2, '%');
        updateMetricValue('totalROI', results.kpi.irr, 2, '%');
        updateMetricValue('debtCoverageRatio', results.kpi.debt_coverage_ratio || 0, 2);
        updateMetricValue('loanToValue', results.kpi.loan_to_value || 0, 1, '%');

        // --- 2. Professional Analysis Metrics ---
        updateMetricValue('dscr', results.kpi.dscr || 0, 2);
        updateMetricValue('leverageRatio', results.kpi.leverage_ratio || 0, 2);
        updateMetricValue('leveragedROE', results.kpi.leveraged_roe || 0, 2, '%');
        updateMetricValue('annualDebtService', results.kpi.annual_debt_service || 0, 1, '萬円 (52.1萬台幣)');
        updateMetricValue('noi', results.kpi.noi || 0, 1, '萬円 (11.3萬台幣)');
        updateMetricValue('paybackPeriodPro', results.kpi.payback_period, 1, ' 年');

        // --- 3. Initial Investment Table ---
        const initialInvestmentTable = document.getElementById('initialInvestmentTable');
        if (initialInvestmentTable) {
            initialInvestmentTable.innerHTML = ''; // Clear previous results
            
            const inv = results.initial_investment;
            initialInvestmentTable.appendChild(createInvestmentRow('總投資金額 (現金支出)', inv.total_investment_jpy, inv.total_investment_twd));
            initialInvestmentTable.appendChild(createInvestmentRow('├ 頭期款中的自備款', inv.down_payment_own_capital_jpy, inv.down_payment_own_capital_twd));
            initialInvestmentTable.appendChild(createInvestmentRow('├ 初期雜項開銷', inv.acquisition_costs_jpy, inv.acquisition_costs_twd));
            initialInvestmentTable.appendChild(createInvestmentRow('├ 家具家電及法人設立', inv.initial_setup_costs_jpy, inv.initial_setup_costs_twd));
            initialInvestmentTable.appendChild(createInvestmentRow('總融資金額', inv.loan_amount_jpy, inv.loan_amount_twd));
            initialInvestmentTable.appendChild(createInvestmentRow('├ 房屋貸款', inv.loan_amount_jpy, inv.loan_amount_twd));
            
            if (inv.down_payment_credit_loan_jpy > 0) {
                initialInvestmentTable.appendChild(createInvestmentRow('├ 頭期款信貸', inv.down_payment_credit_loan_jpy, inv.down_payment_credit_loan_twd));
            } else {
                initialInvestmentTable.appendChild(createInvestmentRow('├ 頭期款信貸', 0, 0));
            }
        }
        
        // --- 4. Cash Flow Breakdown Table ---
        const cashFlowBreakdownTable = document.getElementById('cashFlowBreakdownTable');
        if (cashFlowBreakdownTable && results.cash_flow) {
            cashFlowBreakdownTable.innerHTML = ''; // Clear previous
            const cf = results.cash_flow;
            
            cashFlowBreakdownTable.appendChild(createCashFlowRow('總租金收入', cf.total_revenue_stable_jpy || 0, cf.total_revenue_stable_twd || 0, 'positive'));
            cashFlowBreakdownTable.appendChild(createCashFlowRow('營運總支出', cf.total_expenses_stable_jpy || 0, cf.total_expenses_stable_twd || 0, 'negative'));
            cashFlowBreakdownTable.appendChild(createCashFlowRow('稅息折舊前利潤 (EBITDA)', cf.ebitda_stable_jpy || 0, cf.ebitda_stable_twd || 0, cf.ebitda_stable_twd > 0 ? 'positive' : 'negative'));
            cashFlowBreakdownTable.appendChild(createCashFlowRow('建物折舊', cf.depreciation_jpy || 0, cf.depreciation_twd || 0, 'negative'));
            cashFlowBreakdownTable.appendChild(createCashFlowRow('貸款利息', cf.interest_payment_stable_jpy || 0, cf.interest_payment_stable_twd || 0, 'negative'));
            cashFlowBreakdownTable.appendChild(createCashFlowRow('其他費用 (管理費、稅費等)', cf.other_expenses_jpy || 0, cf.other_expenses_twd || 0, 'negative'));
            cashFlowBreakdownTable.appendChild(createCashFlowRow('稅前淨利 (EBT)', cf.ebt_stable_jpy || 0, cf.ebt_stable_twd || 0, cf.ebt_stable_twd > 0 ? 'positive' : 'negative'));
            cashFlowBreakdownTable.appendChild(createCashFlowRow('稅後淨現金流', cf.net_cash_flow_stable_jpy || 0, cf.net_cash_flow_stable_twd || 0, cf.net_cash_flow_stable_twd > 0 ? 'positive' : 'negative'));
        }
        
        // --- 5. Annual Asset Changes Table ---
        const assetChangesTable = document.getElementById('assetChangesTable');
        if (assetChangesTable) {
            assetChangesTable.innerHTML = ''; // Clear previous
            results.annual_projections.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.year}</td>
                    <td class="value-cell ${item.net_cash_flow > 0 ? 'positive' : item.net_cash_flow < 0 ? 'negative' : ''}">${formatCurrency(item.net_cash_flow)}</td>
                    <td class="value-cell">${formatCurrency(item.property_value)}</td>
                    <td class="value-cell">${formatCurrency(item.loan_balance)}</td>
                    <td class="value-cell">${formatCurrency(item.net_equity)}</td>
                    <td class="value-cell ${item.net_equity_twd > 0 ? 'positive' : item.net_equity_twd < 0 ? 'negative' : ''}">${formatCurrency(item.net_equity_twd)}</td>
                `;
                assetChangesTable.appendChild(row);
            });
        }
    }

    /**
     * Helper function to update metric values with proper formatting
     */
    function updateMetricValue(elementId, value, decimals = 2, suffix = '') {
        const element = document.getElementById(elementId);
        if (element) {
            if (typeof value === 'number' && !isNaN(value)) {
                element.textContent = `${formatCurrency(value, decimals)}${suffix}`;
                element.className = `metric-value ${value > 0 ? 'positive' : value < 0 ? 'negative' : ''}`;
            } else {
                element.textContent = '-';
                element.className = 'metric-value';
            }
        }
    }

    /**
     * Creates a row for the investment breakdown table
     */
    function createInvestmentRow(label, valueJPY, valueTWD) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${label}</td>
            <td class="value-cell">${formatCurrency(valueJPY)}</td>
            <td class="value-cell">${formatCurrency(valueTWD)}</td>
        `;
        return tr;
    }

    /**
     * Creates a row for the cash flow breakdown table
     */
    function createCashFlowRow(label, valueJPY, valueTWD, cssClass = '') {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${label}</td>
            <td class="value-cell ${cssClass}">${formatCurrency(Math.abs(valueJPY))}</td>
            <td class="value-cell ${cssClass}">${formatCurrency(Math.abs(valueTWD))}</td>
        `;
        return tr;
    }

    // ===================================================================================
    //                                  EXPERT VALUES LOGIC
    // ===================================================================================
    
    /**
     * Main function to update form fields with expert-recommended values.
     * This function is called when key parameters like property type or location change.
     */
    function updateExpertValues() {
        const propertyType = propertyTypeSelect ? propertyTypeSelect.value : '';
        const location = locationSelect ? locationSelect.value : '';
        const monetizationModel = monetizationModelSelect ? monetizationModelSelect.value : '';
        const purchaseType = purchaseTypeSelect ? purchaseTypeSelect.value : '';

        // Fetch the base configs for property and location
        const propertyConfig = expertValues.propertyTypes[propertyType] || {};
        const locationConfig = expertValues.locations[location] || {};
        const modelConfig = expertValues.monetizationModels[monetizationModel] || {};

        // --- Update financial parameters based on property and location ---
        const basePrice = locationConfig.basePrice || 0;
        const priceModifier = propertyConfig.priceModifier || 1;
        const propertyPriceEl = document.getElementById('propertyPrice');
        if (propertyPriceEl) {
            propertyPriceEl.value = Math.round(basePrice * priceModifier);
        }
        
        // --- Update operational parameters based on the monetization model ---
        if (monetizationModel === 'airbnb') {
            const dailyRateEl = document.getElementById('dailyRate');
            const monthlyUtilitiesEl = document.getElementById('monthlyUtilities');
            const avgGuestsEl = document.getElementById('avgGuests');
            
            if (dailyRateEl) dailyRateEl.value = Math.round((locationConfig.baseADR || 0) * (propertyConfig.adrModifier || 1));
            if (monthlyUtilitiesEl) monthlyUtilitiesEl.value = propertyConfig.utilitiesAirbnb || 2.5;
            if (avgGuestsEl) avgGuestsEl.value = propertyConfig.maxOccupancy || 4;
        } else if (monetizationModel === 'personalLease') {
            const monthlyRentEl = document.getElementById('monthlyRent');
            const leaseUtilitiesEl = document.getElementById('leaseUtilities');
            
            if (monthlyRentEl) monthlyRentEl.value = Math.round((locationConfig.baseRent || 0) * (propertyConfig.rentModifier || 1));
            if (leaseUtilitiesEl) leaseUtilitiesEl.value = propertyConfig.utilitiesLease || 0.5;
        } else if (monetizationModel === 'commercialLease') {
            const monthlyRentCommercialEl = document.getElementById('monthlyRentCommercial');
            
            if (monthlyRentCommercialEl) {
                // 商業租賃通常比個人租賃高 20-30%
                const baseCommercialRent = Math.round((locationConfig.baseRent || 0) * (propertyConfig.rentModifier || 1) * 1.25);
                monthlyRentCommercialEl.value = baseCommercialRent;
            }
        }

        // --- Update structural and tax-related parameters ---
        const buildingStructureEl = document.getElementById('buildingStructure');
        const buildingRatioEl = document.getElementById('buildingRatio');
        const managementFeeRatioEl = document.getElementById('managementFeeRatio');
        
        if (buildingStructureEl) buildingStructureEl.value = propertyConfig.structure || 'rc';
        if (buildingRatioEl) buildingRatioEl.value = propertyConfig.buildingRatio || 60;
        if (managementFeeRatioEl) managementFeeRatioEl.value = propertyConfig.managementFeeRatio || 8;
        
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
        if (loanOriginSelect) {
            loanOriginSelect.dispatchEvent(new Event('change'));
        }
    }

    // ===================================================================================
    //                                  MODE SWITCHING LOGIC
    // ===================================================================================
    
    /**
     * Initialize mode switching functionality
     */
    function initializeModeSwitch() {
        const basicModeBtn = document.getElementById('basicMode');
        const professionalModeBtn = document.getElementById('professionalMode');
        const basicAnalysis = document.getElementById('basicAnalysis');
        const professionalAnalysis = document.getElementById('professionalAnalysis');
        
        if (basicModeBtn) {
            basicModeBtn.addEventListener('click', function() {
                // Switch to basic mode
                basicModeBtn.classList.add('active');
                professionalModeBtn.classList.remove('active');
                basicAnalysis.classList.remove('hidden');
                professionalAnalysis.classList.add('hidden');
            });
        }
        
        if (professionalModeBtn) {
            professionalModeBtn.addEventListener('click', function() {
                // Switch to professional mode
                professionalModeBtn.classList.add('active');
                basicModeBtn.classList.remove('active');
                professionalAnalysis.classList.remove('hidden');
                basicAnalysis.classList.add('hidden');
            });
        }
    }

    // --- Initial setup on page load ---
    function initialize() {
        // Set initial visibility of sections based on default selections
        if (monetizationModelSelect) {
            monetizationModelSelect.dispatchEvent(new Event('change'));
        }
        if (purchaseTypeSelect) {
            purchaseTypeSelect.dispatchEvent(new Event('change'));
        }
        
        // Populate form with expert values
        updateExpertValues();
        
        // Initialize mode switching
        initializeModeSwitch();

        showLoading(false); // Hide loading overlay once everything is ready
    }

    initialize();
});

// ===== GOOGLE OAUTH FUNCTIONALITY =====
// Google OAuth 功能已完全移至獨立模組 (static/js/google-auth.js)

// Google Client ID 獲取功能已移至獨立模組 (google-auth.js)

// Google OAuth 功能已移至獨立模組 (google-auth.js)

// Google OAuth 相關功能已移至獨立模組 (google-auth.js)

// 以下 Google OAuth 相關功能已移至獨立模組 (google-auth.js)：
// - handleGoogleSignOut()
// - displayUserInfo()
// - checkExistingAuth()
// - saveAnalysisResults()

// Google OAuth 初始化已移至獨立模組 (google-auth.js) 