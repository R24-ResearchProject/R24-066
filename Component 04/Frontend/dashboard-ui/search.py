import streamlit as st
import pandas as pd
from datetime import datetime

# Set up the page configuration
st.set_page_config(page_title="Seam Sense", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .big-font {
        font-size:16px !important;
        color: white;
    }
    .section-header {
        color: #FFFFFF;
        font-weight: bold;
        padding: 5px;
    }
    .card {
        background-color: #6C346C;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
        width: 100%;
        position: relative; /* Allow absolute positioning of child elements */
    }
    .card-text {
        color: white;
        font-size: 20px;
    }
    .user-icon-top {
        position: absolute;
        top: 10px; /* Adjust as needed */
        right: 10px; /* Adjust as needed */
        font-size: 20px;
    }
    .output-card, .shift-card {
        background-color: #1C1C1C;
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-size: 18px;
        font-weight: bold;
        position: relative;
        height: 140px;
    }
    .output-card:before {
        content: '\\1F4BC'; /* Clipboard icon */
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 20px;
        color: white;
    }
    .shift-card:before {
        content: '\\2600'; /* Sun icon */
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 20px;
        color: white;
    }
    .defect-box {
        background-color: #2c2c2c;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 5px;
        color: white;
        font-size: 14px;
        font-weight: bold;
        width: 100%;
    }
    .icon-text {
        display: inline-block;
        margin-right: 10px;
        color: white;
    }
    .icon {
        margin-left: 5px;
        font-size: 16px;
    }
    .stButton>button {
        width: 200px;
        height: 45px;
        font-size: 18px;
        background-color: #6C346C; /* Purple button */
        color: white;
        border: none;
        border-radius: 5px;
        margin: auto;
        display: block;
    }
    .search-bar {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
        border: 2px solid #1C1C1C;
        margin-bottom: 20px;
    }
    .center-image {
        display: block;
        margin: 20px auto;
        max-width: 100%; /* Ensure the image scales properly */
    }
    .footer {
        font-size: 12px;
        color: #999;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>Seam Sense</h1>", unsafe_allow_html=True)

# Add space before the search bar
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Load your dataset (Replace 'your_dataset.csv' with your actual dataset file)
df = pd.read_csv('/Users/minu/Desktop/R24-066/Component 04/Dataset/demographic_data_dataset.csv')  # Ensure your CSV file has a column named 'Worker_ID'

# Search Worker ID with Bold and Increased Font Size
st.markdown("<p style='font-size: 20px; font-weight: bold; color: #FFFFFF; margin-bottom: 5px;'>Search Worker ID:</p>", unsafe_allow_html=True)
worker_id_input = st.text_input("", placeholder="Enter Worker ID (e.g., W_xxxxx)...", key="worker_id_input", label_visibility='collapsed')

# Check if the Worker ID is in the correct format
if worker_id_input and not worker_id_input.startswith("W_"):
    st.error("Worker ID should start with 'W_' followed by numbers (e.g., W_xxxxx).")
elif worker_id_input:
    # Search the dataset for the Worker ID
    result = df[df['Worker_ID'] == worker_id_input]
    if not result.empty:
        st.success(f"Worker ID {worker_id_input} found!")
        # Display the relevant data
        # st.write(result)
        
        # Add a button to go to the dashboard
        if st.button("Go to Dashboard"):
            st.session_state['page'] = 'dashboard'
    else:
        st.error(f"Worker ID {worker_id_input} not found in the dataset.")

# Redirect to the dashboard if the button is clicked
if 'page' in st.session_state and st.session_state['page'] == 'dashboard':
    st.write("Redirecting to the Dashboard...")  # Placeholder for actual dashboard redirection logic
    # Add your dashboard redirection code here

# Footer
st.markdown("<div class='footer'>Developed by SeamSense</div>", unsafe_allow_html=True)