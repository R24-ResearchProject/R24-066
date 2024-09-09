import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the data
df = pd.read_csv('/Users/minu/Desktop/R24-066/Component 04/Dataset/worker_defect_production_data.csv')

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Drop rows with invalid dates
df.dropna(subset=['Date'], inplace=True)

# Set Date as index
df.set_index('Date', inplace=True)

# List of defect types
defect_types = ['Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low']

# Create a directory to save the forecasts if it doesn't exist
forecast_output_dir = '/Users/minu/Desktop/R24-066/Component 04/Dataset/each_worker_forecast_dataset'
model_output_dir = '/Users/minu/Desktop/R24-066/Component 04/Backend/each_worker_save_model'
os.makedirs(forecast_output_dir, exist_ok=True)
os.makedirs(model_output_dir, exist_ok=True)

def train_arima_model(data, order=(3, 0, 3), steps=5):
    try:
        model = ARIMA(data, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)
        logging.info(f"ARIMA model trained successfully with order {order}")
        return model_fit, forecast
    except Exception as e:
        logging.error(f"Error in training ARIMA model: {e}")
        return None, None

def calculate_rmse(observed, forecast):
    mse = mean_squared_error(observed, forecast)
    rmse = np.sqrt(mse)
    return rmse

def forecast_for_worker(worker_id, forecast_steps=5):
    worker_data = df[df['Worker_ID'] == worker_id]
    
    if worker_data.empty:
        logging.warning(f"No data found for worker {worker_id}.")
        return

    # Plotting time series for each defect type for the selected worker
    plt.figure(figsize=(14, 10))
    for i, defect_type in enumerate(defect_types, 1):
        plt.subplot(len(defect_types), 1, i)
        plt.plot(worker_data.index, worker_data[defect_type], marker='o', linestyle='-', color='red')
        plt.title(f'Previous data plot for {defect_type} (Worker {worker_id})')
        plt.xlabel('Date')
        plt.ylabel(f'{defect_type} Count')
        plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Calculate summary statistics for each defect type for the selected worker
    summary_stats = worker_data[defect_types].agg(['mean', 'sum']).transpose()

    # Determine high and low defect types for the selected worker
    high_defect_type = summary_stats['mean'].idxmax()
    low_defect_type = summary_stats['mean'].idxmin()

    logging.info(f"High defect type for worker {worker_id}: {high_defect_type}")
    logging.info(f"Low defect type for worker {worker_id}: {low_defect_type}")

    # Calculate last week's high and low defect counts for the selected worker
    last_week_data = worker_data.last('7D')
    if not last_week_data.empty:
        last_week_summary = last_week_data[defect_types].sum()
        last_week_high_defect_type = last_week_summary.idxmax()
        last_week_low_defect_type = last_week_summary.idxmin()
        last_week_high_defect_count = last_week_summary.max()
        last_week_low_defect_count = last_week_summary.min()

        logging.info(f"Worker {worker_id} - Last week's high defect type: {last_week_high_defect_type} with count: {last_week_high_defect_count}")
        logging.info(f"Worker {worker_id} - Last week's low defect type: {last_week_low_defect_type} with count: {last_week_low_defect_count}")
    else:
        logging.warning(f"No data available for the last week for worker {worker_id}")

    # Train ARIMA models and make forecasts for each defect type for the selected worker
    time_series_forecasts = pd.DataFrame(index=pd.date_range(start=worker_data.index[-1], periods=forecast_steps + 1, freq='B')[1:])
    
    for defect_type in defect_types:
        logging.info(f"Training ARIMA model for {defect_type} (Worker {worker_id})...")
        model_fit, forecast = train_arima_model(worker_data[defect_type], steps=forecast_steps)
        
        if model_fit is None:
            logging.warning(f"Skipping forecast for {defect_type} due to model training failure.")
            continue
        
        time_series_forecasts[defect_type] = forecast

        # Calculate RMSE
        if len(worker_data[defect_type]) >= forecast_steps:
            rmse = calculate_rmse(worker_data[defect_type][-forecast_steps:], forecast)
            logging.info(f"RMSE for {defect_type} (Worker {worker_id}): {rmse}")

        # Plotting the results
        plt.figure(figsize=(12, 6))
        plt.plot(worker_data.index, worker_data[defect_type], label='Observed', color='blue')
        future_dates = pd.date_range(start=worker_data.index[-1], periods=forecast_steps + 1, freq='B')[1:]
        plt.plot(future_dates, forecast, label='Forecast', linestyle='--', marker='o', color='purple')
        plt.title(f'Future forecast for {defect_type} (Worker {worker_id})')
        plt.xlabel('Date')
        plt.ylabel(f'{defect_type} Count')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Print model summary
        print(model_fit.summary())
    
    # Save time series forecasts for the current worker
    forecast_file = os.path.join(forecast_output_dir, f'time_series_forecasts_worker_{worker_id}.csv')
    time_series_forecasts.to_csv(forecast_file)

    # Save the ARIMA models for the current worker (optional)
    model_file = os.path.join(model_output_dir, f'arima_model_worker_{worker_id}.pkl')
    joblib.dump(model_fit, model_file)

# Prompt user to select a worker ID and forecast
worker_id = input("Enter the Worker ID: ")
forecast_for_worker(worker_id)
