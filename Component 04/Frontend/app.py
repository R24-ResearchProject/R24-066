import pandas as pd
import numpy as np
from flask import Flask, request, render_template
import os
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

# Use 'Agg' backend for Matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# Customized file paths
defect_data_path = '/Users/minu/Desktop/R24-066/Component 04/Backend/Dataset/updated_worker_defect_details.csv'
demographic_data_path = '/Users/minu/Desktop/R24-066/Component 04/Backend/Dataset/demographic_data_dataset.csv'
time_series_forecasts_path = '/Users/minu/Desktop/R24-066/Component 04/Backend/Dataset/worker_forecasts_dataset/time_series_forecasts.csv'
traditional_model_path = '/Users/minu/Desktop/R24-066/Component 04/Backend/Save_model/best_traditional_model.pkl'

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    worker_name = None
    defect_counts = {}
    highest_defect_type = None
    lowest_defect_type = None
    last_week_highest_defect_type = None
    last_week_lowest_defect_type = None
    last_week_defect_counts = {}
    plots = []

    try:
        # Load data
        print("Loading defect data...")
        defect_data = pd.read_csv(defect_data_path)
        print("Defect data loaded.")

        print("Loading demographic data...")
        demographic_data = pd.read_csv(demographic_data_path)
        print("Demographic data loaded.")

        print("Loading time series forecasts...")
        time_series_forecasts = pd.read_csv(time_series_forecasts_path, index_col=0)
        print("Time series forecasts loaded.")

        # Convert Date columns to datetime
        defect_data['Date'] = pd.to_datetime(defect_data['Date'])
        demographic_data['Joining_Date'] = pd.to_datetime(demographic_data['Joining_Date'])

        # Combine datasets on Worker_ID
        print("Merging data...")
        combined_data = pd.merge(defect_data, demographic_data, on='Worker_ID')
        print("Data merged.")

        if request.method == 'POST':
            worker_id = request.form['worker_id']
            print(f"Received worker_id: {worker_id}")

            worker_data = combined_data[combined_data['Worker_ID'] == worker_id]

            if worker_data.empty:
                error = 'Worker ID not found.'
                return render_template('index.html', error=error)

            worker_name = worker_data['Name'].iloc[0]
            defect_counts = worker_data[['Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low']].sum().to_dict()
            highest_defect_type = max(defect_counts, key=defect_counts.get)
            lowest_defect_type = min(defect_counts, key=defect_counts.get)

            # Calculate last week's defect counts
            last_week = worker_data['Date'].max() - pd.DateOffset(weeks=1)
            last_week_data = worker_data[worker_data['Date'] > last_week]
            last_week_defect_counts = last_week_data[['Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low']].sum().to_dict()
            last_week_highest_defect_type = max(last_week_defect_counts, key=last_week_defect_counts.get)
            last_week_lowest_defect_type = min(last_week_defect_counts, key=last_week_defect_counts.get)

            # Plot forecasts
            for defect_type in ['Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low']:
                plt.figure()
                plt.plot(worker_data['Date'], worker_data[defect_type], label='Observed', color='blue')
                future_dates = pd.date_range(start=worker_data['Date'].max(), periods=6, freq='B')[1:]
                future_forecast = time_series_forecasts[defect_type]
                plt.plot(future_dates, future_forecast, label='Forecast', color='purple', linestyle='--', marker='o')
                plt.title(f'Forecast for {defect_type} (Worker {worker_id})')
                plt.xlabel('Date')
                plt.ylabel(f'{defect_type} Count')
                plt.legend()
                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode('utf8')
                plots.append(plot_url)
                plt.close()

        return render_template('index.html', worker_name=worker_name, defect_counts=defect_counts, 
                               highest_defect_type=highest_defect_type, lowest_defect_type=lowest_defect_type,
                               last_week_highest_defect_type=last_week_highest_defect_type, 
                               last_week_lowest_defect_type=last_week_lowest_defect_type,
                               last_week_defect_counts=last_week_defect_counts,
                               plots=plots, error=error)
    except Exception as e:
        error = str(e)
        print(f"Error: {error}")
        return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
