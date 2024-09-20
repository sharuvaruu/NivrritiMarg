import yfinance as yf
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import joblib
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of Indian stock tickers, mutual funds, gold ETFs, and bonds
investment_tickers = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "KOTAKBANK.NS", "LT.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS",
    "HINDUNILVR.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJFINANCE.NS",
    "MARUTI.NS", "M&M.NS", "SUNPHARMA.NS", "HCLTECH.NS", "ONGC.NS",
    "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS", "ADANIGREEN.NS", "DMART.NS",
    # Mutual Funds
    "0P0000YENW.BO", "0P0000ZG0G.BO", "0P0000YIV3.BO",
    # Gold
    "GLD",
    # Bonds
    "TLT"
]

model_dir = "saved_models"
os.makedirs(model_dir, exist_ok=True)

def create_lstm_model(input_shape: tuple) -> Sequential:
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=input_shape),
        LSTM(units=50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def process_ticker(ticker: str) -> Dict:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5y")
        if hist.empty:
            return None

        model_path = os.path.join(model_dir, f"{ticker}_lstm.pkl")
        scaler_path = os.path.join(model_dir, f"{ticker}_scaler.pkl")

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
        else:
            data = hist[['Close']].values
            scaler = MinMaxScaler(feature_range=(0,1))
            data_scaled = scaler.fit_transform(data)
            X_train, y_train = [], []
            for i in range(60, len(data_scaled)):
                X_train.append(data_scaled[i-60:i, 0])
                y_train.append(data_scaled[i, 0])
            X_train, y_train = np.array(X_train), np.array(y_train)
            X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

            model = create_lstm_model((X_train.shape[1], 1))
            model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

            joblib.dump(model, model_path)
            joblib.dump(scaler, scaler_path)

        data = scaler.transform(hist[['Close']])
        X_test = np.array([data[i-60:i, 0] for i in range(60, len(data))])
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        predicted_stock_price = model.predict(X_test)
        predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
        
        hist['Predicted'] = np.nan
        hist.iloc[60:, hist.columns.get_loc('Predicted')] = predicted_stock_price.flatten()

        annual_return = hist['Predicted'].pct_change().mean() * 252 * 100
        volatility = hist['Predicted'].pct_change().std() * np.sqrt(252) * 100
        beta = stock.info.get('beta', 1)
        sharpe_ratio = annual_return / volatility if volatility != 0 else 0
        risk_profile = 'Low' if volatility < 15 else 'Medium' if volatility < 25 else 'High'

        return {
            'Stock Name': ticker,
            'Annual Return (%)': annual_return,
            'Volatility (%)': volatility,
            'Beta': beta,
            'Sharpe Ratio': sharpe_ratio,
            'Risk Profile': risk_profile
        }
    except Exception as e:
        print(f"Error processing ticker {ticker}: {e}")
        return None

def fetch_stock_data(tickers: List[str]) -> pd.DataFrame:
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_ticker, ticker) for ticker in tickers]
        stock_data = [future.result() for future in as_completed(futures) if future.result()]
    return pd.DataFrame(stock_data)

def suggest_investment(df: pd.DataFrame, years: int, target_fund: float, monthly_investment: float, risk_category: str) -> Dict:
    df = df.copy()

    risk_filters = {
        "high": df['Risk Profile'] == 'High',
        "medium": df['Risk Profile'].isin(['Medium', 'High']),
        "low": df['Risk Profile'].isin(['Low', 'Medium', 'High'])
    }
    df = df[risk_filters.get(risk_category.lower(), True)]

    if df.empty:
        return {"error": "No investments match the specified risk category"}

    # Improved allocation strategy based on Sharpe ratio
    total_sharpe = df['Sharpe Ratio'].sum()
    df['Allocation'] = (df['Sharpe Ratio'] / total_sharpe) * 100

    # Calculate expected return and risk
    portfolio_return = (df['Annual Return (%)'] * df['Allocation'] / 100).sum()
    portfolio_volatility = np.sqrt((df['Volatility (%)'] ** 2 * (df['Allocation'] / 100) ** 2).sum())

    # Monte Carlo simulation for risk estimate
    num_simulations = 10000
    sim_returns = np.random.normal(portfolio_return / 100 / 12, portfolio_volatility / 100 / np.sqrt(12), (num_simulations, years * 12))
    sim_returns = np.cumprod(1 + sim_returns, axis=1)
    sim_final_values = monthly_investment * sim_returns.sum(axis=1)

    total_invested = monthly_investment * 12 * years
    mean_final_value = np.mean(sim_final_values)
    std_dev_final_value = np.std(sim_final_values)

    risk_estimate = {
        'mean': mean_final_value,
        'std_dev': std_dev_final_value,
        'confidence_interval': (np.percentile(sim_final_values, 5), np.percentile(sim_final_values, 95))
    }

    return {
        'allocations': df[['Stock Name', 'Allocation']].values.tolist(),
        'total_future_value': mean_final_value,
        'average_annual_return_percentage': portfolio_return,
        'total_invested': total_invested,
        'risk_estimate': risk_estimate
    }

# Example usage
if __name__ == "__main__":
    stock_data = fetch_stock_data(investment_tickers)
    result = suggest_investment(stock_data, years=10, target_fund=1000000, monthly_investment=10000, risk_category="medium")
    print(result)