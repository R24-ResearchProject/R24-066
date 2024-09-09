import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np
from datetime import datetime
import joblib
import os

# Set up page configuration
st.set_page_config(page_title="Seam Sense Dashboard", layout="wide")

# Custom CSS for styling with color adjustments for both light and dark themes
st.markdown(
    """
    <style>
    body {
        background-color: #20232a; /* Dark background for the page */
    }
    .main-title {
        font-size: 40px;
        color: #6C346C;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 24px;
        color: #f7f7f7;
        margin-top: 30px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .worker-card {
        background-color: #6C346C;
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        position: relative;
    }
    .worker-info {
        font-size: 20px;
        font-weight: bold;
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
    .defect-table {
        font-size: 18px;
        color: #333;
        background-color: #f7f7f7;
        padding: 10px;
        border-radius: 10px;
        width: 60%;
        margin: 0 auto;
    }
    .defect-count-card {
        background-color: #2c2c2c;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin: 5px;
        color: white;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
        width: 100px;
    }
    .info-card {
        background-color: #1C1C1C;
        padding: 15px;
        border-radius: 10px;
        color: white;
        font-size: 18px;
        font-weight: bold;
        text-align: left;
        margin: 5px;
        position: relative;
    }
    .info-card-header {
        font-size: 16px;
        color: #999;
        margin-bottom: 5px;
    }
    .defect-count-box {
        background-color: #2c2c2c;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin: 5px;
        color: white;
        font-size: 14px;
        font-weight: bold;
        width: 100px;
        display: inline-block;
    }
    .icon {
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 20px;
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
    .summary-box {
        background-color: #2c2c2c;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: left;
        font-size: 19px;
        color: #333;
        font-weight: bold
    }
    .footer {
        text-align: center;
        font-size: 12px;
        color: #999;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'worker_id' not in st.session_state:
    st.session_state['worker_id'] = None

# Directory setup
forecast_output_dir = '/Users/minu/Desktop/R24-066/Component 04/Dataset/each_worker_forecast_dataset'
model_output_dir = '/Users/minu/Desktop/R24-066/Component 04/Backend/each_worker_save_model'
os.makedirs(forecast_output_dir, exist_ok=True)
os.makedirs(model_output_dir, exist_ok=True)

# Helper function for navigation
def go_to_dashboard(worker_id):
    st.session_state['worker_id'] = worker_id
    st.session_state['page'] = 'dashboard'
    st.experimental_rerun()

# Forecasting functions
def train_arima_model(data, order=(3, 0, 3), steps=5):
    try:
        model = ARIMA(data, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)
        return model_fit, forecast
    except Exception as e:
        st.error(f"Error in training ARIMA model: {e}")
        return None, None

def calculate_rmse(observed, forecast):
    mse = mean_squared_error(observed, forecast)
    rmse = np.sqrt(mse)
    return rmse

# Load datasets
df_defects = pd.read_csv('/Users/minu/Desktop/R24-066/Component 04/Dataset/worker_defect_production_data.csv')
df_demographics = pd.read_csv('/Users/minu/Desktop/R24-066/Component 04/Dataset/demographic_data_dataset.csv')

# Merge the datasets
df_merged = pd.merge(df_defects, df_demographics, on='Worker_ID', how='left')

df_merged['Date'] = pd.to_datetime(df_merged['Date'], errors='coerce')
df_merged.dropna(subset=['Date'], inplace=True)
df_merged.set_index('Date', inplace=True)
defect_types = ['Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low']

# Main page
if st.session_state['page'] == 'home':

    # Header Section with Title and Subtitle
    st.markdown("<div class='main-title'>Seam Sense</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Real-Time Seam Defect Detection and Analysis</div>", unsafe_allow_html=True)

    # Display the Image in the Center
    st.image('https://masholdings.com/wp-content/uploads/2022/06/024.jpg', use_column_width=True, caption='')

    # Centered Button for Navigation
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    if st.button("Go to Dashboard"):
        st.session_state['page'] = 'search_worker'

    # Footer
    st.markdown("<div class='footer'>Developed by SeamSense</div>", unsafe_allow_html=True)

# Search Worker page
elif st.session_state['page'] == 'search_worker':
    st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>Search Worker</h1>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>Search Worker ID:</p>", unsafe_allow_html=True)
    
    # Search bar for worker ID
    worker_id_input = st.text_input("", placeholder="Enter Worker ID (e.g., W_xxxxx)...", key="worker_id_input", label_visibility='collapsed')

    # Validate Worker ID
    if worker_id_input and not worker_id_input.startswith("W_"):
        st.error("Worker ID should start with 'W_' followed by numbers (e.g., W_xxxxx).")
    elif worker_id_input:
        # Check if worker exists
        result = df_merged[df_merged['Worker_ID'] == worker_id_input]
        if not result.empty:
            st.success(f"Worker ID {worker_id_input} found!")

            # Button to go to Dashboard
            if st.button("Go to Dashboard", key='go_dashboard'):
                go_to_dashboard(worker_id_input)
        else:
            st.error(f"Worker ID {worker_id_input} not found in the dataset.")
    st.markdown("<div class='footer'>Developed by SeamSense</div>", unsafe_allow_html=True)

# Dashboard page
if st.session_state['page'] == 'dashboard':
    # Header Section
    st.markdown("<h1 style='text-align: center; color: #FFFFFF; style='text-align: left;'>Dashboard</h1>", unsafe_allow_html=True)
    # st.markdown(f"<p style='text-align: center; color: #FFFFFF; style='text-align: left;'>{datetime.now().strftime('%d %B %Y')} • {datetime.now().strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

    # Display header with date and time icons
    current_date = datetime.now().strftime('%d %B %Y')
    current_time = datetime.now().strftime('%I:%M %p')

    #&#x23F0;&#x1F4D8;
    st.markdown(
        f"""
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span class='icon-text'> {current_date}</span>  <!-- Notebook icon -->
            <span class='icon-text'> {current_time}</span>  <!-- Clock icon -->
        </div>
        """, 
        unsafe_allow_html=True
    )

    worker_id_input = st.session_state['worker_id']
    st.markdown(f"<h2 class='section-title'>Dashboard for Worker ID: {worker_id_input}</h2>", unsafe_allow_html=True)

    # Filter data for specific worker
    worker_data = df_merged[df_merged['Worker_ID'] == worker_id_input]

    if worker_data.empty:
        st.error(f"No data found for Worker ID: {worker_id_input}")
    else:
        # Display worker details
        worker_name = worker_data['Name'].iloc[0]
        skill_level = worker_data['Skill_Level'].iloc[0]
        shift = worker_data['Shift'].iloc[0]
        cumulative_output = worker_data['Production_Volume'].iloc[0]  # Example column for production volume
        
        st.markdown(
            f"""
            <div class='worker-card'>
                <h2 class='card-text' style='text-align: left; font-size: 15px; color:white;'><span class='user-icon-top'>&#x1F464;</span> <!-- User icon -->Worker Information</h2>
                <p class='worker-info'>Worker Name: {worker_name}</p>
                <p class='worker-info'>Skill Level: {skill_level}</p>
                <p class='worker-info' style='text-align: right;'>Worker ID: {worker_id_input}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Display Cumulative Output and Shift Information
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            st.markdown(
                """
                <div class='info-card' style='border: 2px solid #333; border-radius: 10px; background-color: #2C2C2C; color: white; padding: 20px; height: 140px; position: relative;'>
                    <div class='info-card-header' style='font-size: 15px; font-weight: bold; color: #FFFFFF;'>Cumulative Output</div>
                    <div style='margin-top: 10px; font-size: 18px; font-weight: bold;'>Target: 600 pcs</div>
                    <span style='position: absolute; top: 10px; right: 10px; font-size: 20px; color: white;'>&#x1F4BC;</span> <!-- Briefcase Icon -->
                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:
            shift_info = worker_data['Shift'].iloc[0] if not worker_data.empty else "N/A"
            st.markdown(
                f"""
                <div class='info-card' style='border: 2px solid #333; border-radius: 10px; background-color: #2C2C2C; color: white; padding: 20px; height: 140px; position: relative;'>
                    <div class='info-card-header' style='font-size: 15px; font-weight: bold; color: #FFFFFF;'>Shift</div>
                    <div style='margin-top: 10px; font-size: 15px; font-weight: bold;'>{shift_info}<br>9am - 5pm</div>
                    <span style='position: absolute; top: 10px; right: 10px; font-size: 20px; color: yellow;'>&#x2600;</span> <!-- Sun Icon -->
                </div>
                """, 
                unsafe_allow_html=True
            )
            
        # Calculate defect counts dynamically for the selected worker
        defect_counts = worker_data[defect_types].sum()

        # Display Defect Counts in a 2x2 Grid Format
        with col3:
            st.markdown("<p class='section-header' style='color: #FFFFFF; font-weight: bold;'>Defect Count</p>", unsafe_allow_html=True)

            # 2x2 Grid for Defect Counts
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown(
                    f"<div class='defect-box' style='background-color: #2c2c2c; padding: 10px; margin-bottom: 10px; border-radius: 5px; text-align: center; color: white; font-size: 14px; font-weight: bold;'>High Low : {defect_counts['High_Low']}</div>", 
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div class='defect-box' style='background-color: #2c2c2c; padding: 10px; margin-bottom: 10px; border-radius: 5px; text-align: center; color: white; font-size: 14px; font-weight: bold;'>Run Off : {defect_counts['Run_Off']}</div>", 
                    unsafe_allow_html=True
                )
                
            with col_b:
                st.markdown(
                    f"<div class='defect-box' style='background-color: #2c2c2c; padding: 10px; margin-bottom: 10px; border-radius: 5px; text-align: center; color: white; font-size: 14px; font-weight: bold;'>SPI Error : {defect_counts['SPI_Errors']}</div>", 
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div class='defect-box' style='background-color: #2c2c2c; padding: 10px; margin-bottom: 10px; border-radius: 5px; text-align: center; color: white; font-size: 14px; font-weight: bold;'>Open Seam : {defect_counts['Open_Seam']}</div>", 
                    unsafe_allow_html=True
                )

        # Summary Statistics Section
        st.markdown("<div class='section-title'>Summary Statistics</div>", unsafe_allow_html=True)

        # Calculate high and low defect types
        summary_stats = worker_data[defect_types].agg(['mean', 'sum']).transpose()
        high_defect_type = summary_stats['mean'].idxmax()
        low_defect_type = summary_stats['mean'].idxmin()

        # Display High and Low Defect Types
        st.markdown(
            f"""
            <div class='summary-box'>
                <p style='font-size: 17px; color: white;'>High defect type for worker {worker_id_input}: <strong>{high_defect_type}</strong></p>
                <p style='font-size: 17px; color: white;'>Low defect type for worker {worker_id_input}: <strong>{low_defect_type}</strong></p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Calculate last week's high and low defect counts
        last_week_data = worker_data.last('7D')
        if not last_week_data.empty:
            last_week_summary = last_week_data[defect_types].sum()
            last_week_high_defect_type = last_week_summary.idxmax()
            last_week_low_defect_type = last_week_summary.idxmin()
            
            # Display Last Week's Defect Statistics
            st.markdown(
                f"""
                <div class='summary-box'>
                    <p style='font-size: 17px; color: white;'>Last week's high defect type: <strong>{last_week_high_defect_type}</strong> with count: <strong>{last_week_summary.max()}</strong></p>
                    <p style='font-size: 17px; color: white;'>Last week's low defect type: <strong>{last_week_low_defect_type}</strong> with count: <strong>{last_week_summary.min()}</strong></p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.warning("No data available for the last week.")

        # Display previous data plots in a 2x2 grid
        st.markdown("<div class='section-title'>Previous Data Plots</div>", unsafe_allow_html=True)
        with st.container():
            col1, col2 = st.columns(2)
            for idx, defect_type in enumerate(defect_types):
                if idx % 2 == 0:
                    with col1:
                        st.write(f"Previous data for {defect_type}:")
                        plt.figure(figsize=(8, 4))
                        plt.plot(worker_data.index, worker_data[defect_type], marker='o', linestyle='-', color='red')
                        plt.title(f'Previous data plot for {defect_type} (Worker {worker_id_input})')
                        plt.xlabel('Date')
                        plt.ylabel(f'{defect_type} Count')
                        plt.grid(True)
                        st.pyplot(plt)
                else:
                    with col2:
                        st.write(f"Previous data for {defect_type}:")
                        plt.figure(figsize=(8, 4))
                        plt.plot(worker_data.index, worker_data[defect_type], marker='o', linestyle='-', color='red')
                        plt.title(f'Previous data plot for {defect_type} (Worker {worker_id_input})')
                        plt.xlabel('Date')
                        plt.ylabel(f'{defect_type} Count')
                        plt.grid(True)
                        st.pyplot(plt)

        # Display forecasting results in a 2x2 grid
        st.markdown("<div class='section-title'>Forecasting Results</div>", unsafe_allow_html=True)
        with st.container():
            col1, col2 = st.columns(2)
            for idx, defect_type in enumerate(defect_types):
                if idx % 2 == 0:
                    with col1:
                        st.write(f"Forecasting for {defect_type}:")
                        model_fit, forecast = train_arima_model(worker_data[defect_type].dropna())
                        if model_fit:
                            plt.figure(figsize=(8, 4))
                            plt.plot(worker_data.index, worker_data[defect_type], label='Observed', color='blue')
                            future_dates = pd.date_range(start=worker_data.index[-1], periods=len(forecast) + 1, freq='B')[1:]
                            plt.plot(future_dates, forecast, label='Forecast', linestyle='--', marker='o', color='purple')
                            plt.title(f'Future forecast for {defect_type} (Worker {worker_id_input})')
                            plt.xlabel('Date')
                            plt.ylabel(f'{defect_type} Count')
                            plt.legend()
                            plt.grid(True)
                            st.pyplot(plt)
                else:
                    with col2:
                        st.write(f"Forecasting for {defect_type}:")
                        model_fit, forecast = train_arima_model(worker_data[defect_type].dropna())
                        if model_fit:
                            plt.figure(figsize=(8, 4))
                            plt.plot(worker_data.index, worker_data[defect_type], label='Observed', color='blue')
                            future_dates = pd.date_range(start=worker_data.index[-1], periods=len(forecast) + 1, freq='B')[1:]
                            plt.plot(future_dates, forecast, label='Forecast', linestyle='--', marker='o', color='purple')
                            plt.title(f'Future forecast for {defect_type} (Worker {worker_id_input})')
                            plt.xlabel('Date')
                            plt.ylabel(f'{defect_type} Count')
                            plt.legend()
                            plt.grid(True)
                            st.pyplot(plt)


# Footer
    st.markdown("<div class='footer'>Developed by SeamSense</div>", unsafe_allow_html=True)
