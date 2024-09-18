import streamlit as st
import requests
from PIL import Image

# Set page configuration
st.set_page_config(page_title="NivrritiMarg - AI Engine", layout="wide")

# Add custom CSS for styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inria+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap');

    .main {
        background-color: #fff4e6; /* Light beige background */
        color: #3c2f2f; /* Dark muted color for text */
        font-family: 'Inria Sans', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #be9b7b; /* Light tan for sidebar */
        color: #3c2f2f; /* Dark muted color for sidebar text */
        font-family: 'Inria Sans', sans-serif;
    }
    .stButton>button {
        border-radius: 12px;
        background-color: #854442; /* Muted brown for button */
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 10px 20px;
        transition: background-color 0.3s, transform 0.3s;
        font-family: 'Inria Sans', sans-serif;
    }
    .stButton>button:hover {
        background-color: #4b3832; /* Darker brown for button hover */
        transform: scale(1.05);
    }
    h1 {
        color: #3c2f2f; /* Dark muted color for title */
        font-family: 'Inria Sans', sans-serif;
    }
    .card {
        border-radius: 10px;
        background: #be9b7b; /* Light tan background for card */
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
        color: #3c2f2f; /* Dark muted color for card title */
    }
    .card-content {
        font-size: 16px;
        color: #3c2f2f; /* Dark muted color for card content */
    }
    footer {
        text-align: center;
        padding: 10px;
        background-color: #4b3832; /* Dark brown for footer */
        color: #fff4e6; /* Light beige for footer text */
        font-family: 'Inria Sans', sans-serif;
        border: none; /* No border around the footer */
    }
    .sidebar .sidebar-content .stNumberInput, .sidebar .sidebar-content .stSelectbox {
        background-color: #fff4e6; /* Light beige background for inputs */
        color: #3c2f2f; /* Dark muted color for input text */
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #854442; /* Muted brown border */
    }
    .sidebar .sidebar-content .stNumberInput input, .sidebar .sidebar-content .stSelectbox select {
        background-color: #ffffff; /* White background for input fields */
        color: #3c2f2f; /* Dark muted color for input text */
        border: 1px solid #854442; /* Muted brown border */
        border-radius: 8px;
        padding: 8px;
    }
    .sidebar .sidebar-content .stNumberInput input:hover, .sidebar .sidebar-content .stSelectbox select:hover {
        border-color: #4b3832; /* Darker brown border on hover */
    }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.title('🎯 NivrritiMarg - AI Engine for Retirement Investment Allocation 🌟')
st.write("Welcome to NivrritiMarg! Plan your retirement with our AI-powered investment optimizer. 🚀")

# Add a sample image (optional, comment out if not available)
# image_path = 'path_to_your_image.png'  # Update with the correct path
# try:
#     image = Image.open(image_path)
#     st.image(image, caption='Your Investment Journey Starts Here!', use_column_width=True)
# except FileNotFoundError:
#     st.warning("Image file not found. Please check the path or remove the image.")

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

    try:
        response = requests.post('http://127.0.0.1:5000/investment-strategy', json=payload)
        data = response.json()
        
        # Display Investment Recommendations
        st.write("### Investment Recommendations:")
        if 'allocations' in data:
            for stock, percentage in data['allocations']:
                st.write(f"📊 **{stock}**: {percentage:.2f}%")
            st.write(f"💸 **Total Future Value**: ₹{data['total_future_value']:.2f}")
            st.write(f"📉 **Average Annual Return**: {data['average_annual_return_percentage']:.2f}%")
            st.write(f"💰 **Total Invested**: ₹{data['total_invested']:.2f}")
            
            # Display Risk Estimate
            st.write("### ⚠️ Risk Estimate:")
            st.markdown(f"<div class='card'><div class='card-title'>🔮 **Mean Future Value**</div><div class='card-content'>₹{data['risk_estimate']['mean']:.2f}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'><div class='card-title'>📈 **Standard Deviation**</div><div class='card-content'>₹{data['risk_estimate']['std_dev']:.2f}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'><div class='card-title'>🔒 **95% Confidence Interval**</div><div class='card-content'>₹{data['risk_estimate']['confidence_interval'][0]:.2f} to ₹{data['risk_estimate']['confidence_interval'][1]:.2f}</div></div>", unsafe_allow_html=True)
        else:
            st.write(data)
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Request failed: {e}")

# Add footer
st.markdown("""
    <footer>
        <p>Powered by NivrritiMarg 🌟 | Your Path to a Secure Retirement 🚀</p>
    </footer>
""", unsafe_allow_html=True)
