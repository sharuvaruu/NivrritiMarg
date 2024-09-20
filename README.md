# 📈 **NivrritiMarg** - AI-Powered Retirement Investment Allocation Platform 🚀

Welcome to **NivrritiMarg**, your go-to AI engine for simplifying retirement planning. By using historical stock, mutual fund, and bond data, our platform generates an optimal investment strategy tailored to your financial goals and risk preferences. 🌟

## 🔍 **Project Overview**

NivrritiMarg provides users with personalized investment allocation plans by analyzing five years of historical financial data from various Indian stocks, mutual funds, and other asset classes. The model predicts future trends using LSTM-based deep learning techniques and assists in making informed investment decisions based on user-defined inputs.

### 📊 **Key Features**

- **Deep Learning (LSTM) for Stock Prediction**: Our system utilizes LSTM models to predict future stock prices based on historical data.
- **Risk Profiling**: Tailor your portfolio based on low, medium, or high-risk preferences.
- **Future Value Prediction**: Predict future value based on monthly investments, risk categories, and desired retirement goals.
- **Sharpe Ratio & Volatility Analysis**: Understand the risk-return trade-off for each investment.

### 💼 **Tech Stack**

The project is powered by the following technologies:

- **Python** 🐍: Core programming language for the backend.
- **Flask** 🧩: Backend framework for building the server and API.
- **Streamlit** 📱: Frontend UI for user interaction.
- **CSS** 🎨: Styling the user interface for a polished look.
- **HTML** 🌐: Structuring the web content.
- **yfinance** 📊: Fetching historical stock data.
- **Keras** 🧠: For building and training the LSTM models.
- **Pandas & NumPy** 📈: Data handling and processing.
- **MinMaxScaler**: Data normalization for LSTM model input.


### 📋 **How to Use**

#### Input Parameters:

- **Current Age**: The user's current age.
- **Retirement Age**: The desired retirement age.
- **Monthly Investment**: Amount of money the user is willing to invest monthly.
- **Target Retirement Fund**: The amount of money the user wants to have saved by retirement.
- **Risk Category**: Low, medium, or high risk preference for investment.

#### Suggested Investment Plan:

- **Allocation**: The app suggests an allocation of stocks, mutual funds, and bonds based on the risk profile.
- **Future Value**: It estimates the future value of the investment based on monthly contributions and market growth.
- **Risk Estimate**: The system provides a risk estimate, which includes confidence intervals and projected returns.

---

## 🚀 **Getting Started**

### 1. 🛠️ **Clone the Repository**

```bash
git clone https://github.com/sharuvaruu/NivrritiMarg.git
cd NivrritiMarg
```

### 2. 📦 **Install Dependencies**

Make sure to install the required libraries:

```bash
pip install -r requirements.txt
```

### 3. ▶️ **Run the Application**

Start the application:

```bash
streamlit run app.py

```
### 4. 🤝 **Contributing**

If you have suggestions for improvements or want to contribute to **NivrritiMarg**, we’d love to hear from you! 

Feel free to submit issues or pull requests with your ideas or enhancements. Your contributions can help make this project even better.

### How to Contribute

1. **Fork the Repository**: Create your own copy of the repository by clicking the "Fork" button.
2. **Create a Branch**: Create a new branch for your changes.
   ```bash
   git checkout -b feature/your-feature
   ```

--
### Thankyou for visiting


