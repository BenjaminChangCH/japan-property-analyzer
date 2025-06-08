from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import math
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app) # 允許跨域請求

@app.route('/')
def index():
    # 根據環境變數決定 GA 追蹤 ID
    ga_tracking_id = os.environ.get('GA_TRACKING_ID', '')
    environment = os.environ.get('ENVIRONMENT', 'development')
    
    return render_template('index.html', 
                         ga_tracking_id=ga_tracking_id,
                         environment=environment)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
def calculate():
    params = request.get_json()
    
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

        annual_booked_nights = operating_days_cap * occupancy_rate
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
    total_annual_expenses = (monthly_payment + credit_loan_payment + monthly_management_and_repairs + monthly_property_tax) * 12 + annual_insurance_cost + annual_tax_accountant_fee

    cash_flows = [-total_initial_investment]
    remaining_loan = loan_amount
    annual_depreciation = (property_price * building_ratio) / (22 if building_structure == 'wood' else 47)
    annual_tax_y1 = 0
    annual_tax_y2 = 0

    for year in range(1, investment_period + 1):
        lease_renewal_fee_frequency = safe_float(params.get('leaseRenewalFeeFrequency'), 2)
        is_renewal_year = (monetization_model == 'personalLease' and annual_renewal_fee > 0 and year > 0 and year % lease_renewal_fee_frequency == 0)
        current_year_renewal_fee = annual_renewal_fee * lease_renewal_fee_frequency if is_renewal_year else 0
        
        annual_income = monthly_net_revenue * 12 + (one_time_initial_income if year == 1 else 0) + current_year_renewal_fee
        
        annual_interest_paid = 0
        annual_credit_interest_paid = 0 # This part is simplified

        if remaining_loan > 0 and monthly_payment > 0:
            for m in range(12):
                interest = remaining_loan * (loan_interest_rate / 12)
                annual_interest_paid += interest
                principal = monthly_payment - interest
                remaining_loan -= principal

        post_tax_annual_cash_flow = annual_income - total_annual_expenses

        if purchase_type == 'corporate':
            annual_management_and_repairs_value = monthly_management_and_repairs * 12
            annual_property_tax_value = monthly_property_tax * 12
            taxable_income = (monthly_gross_revenue * 12 + (one_time_initial_income if year == 1 else 0) + current_year_renewal_fee) - \
                             (monthly_operating_expenses * 12) - \
                             annual_interest_paid - \
                             annual_credit_interest_paid - \
                             annual_management_and_repairs_value - \
                             annual_property_tax_value - \
                             annual_insurance_cost - \
                             annual_tax_accountant_fee - \
                             annual_depreciation
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

    results = {
        "totalInitialInvestment": total_initial_investment,
        "totalCost": total_cost,
        "downPaymentAmount": down_payment_amount,
        "downPaymentRatio": down_payment_ratio,
        "ownCapitalForDownPaymentAmount": own_capital_for_down_payment_amount,
        "creditLoanForDownPaymentAmount": credit_loan_for_down_payment_amount,
        "loanAmount": loan_amount,
        "monthlyNetRevenue": monthly_net_revenue,
        "totalAnnualExpenses": total_annual_expenses,
        "oneTimeInitialIncome": one_time_initial_income,
        "annualRenewalFee": annual_renewal_fee,
        "cashFlows": cash_flows,
        "investmentPeriod": investment_period,
        "purchaseType": purchase_type,
        "corporateTaxRate": corporate_tax_rate,
        "exchangeRate": exchange_rate,
        "annualAppreciation": annual_appreciation,
        "propertyPrice": property_price,
        "loanInterestRate": loan_interest_rate,
        "loanTerm": loan_term,
        "monthlyGrossRevenue": monthly_gross_revenue,
        "monthlyOperatingExpenses": monthly_operating_expenses,
        "annualDebtService": (monthly_payment + credit_loan_payment) * 12,
        "annualManagementFee": monthly_management_and_repairs * 12,
        "annualPropertyTax": monthly_property_tax * 12,
        "annualInsuranceCost": annual_insurance_cost,
        "annualTaxAccountantFee": annual_tax_accountant_fee,
        "annualTax_y1": annual_tax_y1,
        "annualTax_y2": annual_tax_y2
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 