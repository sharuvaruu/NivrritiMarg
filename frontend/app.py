import streamlit as st
import requests
import json
import time
import pandas as pd
import numpy as np
from typing import Dict

# Set page configuration
st.set_page_config(page_title="NivrritiMarg - AI Engine", layout="wide")

# Add custom CSS for styling
st.markdown("""
    <style>
        /* Main background color */
        .stApp {
            background-color: #FDFCFB; /* Original background */
        }

        /* Title styles */
        .title {
            color: #000000 !important; /* Dark title color */
            font-size: 2.5rem;
            font-family: 'Arial', sans-serif;
            margin-bottom: 20px; /* Space below title */
        }

        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #f04d6c; /* Sidebar background color */
            border-radius: 5px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            color: #000000; /* Dark text color for sidebar */
        }

        /* Button styles */
        .stButton > button {
            background-color: #f04d6c; /* Button color */
            color: #000000; /* Black text color */
            border-radius: 5px;
            border: none;
            padding: 10px 20px; /* Added padding for better appearance */
            font-size: 16px; /* Increased font size */
            font-weight: bold; /* Bold text for better readability */
            cursor: pointer; /* Pointer cursor for buttons */
            transition: background-color 0.3s, transform 0.2s; /* Added transition effects */
        }

        .stButton > button:hover {
            background-color: #faab74; /* Darker shade on hover */
            transform: scale(1.05); /* Slightly enlarge button on hover */
        }

        /* Input field styles */
        input[type="number"], select {
            border: 2px solid #f04d6c; /* Input border color */
            border-radius: 5px;
            padding: 10px; /* Added padding for better input field appearance */
            font-size: 16px; /* Increased font size for inputs */
            color: #FFFFFF; /* White text color for input fields */
            background-color: #f04d6c; /* Matching input background with the sidebar */
        }

        /* Result text styles */
        .stSubheader, .stMarkdown, .stWrite, .stError {
            color: #000000; /* Dark text color for results */
        }

        /* Custom styles for processing message */
        .processing {
            color: #000000; /* Plain black text for processing message */
            font-size: 16px; /* Font size for processing message */
        }

        /* Additional custom animations */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        .fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.markdown('<h1 class="title">🎯 NivrritiMarg - AI Engine for Retirement Investment Allocation 🌟</h1>', unsafe_allow_html=True)
st.write("Welcome to NivrritiMarg! Plan your retirement with our AI-powered investment optimizer. 🚀")

# Input fields with enhanced styling
st.sidebar.header('Input Details 📝')
current_age = st.sidebar.number_input('🔢 Current Age', min_value=0, max_value=100, value=30)
retirement_age = st.sidebar.number_input('🔢 Retirement Age', min_value=current_age + 1, max_value=100, value=60)
desired_fund = st.sidebar.number_input('💰 Desired Retirement Fund (INR)', min_value=0, value=1000000)
monthly_investment = st.sidebar.number_input('💵 Monthly Investment (INR)', min_value=0, value=5000)
risk_category = st.sidebar.selectbox('📊 Risk Category', ['Low', 'Medium', 'High'])

# Button to submit data
if st.sidebar.button('Calculate Investment Strategy'):
    # Collect input data
    input_data = {
        'currentAge': current_age,
        'retirementAge': retirement_age,
        'desiredFund': desired_fund,
        'monthlyInvestment': monthly_investment,
        'riskCategory': risk_category
    }
    
    # Call the Flask API
    response = requests.post('http://127.0.0.1:5000/investment-strategy', json=input_data)

    # Check the response
    if response.status_code == 200:
        job_id = response.json().get('job_id')
        st.markdown('<p class="processing">Processing your request...</p>', unsafe_allow_html=True)  # Plain black text for processing message

        # Poll for results
        while True:
            time.sleep(2)  # Polling delay
            status_response = requests.get(f'http://127.0.0.1:5000/check-status/{job_id}')
            status_data = status_response.json()

            if 'error' in status_data:
                st.error(status_data['error'])  # Error messages should also be dark
                break
            elif status_data.get('status') != 'processing':
                # Successfully received results
                investment_allocation = status_data.get('Investment Allocation', pd.DataFrame())
                expected_return = status_data.get('Expected Portfolio Return', None)
                expected_volatility = status_data.get('Expected Portfolio Volatility', None)
                total_return = status_data.get('Total Investment Return', None)

                # Display results
                if not investment_allocation.empty:
                    st.subheader("Investment Allocation")
                    st.write(investment_allocation)
                
                if expected_return is not None:
                    st.write(f"**Expected Portfolio Return:** {expected_return:.2f}%", unsafe_allow_html=True)
                
                if expected_volatility is not None:
                    st.write(f"**Expected Portfolio Volatility:** {expected_volatility:.2f}%", unsafe_allow_html=True)
                
                if total_return is not None:
                    st.write(f"**Total Investment Return:** ₹{total_return:.2f}", unsafe_allow_html=True)
                
                break
    else:
        st.error("Failed to connect to the backend. Please check if the Flask server is running.")
