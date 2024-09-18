import logging
from flask import Flask, request, jsonify
from investment_strategy import fetch_stock_data, suggest_investment, investment_tickers
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/investment-strategy', methods=['POST'])
def investment_strategy():
    data = request.json
    logging.debug(f"Received data: {data}")
    
    try:
        current_age = int(data['currentAge'])
        retirement_age = int(data['retirementAge'])
        desired_retirement_fund = float(data['desiredFund'])
        monthly_investment = float(data['monthlyInvestment'])
        risk_category = data['riskCategory']
    except (KeyError, ValueError) as e:
        logging.error(f"Error parsing input data: {e}")
        return jsonify({'error': 'Invalid input data'}), 400

    years_to_invest = retirement_age - current_age

    if years_to_invest <= 0:
        logging.error("Invalid retirement age or current age")
        return jsonify({'error': 'Invalid retirement age or current age'}), 400

    # Fetch the stock data
    try:
        df_stocks = fetch_stock_data(investment_tickers)
        investment_strategy = suggest_investment(df_stocks, years_to_invest, desired_retirement_fund, monthly_investment, risk_category)
    except Exception as e:
        logging.error(f"Error in investment calculation: {e}")
        return jsonify({'error': 'Error calculating investment strategy'}), 500

    logging.debug(f"Investment strategy result: {investment_strategy}")
    return jsonify(investment_strategy)

if __name__ == '__main__':
    app.run(debug=True)
