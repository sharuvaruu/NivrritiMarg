import yfinance as yf
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import joblib

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

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

def fetch_stock_data(tickers):
    stock_data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5y")  # Last 5 years of data
            if not hist.empty:
                model_path = os.path.join(model_dir, f"{ticker}_lstm.pkl")
                scaler_path = os.path.join(model_dir, f"{ticker}_scaler.pkl")

                if os.path.exists(model_path) and os.path.exists(scaler_path):
                    model = joblib.load(model_path)
                    scaler = joblib.load(scaler_path)
                else:
                    data = hist[['Close']].values
                    scaler = MinMaxScaler(feature_range=(0,1))
                    data_scaled = scaler.fit_transform(data)
                    X_train = []
                    y_train = []
                    for i in range(60, len(data_scaled)):
                        X_train.append(data_scaled[i-60:i, 0])
                        y_train.append(data_scaled[i, 0])
                    X_train, y_train = np.array(X_train), np.array(y_train)
                    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

                    model = Sequential()
                    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
                    model.add(LSTM(units=50))
                    model.add(Dense(1))

                    model.compile(optimizer='adam', loss='mean_squared_error')
                    model.fit(X_train, y_train, epochs=1, batch_size=32)

                    # Save the model and scaler
                    joblib.dump(model, model_path)
                    joblib.dump(scaler, scaler_path)

                # Predict future prices
                data = scaler.transform(hist[['Close']])
                X_test = []
                for i in range(60, len(data)):
                    X_test.append(data[i-60:i, 0])
                X_test = np.array(X_test)
                X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
                predicted_stock_price = model.predict(X_test)
                predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
                hist['Predicted'] = np.nan
                hist.iloc[60:, hist.columns.get_loc('Predicted')] = predicted_stock_price.flatten()   

                # Calculate annual return and volatility based on predicted prices
                annual_return = hist['Predicted'].pct_change().mean() * 252 * 100
                volatility = hist['Predicted'].pct_change().std() * np.sqrt(252) * 100
                beta = stock.info.get('beta', 1)
                sharpe_ratio = annual_return / volatility
                risk_profile = 'Low' if volatility < 7 else 'Medium' if volatility < 10 else 'High'

                stock_data.append({
                    'Stock Name': ticker,
                    'Annual Return (%)': annual_return,
                    'Volatility (%)': volatility,
                    'Beta': beta,
                    'Sharpe Ratio': sharpe_ratio,
                    'Risk Profile': risk_profile
                })
        except Exception as e:
            print(f"Error processing ticker {ticker}: {e}")
    return pd.DataFrame(stock_data)

def suggest_investment(df, years, target_fund, monthly_investment, risk_category):
    df = df.copy()

    if risk_category == "high":
        df = df[df['Risk Profile'] == 'High']
    elif risk_category == "medium":
        df = df[df['Risk Profile'] == 'Medium']
    elif risk_category == "low":
        df = df[df['Risk Profile'] == 'Low']

    # Basic portfolio suggestion based on risk profile
    df['Allocation'] = 0.0
    total_allocation = 0.0
    for index, row in df.iterrows():
        if total_allocation < 100:
            allocation = 100 / len(df)
            df.at[index, 'Allocation'] = allocation
            total_allocation += allocation

    future_value = (monthly_investment * (((1 + 0.1 / 12) ** (12 * years) - 1) / (0.1 / 12))) * (1 + 0.1 / 12)
    total_invested = monthly_investment * 12 * years
    average_annual_return = 0.1
    total_future_value = future_value

    # Risk estimate (mock example)
    risk_estimate = {
        'mean': future_value * 0.9,
        'std_dev': future_value * 0.1,
        'confidence_interval': (future_value * 0.8, future_value * 1.2)
    }

    return {
        'allocations': df[['Stock Name', 'Allocation']].values.tolist(),
        'total_future_value': total_future_value,
        'average_annual_return_percentage': average_annual_return * 100,
        'total_invested': total_invested,
        'risk_estimate': risk_estimate
    }