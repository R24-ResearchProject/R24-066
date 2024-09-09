import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import joblib
import os

# Load the data
data_path = '/Users/minu/Desktop/R24-066/Component 04/Dataset/worker_defect_production_data.csv'
df = pd.read_csv(data_path)

# Convert Date column to datetime and set as index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Identify and drop duplicate dates, keeping the first occurrence
df = df[~df.index.duplicated(keep='first')]

# Ensure the index has a defined frequency (assuming daily data here)
df = df.asfreq('D') 

# Fill missing values if any
df = df.fillna(method='ffill').fillna(method='bfill')

# List of defect types to model
defect_types = ['Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low']

# Directories for saving models and forecasts
forecast_output_dir = '/Users/minu/Desktop/R24-066/Component 04/Dataset/worker_forecasts_dataset'
binary_output_dir = '/Users/minu/Desktop/R24-066/Component 04/Dataset/worker_binary_dataset'
model_output_dir = '/Users/minu/Desktop/R24-066/Component 04/Backend/Save_model'
os.makedirs(forecast_output_dir, exist_ok=True)
os.makedirs(binary_output_dir, exist_ok=True)
os.makedirs(model_output_dir, exist_ok=True)

def train_arima_model(data, order=(1, 1, 1), steps=5):
    """Train an ARIMA model and forecast future data."""
    model = ARIMA(data, order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return model_fit, forecast

def calculate_rmse(actual, forecast):
    """Calculate Root Mean Squared Error between actual and forecasted values."""
    mse = mean_squared_error(actual, forecast)
    rmse = np.sqrt(mse)
    return rmse

def to_binary_classification(series, threshold):
    """Convert a time series to binary classification based on a threshold."""
    return (series > threshold).astype(int)

# Prepare DataFrame to store forecasts
time_series_forecasts = pd.DataFrame(index=pd.date_range(start=df.index[-1], periods=6, freq='D')[1:])

# Prepare DataFrame to store binary forecasts and actuals
binary_forecasts = pd.DataFrame(index=time_series_forecasts.index)
binary_actuals = pd.DataFrame(index=df.index[-5:])

# Example threshold for binary classification
threshold = 0  # Adjust this according to your needs

# Train ARIMA models for each defect type and make forecasts
for defect_type in defect_types:
    print(f"Training ARIMA model for {defect_type}...")
    try:
        # Train the model and make forecast
        model_fit, forecast = train_arima_model(df[defect_type], order=(1, 1, 1), steps=5)
        time_series_forecasts[defect_type] = forecast

        # Convert forecast and actuals to binary
        binary_forecast = to_binary_classification(forecast, threshold)
        binary_forecasts[defect_type] = binary_forecast

        binary_actual = to_binary_classification(df[defect_type][-5:], threshold)
        binary_actuals[defect_type] = binary_actual

        # Calculate RMSE
        if len(df[defect_type]) >= 5:
            rmse = calculate_rmse(df[defect_type][-5:], forecast)
            print(f"RMSE for {defect_type}: {rmse}")

        # Calculate binary classification metrics
        accuracy = accuracy_score(binary_actual, binary_forecast)
        precision = precision_score(binary_actual, binary_forecast)
        recall = recall_score(binary_actual, binary_forecast)
        f1 = f1_score(binary_actual, binary_forecast)

        print(f"Metrics for {defect_type}:")
        print(f"  - Accuracy: {accuracy}")
        print(f"  - Precision: {precision}")
        print(f"  - Recall: {recall}")
        print(f"  - F1 Score: {f1}")
        print('----------------------------------------------------------------')

        # Plotting the results
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df[defect_type], label='Observed', color='red')
        future_dates = pd.date_range(start=df.index[-1], periods=6, freq='D')[1:]
        plt.plot(future_dates, forecast, label='Forecast', linestyle='--', marker='o', color='purple')
        plt.title(f'Future forecast for {defect_type}')
        plt.xlabel('Date')
        plt.ylabel(f'{defect_type} Count')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Plotting the binary metrics
        plt.figure(figsize=(10, 6))
        plt.bar(['Accuracy', 'Precision', 'Recall', 'F1'], [accuracy, precision, recall, f1], color='blue')
        plt.title(f'Binary Metrics for {defect_type}')
        plt.ylabel('Score')
        plt.show()

        # Save the model
        model_file = os.path.join(model_output_dir, f'arima_model_{defect_type}.pkl')
        joblib.dump(model_fit, model_file)
    except Exception as e:
        print(f"An error occurred for {defect_type}: {e}")
        import traceback
        traceback.print_exc()

# Save all forecasts to a CSV file
forecast_file_path = os.path.join(forecast_output_dir, 'time_series_forecasts.csv')
time_series_forecasts.to_csv(forecast_file_path)
print(f"Forecasts saved to {forecast_file_path}")

# Save binary forecasts if needed
binary_forecasts_file_path = os.path.join(binary_output_dir, 'binary_forecasts.csv')
binary_forecasts.to_csv(binary_forecasts_file_path)
print(f"Binary forecasts saved to {binary_forecasts_file_path}")