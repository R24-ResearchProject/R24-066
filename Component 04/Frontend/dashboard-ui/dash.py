import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
import os

# Set up page configuration
st.set_page_config(page_title="Seam Sense Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        color: #6C346C;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 24px;
        color: #1C1C1C;
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
    .defect-table {
        font-size: 18px;
        color: #333;
        background-color: #f7f7f7;
        padding: 10px;
        border-radius: 10px;
        width: 60%;
        margin: 0 auto;
    }
    .summary-box {
        background-color: #EFEFEF;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 18px;
        color: #333;
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

# Home page
if st.session_state['page'] == 'home':
    st.markdown("<div class='main-title'>Seam Sense Dashboard</div>", unsafe_allow_html=True)
    st.write("---")
    
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
            if st.button("Go to Dashboard"):
                go_to_dashboard(worker_id_input)
        else:
            st.error(f"Worker ID {worker_id_input} not found in the dataset.")
    st.markdown("<div class='footer'>Developed by SeamSense</div>", unsafe_allow_html=True)

# Dashboard page
if st.session_state['page'] == 'dashboard':
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
        st.markdown(
            f"""
            <div class='worker-card'>
                <h2 class='card-text' style='text-align: left; font-size: 15px; color:white;'><span class='user-icon-top'>&#x1F464;</span> <!-- User icon -->Worker Information</h2>
                <p class='worker-info'>Worker Name: {worker_name}</p>
                <p class='worker-info'>Skill Level: {skill_level}</p>
                <p class='worker-info' >Worker ID: {worker_id_input}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Display a small table for defect type counts
        st.markdown("<div class='section-title'>Defect Type Counts</div>", unsafe_allow_html=True)
        defect_counts = worker_data[defect_types].sum().reset_index()
        defect_counts.columns = ['Defect Type', 'Total Count']
        st.table(defect_counts.style.set_properties(**{'text-align': 'center'}).set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}]))

        # Display previous data plots
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
        
        # Summary statistics
        st.markdown("<div class='section-title'>Summary Statistics</div>", unsafe_allow_html=True)
        summary_stats = worker_data[defect_types].agg(['mean', 'sum']).transpose()
        high_defect_type = summary_stats['mean'].idxmax()
        low_defect_type = summary_stats['mean'].idxmin()

        st.write(f"High defect type for worker {worker_id_input}: **{high_defect_type}**")
        st.write(f"Low defect type for worker {worker_id_input}: **{low_defect_type}**")

        # Last week's high and low defect counts
        last_week_data = worker_data.last('7D')
        if not last_week_data.empty:
            last_week_summary = last_week_data[defect_types].sum()
            last_week_high_defect_type = last_week_summary.idxmax()
            last_week_low_defect_type = last_week_summary.idxmin()
            st.write(f"Last week's high defect type: **{last_week_high_defect_type}** with count: **{last_week_summary.max()}**")
            st.write(f"Last week's low defect type: **{last_week_low_defect_type}** with count: **{last_week_summary.min()}**")
        else:
            st.warning("No data available for the last week.")

        # Forecasting results
        st.markdown("<div class='section-title'>Forecasting Results</div>", unsafe_allow_html=True)
        for defect_type in defect_types:
            st.write(f"Forecasting for {defect_type}:")
            model_fit, forecast = train_arima_model(worker_data[defect_type].dropna())
            
            if model_fit:
                plt.figure(figsize=(10, 5))
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
                st.warning(f"Could not generate forecast for {defect_type}.")

# Footer
# st.markdown("<div class='footer'>Developed by SeamSense</div>", unsafe_allow_html=True)
