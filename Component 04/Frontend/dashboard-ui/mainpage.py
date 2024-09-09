import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Set up the page configuration
st.set_page_config(page_title="Seam Sense", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #20232a; /* Dark background for the page */
    }
    .main-title {
        font-size: 48px;
        color: #FFFFFF;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 20px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 30px;
    }
    .center-image {
        display: block;
        margin: 30px auto;
        max-width: 100%;
        border-radius: 10px; /* Rounded corners for the image */
    }
    .button-container {
        text-align: center;
        margin-top: 20px;
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

# Header Section with Title and Subtitle
st.markdown("<div class='main-title'>Seam Sense</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Real-Time Seam Defect Detection and Analysis</div>", unsafe_allow_html=True)

# Display the Image in the Center
st.image('https://masholdings.com/wp-content/uploads/2022/06/024.jpg', use_column_width=True, caption='')

# Centered Button for Navigation
st.markdown("<div class='button-container'>", unsafe_allow_html=True)
if st.button("Go to Dashboard"):
    st.session_state['page'] = 'dashboard'

# Footer
st.markdown("<div class='footer'>Developed by SeamSense</div>", unsafe_allow_html=True)

# Redirect logic
if 'page' in st.session_state and st.session_state['page'] == 'dashboard':
    st.experimental_rerun()
