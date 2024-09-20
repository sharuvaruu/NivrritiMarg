import logging
from flask import Flask, request, jsonify
from improved import fetch_stock_data, suggest_investment, investment_tickers
from flask_cors import CORS
from threading import Thread
import queue

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Queue to store results
result_queue = queue.Queue()

def process_investment_strategy(data, result_queue):
    try:
        current_age = int(data['currentAge'])
        retirement_age = int(data['retirementAge'])
        desired_retirement_fund = float(data['desiredFund'])
        monthly_investment = float(data['monthlyInvestment'])
        risk_category = data['riskCategory']
        
        years_to_invest = retirement_age - current_age
        
        if years_to_invest <= 0:
            result_queue.put({'error': 'Invalid retirement age or current age'})
            return
        
        logging.info("Fetching stock data")
        df_stocks = fetch_stock_data(investment_tickers)
        logging.info("Calculating investment strategy")
        investment_strategy = suggest_investment(df_stocks, years_to_invest, desired_retirement_fund, monthly_investment, risk_category)
        
        result_queue.put(investment_strategy)
    except Exception as e:
        logging.error(f"Error in investment calculation: {str(e)}")
        result_queue.put({'error': f'Error calculating investment strategy: {str(e)}'})

@app.route('/investment-strategy', methods=['POST'])
def investment_strategy():
    logging.info("Received request for investment strategy")
    data = request.json
    logging.debug(f"Received data: {data}")
    
    # Start processing in a separate thread
    thread = Thread(target=process_investment_strategy, args=(data, result_queue))
    thread.start()
    
    # Return immediately with a job ID (you can implement a proper job ID system)
    return jsonify({'status': 'processing', 'job_id': '12345'})

@app.route('/check-status/<job_id>', methods=['GET'])
def check_status(job_id):
    if not result_queue.empty():
        result = result_queue.get()
        return jsonify(result)
    else:
        return jsonify({'status': 'processing'})

if __name__ == '__main__':
    logging.info("Starting Flask server")
    app.run(host='0.0.0.0', port=5000, debug=True)