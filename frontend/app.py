import streamlit as st
import requests
import json
import time

# Set page configuration
st.set_page_config(page_title="NivrritiMarg - AI Engine", layout="wide")

# Add custom CSS for styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inria+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap');

    .main {
        background-color: #fff4e6;
        color: #3c2f2f;
        font-family: 'Inria Sans', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #be9b7b;
        color: #3c2f2f;
        font-family: 'Inria Sans', sans-serif;
    }
    .stButton>button {
        border-radius: 12px;
        background-color: #854442;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 10px 20px;
        transition: background-color 0.3s, transform 0.3s;
        font-family: 'Inria Sans', sans-serif;
    }
    .stButton>button:hover {
        background-color: #4b3832;
        transform: scale(1.05);
    }
    h1 {
        color: #3c2f2f;
        font-family: 'Inria Sans', sans-serif;
    }
    .card {
        border-radius: 10px;
        background: #be9b7b;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 10px;
        padding: 10px;
        display: inline-block;
        width: calc(33% - 20px);
        vertical-align: top;
        font-family: 'Inria Sans', sans-serif;
    }
    .card-title {
        font-size: 18px;
        font-weight: bold;
        color: #3c2f2f;
    }
    .card-content {
        font-size: 16px;
        color: #3c2f2f;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.title('🎯 NivrritiMarg - AI Engine for Retirement Investment Allocation 🌟')
st.write("Welcome to NivrritiMarg! Plan your retirement with our AI-powered investment optimizer. 🚀")

# Input fields with enhanced styling
st.sidebar.header('Input Details 📝')
current_age = st.sidebar.number_input('🔢 Current Age', min_value=0, max_value=100, value=30)
retirement_age = st.sidebar.number_input('🔢 Retirement Age', min_value=current_age + 1, max_value=100, value=60)
desired_fund = st.sidebar.number_input('💰 Desired Retirement Fund (INR)', min_value=0, value=1000000)
monthly_investment = st.sidebar.number_input('💵 Monthly Investment (INR)', min_value=0, value=5000)
risk_category = st.sidebar.selectbox('⚠️ Select Risk Category', ['low', 'medium', 'high'])

# Submit button with animation
if st.sidebar.button('🚀 Get Investment Strategy'):
    payload = {
        'currentAge': current_age,
        'retirementAge': retirement_age,
        'desiredFund': desired_fund,
        'monthlyInvestment': monthly_investment,
        'riskCategory': risk_category
    }

    with st.spinner('Calculating investment strategy...'):
        try:
            # Start the calculation
            response = requests.post('http://localhost:5000/investment-strategy', json=payload, timeout=10)
            response.raise_for_status()
            job_data = response.json()
            
            if 'job_id' in job_data:
                # Poll for results
                while True:
                    time.sleep(5)  # Wait for 5 seconds before checking again
                    status_response = requests.get(f'http://localhost:5000/check-status/{job_data["job_id"]}', timeout=10)
                    status_data = status_response.json()
                    
                    if 'status' in status_data and status_data['status'] == 'processing':
                        st.write("Still processing...")
                    else:
                        # Results are ready
                        data = status_data
                        break
            else:
                st.error("Invalid response from server")
                st.stop()
            
            # Display Investment Recommendations
            st.success("Investment strategy calculated successfully!")
            st.write("### Investment Recommendations:")
            if 'allocations' in data:
                for stock, percentage in data['allocations']:
                    st.write(f"📊 **{stock}**: {percentage:.2f}%")
                st.write(f"💸 **Total Future Value**: ₹{data['total_future_value']:,.2f}")
                st.write(f"📉 **Average Annual Return**: {data['average_annual_return_percentage']:.2f}%")
                st.write(f"💰 **Total Invested**: ₹{data['total_invested']:,.2f}")
                
                # Display Risk Estimate
                st.write("### ⚠️ Risk Estimate:")
                st.markdown(f"<div class='card'><div class='card-title'>🔮 Mean Future Value</div><div class='card-content'>₹{data['risk_estimate']['mean']:,.2f}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='card'><div class='card-title'>📈 Standard Deviation</div><div class='card-content'>₹{data['risk_estimate']['std_dev']:,.2f}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='card'><div class='card-title'>🎯 90% Confidence Interval</div><div class='card-content'>₹{data['risk_estimate']['confidence_interval'][0]:,.2f} to ₹{data['risk_estimate']['confidence_interval'][1]:,.2f}</div></div>", unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
