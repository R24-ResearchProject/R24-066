import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
import os
from flask import Flask, request, render_template

app = Flask(__name__)

# Load the data
defect_data_path = '/Users/minu/Desktop/R24-066/Component 04/Backend/Dataset/updated_worker_defect_details.csv'
demographic_data_path = '/Users/minu/Desktop/R24-066/Component 04/Backend/Dataset/demographic_data_dataset.csv'

defect_data = pd.read_csv(defect_data_path)
demographic_data = pd.read_csv(demographic_data_path)
defect_data['Date'] = pd.to_datetime(defect_data['Date'], errors='coerce')
demographic_data['Joining_Date'] = pd.to_datetime(demographic_data['Joining_Date'], errors='coerce')

# Combine datasets on Worker_ID
combined_data = pd.merge(defect_data, demographic_data, on='Worker_ID')

# List of defect types
defect_types = ['Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low']

# Create a directory to save the forecasts if it doesn't exist
forecast_output_dir = '/Users/minu/Desktop/R24-066/Component 04/Backend/Dataset/worker_forecasts_dataset'
model_output_dir = '/Users/minu/Desktop/R24-066/Component 04/Backend/Save_model'
os.makedirs(forecast_output_dir, exist_ok=True)
os.makedirs(model_output_dir, exist_ok=True)

def train_arima_model(data, order=(1, 1, 1), steps=5):
    model = ARIMA(data, order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return model_fit, forecast

def calculate_rmse(observed, forecast):
    mse = mean_squared_error(observed, forecast)
    rmse = np.sqrt(mse)
    return rmse

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        worker_id = request.form['worker_id']
        return forecast(worker_id)
    return render_template('index1.html')

def forecast(worker_id, forecast_steps=5):
    worker_data = combined_data[combined_data['Worker_ID'] == worker_id]
    
    if worker_data.empty:
        return render_template('index1.html', error=f"No data found for worker {worker_id}")

    # Calculate summary statistics for each defect type for the selected worker
    summary_stats = worker_data[defect_types].agg(['mean', 'sum']).transpose()

    # Determine high and low defect types for the selected worker
    high_defect_type = summary_stats['mean'].idxmax()
    low_defect_type = summary_stats['mean'].idxmin()

    # Calculate last week's high and low defect counts for the selected worker
    worker_data.set_index('Date', inplace=True)
    last_week_data = worker_data.last('7D')
    last_week_summary = last_week_data[defect_types].sum()
    last_week_high_defect_type = last_week_summary.idxmax()
    last_week_low_defect_type = last_week_summary.idxmin()
    last_week_high_defect_count = last_week_summary.max()
    last_week_low_defect_count = last_week_summary.min()

    # Train ARIMA models and make forecasts for each defect type for the selected worker
    time_series_forecasts = pd.DataFrame(index=pd.date_range(start=worker_data.index[-1], periods=forecast_steps + 1, freq='B')[1:])
    plots = []
    for defect_type in defect_types:
        model_fit, forecast = train_arima_model(worker_data[defect_type], steps=forecast_steps)
        time_series_forecasts[defect_type] = forecast

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

        plot_filename = f'static/{worker_id}_{defect_type}.png'
        plt.savefig(plot_filename)
        plt.close()
        plots.append(plot_filename)

    return render_template('index1.html', worker_name=worker_id, highest_defect_type=high_defect_type,
                           lowest_defect_type=low_defect_type,
                           last_week_high_defect_type=last_week_high_defect_type, last_week_high_defect_count=last_week_high_defect_count,
                           last_week_low_defect_type=last_week_low_defect_type, last_week_low_defect_count=last_week_low_defect_count,
                           plots=plots)

if __name__ == '__main__':
    app.run(debug=True, port=5006)
