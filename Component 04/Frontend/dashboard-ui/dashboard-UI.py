import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time

# Set up the page configuration
st.set_page_config(page_title="Seam Sense", layout="wide")

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
    }
    .card-text {
        color: white;
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
    }
    .output-card:before {
        content: '\\1F4BC'; /* Clipboard icon */
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 10px;
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
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
st.markdown("<h1 style='text-align: center; color: #FFFFFF; style='text-align: left;'>Seam Sense</h1>", unsafe_allow_html=True)
# st.markdown(f"<p style='text-align: center; color: #FFFFFF; style='text-align: left;'>{datetime.now().strftime('%d %B %Y')} • {datetime.now().strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

# Display header with date and time icons
current_date = datetime.now().strftime('%d %B %Y')
current_time = datetime.now().strftime('%I:%M %p')

st.markdown(
    f"""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <span class='icon-text'>&#x1F4D8; {current_date}</span>  <!-- Notebook icon -->
        <span class='icon-text'>&#x23F0; {current_time}</span>  <!-- Clock icon -->
    </div>
    """, 
    unsafe_allow_html=True
)

# Add some vertical space before the Worker Information section
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Adds space above Worker Information

# Worker Information Section
st.markdown(
    """
    <div class='card' style='text-align: left; margin: auto; margin-bottom: 20px; padding: 15px; background-color: #522258; border-radius: 10px;'>
        <h2 class='card-text' style='text-align: left; font-size: 15px; color:white;'><span class='user-icon-top'>&#x1F464;</span> <!-- User icon -->Worker Information</h2>
        <p class='card-text' style='text-align: left; font-size: 25px; font-weight:bold; color:white;'>Minuli Samaraweera</p>
        <p class='card-text' style='text-align: left; font-size: 25px; font-weight:bold; color:white;'>Level 5</p>
        <p class='card-text' style='text-align: right; font-size: 25px; font-weight:bold; color:white;'>Worker ID : IT21016066</p>
    </div>
    """, unsafe_allow_html=True
)

# Layout for Output, Shift, and Defect Count with Cards
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown(
        """
        <div class='output-card' style='border: 2px; border-radius: 10px; background-color: #1C1C1Cs; color: white; padding: 20px; height: 140px; position: relative;'>
            <p style='font-size: 15px; margin: 0; color: #FFFFFF; font-weight: bold;'>Cumulative output</p>
            <p class='card-text' style='margin: 5px 0; font-weight: bold;'>Target : 600 pcs</p>
            <div style='position: absolute; top: 10px; right: 10px;'>
                <i class="fas fa-clipboard"></i> <!-- Clipboard icon -->
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class='shift-card' style='border: 2px; border-radius: 10px; background-color: #1C1C1C; color: white; padding: 20px; height: 140px; position: relative;'>
            <p style='font-size: 15px; margin: 0; color: #FFFFFF; font-weight: bold;'>Shift</p>
            <p class='card-text' style='margin: 5px 0; font-weight: bold;'>Morning</p>
            <p style='font-size: 15px; margin: 0;color: #FFFFFF; font-weight: bold;'>9am - 5pm</p>
            <div style='position: absolute; top: 10px; right: 10px;'>
                <i class="fas fa-sun"></i> <!-- Sun icon -->
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown("<p class='section-header' style='color: #FFFFFF; font-weight: bold;'>Defect Count   <span class='icon'>&#x25A3;</span> <!-- Grid icon --> </p>", unsafe_allow_html=True)
    # 2x2 Grid for Defect Counts
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='defect-box' style='background-color: #2c2c2c; padding: 10px; border-radius: 5px; text-align: center; color: white; font-size: 14px; font-weight: bold;'>High Low : 1</div>", unsafe_allow_html=True)
        st.markdown("<div class='defect-box' style='background-color: #2c2c2c; padding: 10px; border-radius: 5px; text-align: center; color: white; font-size: 14px; font-weight: bold;'>Run Off : 3</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='defect-box' style='background-color: #2c2c2c; padding: 10px; border-radius: 5px; text-align: center; color: white; font-size: 14px; font-weight: bold;'>SPI Error : 5</div>", unsafe_allow_html=True)
        st.markdown("<div class='defect-box' style='background-color: #2c2c2c; padding: 10px; border-radius: 5px; text-align: center; color: white; font-size: 14px; font-weight: bold;'>Open Seam : 4</div>", unsafe_allow_html=True)

# Forecasting Graphs Section
st.markdown(
    """
    <div style='display: flex; align-items: center;'>
        <h3 style='color: #FFFFFF;'>Forecasting Graph</h3> 
       <span class='icon'>&#x2191; &#x2193;</span> <!-- Up and Down arrows -->
    </div>
    """, 
    unsafe_allow_html=True
)


# Placeholder data for graphs
data = {
    'Date': pd.date_range(start='1/1/2024', periods=10),
    'High Low': np.random.randint(0, 100, 10),
    'Run Off': np.random.randint(0, 100, 10),
    'SPI Error': np.random.randint(0, 100, 10),
    'Open Seam': np.random.randint(0, 100, 10)
}
df = pd.DataFrame(data)

# Create Forecasting Graphs
col4, col5, col6, col7 = st.columns(4)

with col4:
    st.markdown("<p class='section-header'>High Low</p>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.fill_between(df['Date'], df['High Low'], color="skyblue", alpha=0.4)
    ax.plot(df['Date'], df['High Low'], color="Slateblue", alpha=0.6, linewidth=2)
    st.pyplot(fig)

with col5:
    st.markdown("<p class='section-header'>Run Off</p>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.fill_between(df['Date'], df['Run Off'], color="green", alpha=0.4)
    ax.plot(df['Date'], df['Run Off'], color="darkgreen", alpha=0.6, linewidth=2)
    st.pyplot(fig)

with col6:
    st.markdown("<p class='section-header'>SPI Error</p>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.plot(df['Date'], df['SPI Error'], marker='o', linestyle='-', color="red")
    st.pyplot(fig)

with col7:
    st.markdown("<p class='section-header'>Open Seam</p>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.bar(df['Date'].dt.strftime('%d-%m'), df['Open Seam'], color="orange")
    st.pyplot(fig)
