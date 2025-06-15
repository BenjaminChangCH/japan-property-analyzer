from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
import math
import os
from version import get_version_info
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 導入新的配置模組
from config.security_config import (
    setup_security_headers, setup_cors_security, 
    rate_limit, calculation_rate_limit, validate_request_data
)
from config.logging_config import setup_logging, setup_error_handlers
from config.health_check import setup_health_endpoints, setup_request_tracking

# 確保當前目錄在 Python 路徑中
import sys
import os
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 導入認證相關模組
from models import db, User
from auth import auth_bp, init_oauth, load_user, unauthorized

app = Flask(__name__, template_folder='templates', static_folder='static')

# 設定 Flask 密鑰
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# 設定資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化資料庫
db.init_app(app)

# 設定 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = '請先登入才能使用此功能'
login_manager.login_message_category = 'warning'
login_manager.user_loader(load_user)
login_manager.unauthorized_handler(unauthorized)

# 初始化 OAuth
oauth, google = init_oauth(app)

# 註冊認證藍圖
app.register_blueprint(auth_bp)

# 創建資料庫表格
with app.app_context():
    db.create_all()

# 設定安全性和監控
setup_cors_security(app)  # 取代原本的 CORS(app)
setup_security_headers(app)
setup_logging(app)
setup_error_handlers(app)
setup_health_endpoints(app)
setup_request_tracking(app)

# --- 版本號 ---
def get_version():
    try:
        with open('version.py', 'r') as f:
            exec(f.read(), globals())
        return __version__
    except (FileNotFoundError, NameError):
        return "N/A"

VERSION = get_version()

# --- GA Tracking ---
GA_TRACKING_ID = os.environ.get('GA_TRACKING_ID', 'G-59XMZ0SZ0G') # Default to test ID
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

@app.route('/')
@rate_limit(max_requests=30)  # 首頁限制較寬鬆
def index():
    app.logger.info(f"首頁訪問 - 環境: {ENVIRONMENT}")
    
    return render_template('index.html', 
                         version=VERSION,
                         ga_tracking_id=GA_TRACKING_ID,
                         environment=ENVIRONMENT)

@app.route('/version')
def version():
    """API 端點：返回應用程式版本資訊"""
    return jsonify(get_version_info())

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/test_debug.html')
def test_debug():
    return send_from_directory('.', 'test_debug.html')



def safe_float(s, default=0.0):
    try:
        return float(s) if s else default
    except (ValueError, TypeError):
        return default

def safe_int(s, default=0):
    try:
        return int(s) if s else default
    except (ValueError, TypeError):
        return default

@app.route('/calculate', methods=['POST'])
@calculation_rate_limit  # 添加計算 API 專用頻率限制
def calculate():
    params = request.get_json()
    
    # 調試：記錄收到的參數
    app.logger.info(f"收到的參數: {params}")
    
    # 驗證必要欄位
    required_fields = ['monetizationModel', 'purchaseType', 'propertyPrice', 'exchangeRate']
    validation_errors = validate_request_data(params, required_fields)
    if validation_errors:
        app.logger.warning(f"計算請求驗證失敗: {validation_errors}")
        app.logger.warning(f"收到的參數詳情: {params}")
        return jsonify({'error': '請求資料不完整', 'details': validation_errors}), 400
    
    MAN_EN = 10000

    monetization_model = params.get('monetizationModel')
    purchase_type = params.get('purchaseType')
    property_price = safe_float(params.get('propertyPrice')) * MAN_EN
    down_payment_ratio = safe_float(params.get('downPaymentRatio')) / 100
    acquisition_cost_ratio = safe_float(params.get('acquisitionCostRatio')) / 100
    exchange_rate = safe_float(params.get('exchangeRate'))
    loan_origin = params.get('loanOrigin')
    initial_furnishing_cost = safe_float(params.get('initialFurnishingCost')) * MAN_EN

    loan_interest_rate = 0
    loan_term = 0
    if loan_origin == 'japan' or loan_origin == 'mixed':
        loan_interest_rate = safe_float(params.get('japanLoanInterestRate')) / 100
        loan_term = safe_int(params.get('japanLoanTerm'))
    elif loan_origin == 'taiwan':
        loan_interest_rate = safe_float(params.get('taiwanLoanInterestRate')) / 100
        loan_term = safe_int(params.get('taiwanLoanTerm'))

    credit_loan_rate = safe_float(params.get('creditLoanRate')) / 100
    management_fee_ratio = safe_float(params.get('managementFeeRatio')) / 100
    property_tax_rate = safe_float(params.get('propertyTaxRate')) / 100
    annual_appreciation = safe_float(params.get('annualAppreciation')) / 100
    investment_period = safe_int(params.get('investmentPeriod'))
    building_structure = params.get('buildingStructure')
    building_ratio = safe_float(params.get('buildingRatio')) / 100
    corporate_tax_rate = safe_float(params.get('corporateTaxRate')) / 100
    annual_insurance_cost = safe_float(params.get('annualInsuranceCost')) * MAN_EN
    
    corporate_setup_cost = 0
    if purchase_type == 'corporate':
        corporate_setup_cost = safe_float(params.get('corporateSetupCost')) * MAN_EN

    annual_tax_accountant_fee = 0
    if purchase_type == 'corporate':
        annual_tax_accountant_fee = safe_float(params.get('annualTaxAccountantFee')) * MAN_EN
    
    total_upfront_costs = property_price * acquisition_cost_ratio
    total_cost = property_price + total_upfront_costs
    down_payment_amount = property_price * down_payment_ratio
    loan_amount = property_price - down_payment_amount

    own_capital_for_down_payment_amount = 0
    credit_loan_for_down_payment_amount = 0

    if loan_origin == 'mixed':
        own_capital_amount_input = safe_float(params.get('ownCapitalAmount')) * MAN_EN
        own_capital_for_down_payment_amount = min(own_capital_amount_input, down_payment_amount)
        credit_loan_for_down_payment_amount = down_payment_amount - own_capital_for_down_payment_amount
    else:
        own_capital_for_down_payment_amount = down_payment_amount
        credit_loan_for_down_payment_amount = 0

    total_initial_investment = own_capital_for_down_payment_amount + total_upfront_costs + initial_furnishing_cost + corporate_setup_cost

    monthly_gross_revenue = 0
    monthly_operating_expenses = 0
    one_time_initial_income = 0
    annual_renewal_fee = 0

    if monetization_model == 'airbnb':
        operating_days_cap = safe_int(params.get('operatingDaysCap'))
        occupancy_rate = safe_float(params.get('occupancyRate')) / 100
        daily_rate = safe_float(params.get('dailyRate'))
        platform_fee_rate = safe_float(params.get('platformFeeRate')) / 100
        cleaning_fee = safe_float(params.get('cleaningFee')) * MAN_EN
        avg_stay_duration = safe_float(params.get('avgStayDuration'))
        avg_guests = safe_float(params.get('avgGuests'))
        base_occupancy_for_fee = safe_float(params.get('baseOccupancyForFee'))
        extra_guest_fee = safe_float(params.get('extraGuestFee')) * MAN_EN
        peak_season_markup = safe_float(params.get('peakSeasonMarkup')) / 100
        monthly_utilities = safe_float(params.get('monthlyUtilities')) * MAN_EN

        # 修正：operating_days_cap 應該是年度可營業天數上限，通常為365天
        # 實際入住天數 = min(年度天數, 營業天數上限) * 入住率
        max_possible_nights = min(365, operating_days_cap)
        annual_booked_nights = max_possible_nights * occupancy_rate
        monthly_booked_nights = annual_booked_nights / 12
        total_effective_adr = daily_rate * (1 + peak_season_markup * 3 / 12) + max(0, avg_guests - base_occupancy_for_fee) * extra_guest_fee
        monthly_gross_revenue = monthly_booked_nights * total_effective_adr
        turnovers_per_month = monthly_booked_nights / avg_stay_duration if avg_stay_duration > 0 else 0
        monthly_operating_expenses = monthly_gross_revenue * platform_fee_rate + turnovers_per_month * cleaning_fee + monthly_utilities
    else:
        monthly_rent = 0
        vacancy_rate = 0
        initial_ratio = 0
        lease_utilities = 0
        if monetization_model == 'personalLease':
            monthly_rent = safe_float(params.get('monthlyRent')) * MAN_EN
            vacancy_rate = safe_float(params.get('vacancyRate')) / 100
            initial_ratio = safe_float(params.get('initialLeaseCostsRatio'))
            lease_utilities = safe_float(params.get('leaseUtilities')) * MAN_EN
            lease_renewal_fee_frequency = safe_float(params.get('leaseRenewalFeeFrequency'), 2)
            lease_renewal_fee_amount = safe_float(params.get('leaseRenewalFeeAmount'))
            if lease_renewal_fee_frequency > 0 and lease_renewal_fee_amount > 0:
                 annual_renewal_fee = (monthly_rent * lease_renewal_fee_amount) / lease_renewal_fee_frequency
        else: # Commercial Lease
            monthly_rent = safe_float(params.get('monthlyRentCommercial')) * MAN_EN
            vacancy_rate = safe_float(params.get('vacancyRateCommercial')) / 100
            initial_ratio = safe_float(params.get('initialLeaseCostsRatioCommercial'))
            lease_utilities = 0 # Typically tenant pays utilities for commercial
        
        monthly_gross_revenue = monthly_rent * (1 - vacancy_rate)
        one_time_initial_income = monthly_rent * initial_ratio
        monthly_operating_expenses = lease_utilities

    monthly_net_revenue = monthly_gross_revenue - monthly_operating_expenses
    
    monthly_payment = 0
    if loan_amount > 0 and loan_term > 0 and loan_interest_rate > 0:
        monthly_rate = loan_interest_rate / 12
        num_payments = loan_term * 12
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    elif loan_amount > 0 and loan_term > 0:
        monthly_payment = loan_amount / (loan_term * 12)

    credit_loan_payment = 0
    if credit_loan_for_down_payment_amount > 0:
        monthly_credit_rate = credit_loan_rate / 12
        num_credit_payments = 60 # 5 years
        credit_loan_payment = credit_loan_for_down_payment_amount * (monthly_credit_rate * (1 + monthly_credit_rate)**num_credit_payments) / ((1 + monthly_credit_rate)**num_credit_payments - 1)

    monthly_management_and_repairs = monthly_gross_revenue * management_fee_ratio
    monthly_property_tax = (property_price * property_tax_rate) / 12
    # 修正：貸款本息攤還、管理費、房屋稅等固定支出
    monthly_fixed_expenses = monthly_payment + credit_loan_payment + monthly_management_and_repairs + monthly_property_tax
    annual_fixed_expenses = monthly_fixed_expenses * 12 + annual_insurance_cost + annual_tax_accountant_fee

    cash_flows = [-total_initial_investment]
    remaining_loan = loan_amount
    annual_depreciation = (property_price * building_ratio) / (22 if building_structure == 'wood' else 47)
    annual_tax_y1 = 0
    annual_tax_y2 = 0

    for year in range(1, investment_period + 1):
        lease_renewal_fee_frequency = safe_float(params.get('leaseRenewalFeeFrequency'), 2)
        is_renewal_year = (monetization_model == 'personalLease' and annual_renewal_fee > 0 and year > 0 and year % lease_renewal_fee_frequency == 0)
        current_year_renewal_fee = annual_renewal_fee * lease_renewal_fee_frequency if is_renewal_year else 0
        
        # 正確計算年度收入（EBITDA層級）
        annual_gross_income = monthly_gross_revenue * 12 + (one_time_initial_income if year == 1 else 0) + current_year_renewal_fee
        annual_operating_expenses = monthly_operating_expenses * 12
        annual_ebitda = annual_gross_income - annual_operating_expenses
        
        # 計算實際支付的貸款利息
        annual_interest_paid = 0
        annual_credit_interest_paid = 0
        year_start_loan_balance = remaining_loan

        if remaining_loan > 0 and monthly_payment > 0:
            for m in range(12):
                if remaining_loan <= 0:
                    break
                interest = remaining_loan * (loan_interest_rate / 12)
                annual_interest_paid += interest
                principal = monthly_payment - interest
                remaining_loan = max(0, remaining_loan - principal)

        # 正確計算稅前現金流：EBITDA - 實際利息支出 - 管理費等其他費用
        pre_tax_cash_flow = annual_ebitda - annual_interest_paid - (monthly_management_and_repairs * 12) - (monthly_property_tax * 12) - annual_insurance_cost - annual_tax_accountant_fee
        post_tax_annual_cash_flow = pre_tax_cash_flow

        if purchase_type == 'corporate':
            # 法人稅計算：收入 - 各項費用 - 折舊
            taxable_income = annual_gross_income - annual_operating_expenses - annual_interest_paid - \
                           (monthly_management_and_repairs * 12) - (monthly_property_tax * 12) - \
                           annual_insurance_cost - annual_tax_accountant_fee - annual_depreciation
            annual_tax = taxable_income * corporate_tax_rate if taxable_income > 0 else 0
            if year == 1:
                annual_tax_y1 = annual_tax
            if year == 2:
                annual_tax_y2 = annual_tax
            post_tax_annual_cash_flow -= annual_tax

        if year == investment_period:
            current_property_value = property_price * ((1 + annual_appreciation) ** year)
            selling_costs = current_property_value * 0.03

            final_loan_balance = loan_amount
            if loan_amount > 0 and monthly_payment > 0:
                for y in range(investment_period):
                    if final_loan_balance <= 0:
                        break
                    for m in range(12):
                        interest = final_loan_balance * (loan_interest_rate / 12)
                        principal = monthly_payment - interest
                        final_loan_balance -= principal
            
            final_loan_balance = max(0, final_loan_balance)

            capital_gains_tax = 0
            if purchase_type == 'corporate':
                accumulated_depreciation = annual_depreciation * investment_period
                building_book_value = (property_price * building_ratio) - accumulated_depreciation
                land_value = property_price * (1 - building_ratio)
                book_value = building_book_value + land_value
                capital_gain = current_property_value - book_value - selling_costs
                if capital_gain > 0:
                    capital_gains_tax = capital_gain * corporate_tax_rate
            else: # Individual
                capital_gain = current_property_value - (property_price + total_upfront_costs)
                if capital_gain > 0:
                    tax_rate = 0.20315 if investment_period >= 5 else 0.3963
                    capital_gains_tax = capital_gain * tax_rate
            
            net_sale_proceeds = current_property_value - selling_costs - final_loan_balance - capital_gains_tax
            cash_flows.append(post_tax_annual_cash_flow + net_sale_proceeds)
        else:
            cash_flows.append(post_tax_annual_cash_flow)

    # 計算 KPI 指標
    irr = compute_irr(cash_flows)
    
    # 計算現金回報率 (使用穩定年度的現金流，通常是第二年)
    annual_net_cash_flow_stable = cash_flows[2] if len(cash_flows) > 2 else (cash_flows[1] if len(cash_flows) > 1 else 0)
    cash_on_cash_return = (annual_net_cash_flow_stable / total_initial_investment) * 100 if total_initial_investment > 0 else 0
    
    # 計算回收期
    payback_period = 0
    cumulative_cash_flow = 0
    for i, cf in enumerate(cash_flows[1:], 1):  # 跳過初始投資
        cumulative_cash_flow += cf
        if cumulative_cash_flow >= total_initial_investment:
            payback_period = i + (total_initial_investment - (cumulative_cash_flow - cf)) / cf
            break
    
    # === 新增槓桿風險指標計算 ===
    
    # 1. 計算年度債務服務總額 (Annual Debt Service - ADS)
    annual_debt_service = (monthly_payment + credit_loan_payment) * 12
    
    # 2. 計算年度淨營運收入 (Net Operating Income - NOI)
    # NOI = 總收入 - 營運費用 (不包含融資成本、折舊、稅務)
    annual_noi = (monthly_gross_revenue * 12) - (monthly_operating_expenses * 12) - (monthly_management_and_repairs * 12) - (monthly_property_tax * 12) - annual_insurance_cost
    
    # 3. DCR (Debt Coverage Ratio) - 債務覆蓋率
    dcr = annual_noi / annual_debt_service if annual_debt_service > 0 else float('inf')
    
    # 4. DSCR (Debt Service Coverage Ratio) - 債務償付覆蓋率  
    # 使用穩定年度的 EBITDA
    annual_ebitda_stable = (monthly_gross_revenue * 12) - (monthly_operating_expenses * 12)
    dscr = annual_ebitda_stable / annual_debt_service if annual_debt_service > 0 else float('inf')
    
    # 5. LTV (Loan-to-Value) - 貸款價值比
    total_loan_amount = loan_amount + credit_loan_for_down_payment_amount
    ltv = (total_loan_amount / property_price) * 100 if property_price > 0 else 0
    
    # 6. 槓桿倍數 (Leverage Ratio)
    leverage_ratio = total_loan_amount / total_initial_investment if total_initial_investment > 0 else 0
    
    # 7. 槓桿後 ROE (Leveraged Return on Equity)
    # 使用稅後淨現金流計算
    leveraged_roe = (annual_net_cash_flow_stable / total_initial_investment) * 100 if total_initial_investment > 0 else 0
    
    # 8. 計算健康度評級
    def get_health_rating(dcr, dscr, ltv, cocr):
        """
        根據關鍵指標計算投資健康度
        返回: (rating, color, description)
        """
        danger_count = 0
        warning_count = 0
        
        # DCR 評估
        if dcr < 1.10:
            danger_count += 1
        elif dcr < 1.25:
            warning_count += 1
            
        # DSCR 評估  
        if dscr < 1.15:
            danger_count += 1
        elif dscr < 1.30:
            warning_count += 1
            
        # LTV 評估
        if ltv > 85:
            danger_count += 1
        elif ltv > 75:
            warning_count += 1
            
        # CoCR 評估
        if cocr < 3:
            danger_count += 1
        elif cocr < 5:
            warning_count += 1
        
        if danger_count >= 2:
            return ("危險", "danger", "多項關鍵指標低於安全標準，投資風險較高")
        elif danger_count >= 1 or warning_count >= 3:
            return ("警告", "warning", "部分指標需要關注，建議優化投資結構")
        elif warning_count >= 1:
            return ("良好", "good", "整體表現良好，少數指標有改善空間")
        else:
            return ("優秀", "excellent", "各項指標表現優異，投資結構健康")
    
    health_rating, health_color, health_description = get_health_rating(dcr, dscr, ltv, cash_on_cash_return)
    
    # 準備年度預測數據
    annual_projections = []
    current_property_value = property_price
    projection_loan_balance = loan_amount
    
    for year in range(1, investment_period + 1):
        current_property_value = property_price * ((1 + annual_appreciation) ** year)
        
        # 正確計算年末貸款餘額
        if projection_loan_balance > 0 and monthly_payment > 0:
            for m in range(12):
                if projection_loan_balance <= 0:
                    break
                interest = projection_loan_balance * (loan_interest_rate / 12)
                principal = monthly_payment - interest
                projection_loan_balance = max(0, projection_loan_balance - principal)
        
        net_equity = current_property_value - projection_loan_balance
        
        annual_projections.append({
            "year": year,
            "net_cash_flow": (cash_flows[year] if year < len(cash_flows) else 0) / MAN_EN,
            "property_value": current_property_value / MAN_EN,  # 轉換為萬円
            "loan_balance": projection_loan_balance / MAN_EN,  # 轉換為萬円
            "net_equity": net_equity / MAN_EN,  # 轉換為萬円
            "net_equity_twd": (net_equity / MAN_EN) * exchange_rate  # 轉換為萬台幣
        })

    results = {
        "kpi": {
            "cash_on_cash_return": cash_on_cash_return,
            "irr": irr * 100 if irr else 0,  # 轉換為百分比
            "payback_period": payback_period
        },
        "leverage_metrics": {
            "dcr": dcr,
            "dscr": dscr, 
            "ltv": ltv,
            "leverage_ratio": leverage_ratio,
            "leveraged_roe": leveraged_roe,
            "annual_debt_service_jpy": annual_debt_service / MAN_EN,
            "annual_debt_service_twd": (annual_debt_service / MAN_EN) * exchange_rate,
            "annual_noi_jpy": annual_noi / MAN_EN,
            "annual_noi_twd": (annual_noi / MAN_EN) * exchange_rate,
            "health_rating": health_rating,
            "health_color": health_color,
            "health_description": health_description
        },
        "initial_investment": {
            "total_investment_jpy": total_initial_investment / MAN_EN,
            "total_investment_twd": (total_initial_investment / MAN_EN) * exchange_rate,
            "acquisition_costs_jpy": total_upfront_costs / MAN_EN,
            "acquisition_costs_twd": (total_upfront_costs / MAN_EN) * exchange_rate,
            "initial_setup_costs_jpy": (initial_furnishing_cost + corporate_setup_cost) / MAN_EN,
            "initial_setup_costs_twd": ((initial_furnishing_cost + corporate_setup_cost) / MAN_EN) * exchange_rate,
            "down_payment_own_capital_jpy": own_capital_for_down_payment_amount / MAN_EN,
            "down_payment_own_capital_twd": (own_capital_for_down_payment_amount / MAN_EN) * exchange_rate,
            "down_payment_credit_loan_jpy": credit_loan_for_down_payment_amount / MAN_EN,
            "down_payment_credit_loan_twd": (credit_loan_for_down_payment_amount / MAN_EN) * exchange_rate,
            "loan_amount_jpy": loan_amount / MAN_EN,
            "loan_amount_twd": (loan_amount / MAN_EN) * exchange_rate
        },
        "cash_flow": {
            # 保留原始日幣數據供內部使用
            "total_revenue_y1": (monthly_gross_revenue * 12 + one_time_initial_income) / MAN_EN,
            "total_revenue_y2": monthly_gross_revenue * 12 / MAN_EN,
            "total_expenses_y1": monthly_operating_expenses * 12 / MAN_EN,
            "total_expenses_y2": monthly_operating_expenses * 12 / MAN_EN,
            "ebitda_y1": ((monthly_gross_revenue * 12 + one_time_initial_income) - monthly_operating_expenses * 12) / MAN_EN,
            "ebitda_y2": (monthly_gross_revenue * 12 - monthly_operating_expenses * 12) / MAN_EN,
            "depreciation": annual_depreciation / MAN_EN,
            "interest_payment_y1": (loan_interest_rate * loan_amount if loan_amount > 0 else 0) / MAN_EN,
            "interest_payment_y2": (loan_interest_rate * (loan_amount * 0.9) if loan_amount > 0 else 0) / MAN_EN,
            "ebt_y1": (((monthly_gross_revenue * 12 + one_time_initial_income) - monthly_operating_expenses * 12) - annual_depreciation - (loan_interest_rate * loan_amount if loan_amount > 0 else 0) - (monthly_management_and_repairs * 12) - (monthly_property_tax * 12) - annual_insurance_cost - annual_tax_accountant_fee) / MAN_EN,
            "ebt_y2": ((monthly_gross_revenue * 12 - monthly_operating_expenses * 12) - annual_depreciation - (loan_interest_rate * (loan_amount * 0.9) if loan_amount > 0 else 0) - (monthly_management_and_repairs * 12) - (monthly_property_tax * 12) - annual_insurance_cost - annual_tax_accountant_fee) / MAN_EN,
            "tax_y1": annual_tax_y1 / MAN_EN,
            "tax_y2": annual_tax_y2 / MAN_EN,
            "net_cash_flow_y1": cash_flows[1] / MAN_EN if len(cash_flows) > 1 else 0,
            "net_cash_flow_y2": cash_flows[2] / MAN_EN if len(cash_flows) > 2 else (cash_flows[1] / MAN_EN if len(cash_flows) > 1 else 0),
            
            # 新增台幣換算的穩定年度現金流（用於新的表格格式）
            "total_revenue_stable_twd": ((monthly_gross_revenue * 12) / MAN_EN) * exchange_rate,
            "total_expenses_stable_twd": ((monthly_operating_expenses * 12) / MAN_EN) * exchange_rate,
            "ebitda_stable_twd": (((monthly_gross_revenue * 12) - (monthly_operating_expenses * 12)) / MAN_EN) * exchange_rate,
            "depreciation_twd": (annual_depreciation / MAN_EN) * exchange_rate,
            "interest_payment_stable_twd": ((loan_interest_rate * (loan_amount * 0.9) if loan_amount > 0 else 0) / MAN_EN) * exchange_rate,
            "ebt_stable_twd": (((monthly_gross_revenue * 12 - monthly_operating_expenses * 12) - annual_depreciation - (loan_interest_rate * (loan_amount * 0.9) if loan_amount > 0 else 0) - (monthly_management_and_repairs * 12) - (monthly_property_tax * 12) - annual_insurance_cost - annual_tax_accountant_fee) / MAN_EN) * exchange_rate,
            "tax_stable_twd": (annual_tax_y2 / MAN_EN) * exchange_rate,
            "net_cash_flow_stable_twd": ((cash_flows[2] if len(cash_flows) > 2 else (cash_flows[1] if len(cash_flows) > 1 else 0)) / MAN_EN) * exchange_rate
        },
        "annual_projections": annual_projections,
        "suggestions": []  # 可以後續添加建議邏輯
    }

    # 調試輸出
    app.logger.info(f"=== 調試資訊 ===")
    app.logger.info(f"房價: {property_price/MAN_EN:.1f}萬円")
    app.logger.info(f"初始投資: {total_initial_investment/MAN_EN:.1f}萬円")
    app.logger.info(f"月收入: {monthly_gross_revenue/MAN_EN:.1f}萬円")
    app.logger.info(f"月支出: {monthly_operating_expenses/MAN_EN:.1f}萬円")
    app.logger.info(f"月貸款: {monthly_payment/MAN_EN:.1f}萬円")
    app.logger.info(f"年度現金流[1]: {cash_flows[1]/MAN_EN:.1f}萬円" if len(cash_flows) > 1 else "年度現金流[1]: 無資料")
    app.logger.info(f"年度現金流[2]: {cash_flows[2]/MAN_EN:.1f}萬円" if len(cash_flows) > 2 else "年度現金流[2]: 無資料")
    app.logger.info(f"計算完成 - 物件價格: {property_price/exchange_rate:.0f} TWD, 投資期間: {investment_period} 年")
    
    return jsonify(results)

def compute_irr(cash_flows, initial_investment_period=10, tolerance=1e-6, max_iterations=100):
    """計算 IRR (內部報酬率)"""
    def npv(rate):
        return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))
    
    # 使用二分法求解
    low, high = -0.99, 10.0
    for _ in range(max_iterations):
        mid = (low + high) / 2
        npv_mid = npv(mid)
        if abs(npv_mid) < tolerance:
            return mid
        elif npv_mid > 0:
            low = mid
        else:
            high = mid
    return None

if __name__ == '__main__':
    # 在開發環境啟用除錯模式
    debug_mode = ENVIRONMENT == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 