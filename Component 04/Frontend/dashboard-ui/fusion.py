import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

# Define file paths
time_series_model_paths = {
    'Run_Off': '/Users/minu/Desktop/R24-066/Component 04/Backend/Save_model/arima_model_Run_Off.pkl',
    'Open_Seam': '/Users/minu/Desktop/R24-066/Component 04/Backend/Save_model/arima_model_Open_Seam.pkl',
    'SPI_Errors': '/Users/minu/Desktop/R24-066/Component 04/Backend/Save_model/arima_model_SPI_Errors.pkl',
    'High_Low': '/Users/minu/Desktop/R24-066/Component 04/Backend/Save_model/arima_model_High_Low.pkl'
}
traditional_model_path = '/Users/minu/Desktop/R24-066/Component 04/Backend/Save_model/LassoRegression_best_model.pkl'
demographic_data_path = '/Users/minu/Desktop/R24-066/Component 04/Dataset/demographic_data_dataset.csv'
defect_data_path = '/Users/minu/Desktop/R24-066/Component 04/Dataset/worker_defect_production_data.csv'

# Load saved models
@st.cache_resource
def load_models(time_series_model_paths, traditional_model_path):
    time_series_models = {defect_type: joblib.load(path) for defect_type, path in time_series_model_paths.items()}
    traditional_model = joblib.load(traditional_model_path)
    return time_series_models, traditional_model

# Load data
@st.cache_resource
def load_data():
    demographic_data = pd.read_csv(demographic_data_path)
    defect_data = pd.read_csv(defect_data_path)

    # Convert Date columns to datetime
    demographic_data['Joining_Date'] = pd.to_datetime(demographic_data['Joining_Date'], errors='coerce')
    defect_data['Date'] = pd.to_datetime(defect_data['Date'], errors='coerce')

    # Merge datasets
    combined_data = pd.merge(defect_data, demographic_data, on='Worker_ID')

    # Drop unnecessary columns and add time-series features
    combined_data.drop(columns=['Name', 'Joining_Date'], inplace=True)
    combined_data['DayOfWeek'] = combined_data['Date'].dt.dayofweek
    combined_data['WeekOfYear'] = combined_data['Date'].dt.isocalendar().week
    combined_data['Month'] = combined_data['Date'].dt.month
    combined_data['Quarter'] = combined_data['Date'].dt.quarter

    return combined_data

# Generate time series forecasts
def generate_time_series_forecasts(models, data, defect_types):
    forecasts = {}
    for defect_type in defect_types:
        model = models[defect_type]
        forecasts[defect_type] = model.forecast(len(data))  # Modify this logic based on your model
    return pd.DataFrame(forecasts, index=data.index)

# Function to prepare fusion data
def prepare_fusion_data(time_series_forecasts, traditional_model, combined_data, defect_types):
    X_combined = combined_data.drop(columns=defect_types + ['defect_count', 'count', 'Worker_ID', 'Date'])
    preprocessor = traditional_model.named_steps['preprocessor']
    X_combined = preprocessor.transform(X_combined)
    traditional_predictions = traditional_model.named_steps['regressor'].predict(X_combined)
    traditional_predictions_df = pd.DataFrame(traditional_predictions, columns=defect_types, index=combined_data.index)
    combined_forecasts = time_series_forecasts.add(traditional_predictions_df, fill_value=0)
    return combined_forecasts

# Function to analyze and provide feedback for each worker
def analyze_worker_defect_types(worker_id, feedback_df, defect_types):
    # Retrieve feedback for the specified worker
    worker_feedback = feedback_df[feedback_df['Worker_ID'] == worker_id]

    if not worker_feedback.empty:
        st.subheader(f"Feedback for Worker ID: {worker_id}")

        # Extract metrics
        r2_list = worker_feedback['R² Score'].values[0]
        mae_list = worker_feedback['Mean Absolute Error'].values[0]

        # Determine the highest and lowest defect types
        highest_defect_type_index = np.argmax(mae_list)  # Use MAE for determining the highest error defect type
        lowest_defect_type_index = np.argmin(mae_list)   # Index of the defect type with the lowest MAE

        highest_defect_type = defect_types[highest_defect_type_index]
        lowest_defect_type = defect_types[lowest_defect_type_index]

        # Display metrics in a user-friendly way without MSE
        st.markdown(
            f"""
            <div style="background-color:#f0f8ff;padding:10px;border-radius:5px;margin:30px 0 20px 0;">
                <h3 style="color:#003366;margin-bottom:5px;">Highest Error Defect Type: <span style="font-weight:bold;">{highest_defect_type}</span></h3>
            </div>
            <div style="background-color:#e0f7fa;padding:10px;border-radius:5px;margin:30px 0 30px 0;">
                <h3 style="color:#00796b;margin-bottom:5px;">Lowest Error Defect Type: <span style="font-weight:bold;">{lowest_defect_type}</span></h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        # <p style="font-size:16px;margin:0;">R²: <b>{r2_list[highest_defect_type_index]:.2f}</b>, MAE: <b>{mae_list[highest_defect_type_index]:.2f}</b></p>
        # <p style="font-size:16px;margin:0;">R²: <b>{r2_list[lowest_defect_type_index]:.2f}</b>, MAE: <b>{mae_list[lowest_defect_type_index]:.2f}</b></p>
        # Improved Attention Section with Bold Message
        st.markdown(
            f"""
            <div style="background-color:#ffcccb;padding:10px;border-radius:5px;margin-top:20px;">
                <h3 style="color:#b30000;">⚠️ Attention Needed:</h3>
                <p style="color:#b30000;font-weight:bold;">Please focus on improving <b>{highest_defect_type}</b> as it has the highest error metrics.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.error(f"No feedback found for Worker ID: {worker_id}")

# Streamlit UI
st.title('Worker Defect Feedback Analysis')
st.write("Analyze and get feedback on defect types for each worker based on model predictions.")

# Load data and models
combined_data = load_data()
time_series_models, traditional_model = load_models(time_series_model_paths, traditional_model_path)

# Generate time series forecasts
time_series_forecasts = generate_time_series_forecasts(time_series_models, combined_data, list(time_series_models.keys()))

# Prepare fusion data
combined_forecasts = prepare_fusion_data(time_series_forecasts, traditional_model, combined_data, list(time_series_models.keys()))

# Calculate feedback metrics
worker_feedback = []

for worker_id in combined_data['Worker_ID'].unique():
    worker_data = combined_data[combined_data['Worker_ID'] == worker_id]

    if worker_data.empty:
        continue

    # Generate time-series forecasts for the worker
    worker_time_series_forecasts = generate_time_series_forecasts(time_series_models, worker_data, list(time_series_models.keys()))

    # Prepare fusion data for the worker
    worker_combined_forecasts = prepare_fusion_data(worker_time_series_forecasts, traditional_model, worker_data, list(time_series_models.keys()))

    # Align actual values for the worker
    y_actual_worker = worker_data[list(time_series_models.keys())]
    worker_combined_forecasts = worker_combined_forecasts.loc[y_actual_worker.index]

    # Generate and store feedback
    r2_worker = r2_score(y_actual_worker, worker_combined_forecasts, multioutput='raw_values')
    mae_worker = mean_absolute_error(y_actual_worker, worker_combined_forecasts, multioutput='raw_values')

    feedback = {
        'Worker_ID': worker_id,
        'R² Score': r2_worker.tolist(),
        'Mean Absolute Error': mae_worker.tolist()
    }
    worker_feedback.append(feedback)

# Convert feedback to DataFrame for analysis
worker_feedback_df = pd.DataFrame(worker_feedback)

# User input to search for feedback
st.sidebar.header("Search Worker Feedback")
worker_id_to_search = st.sidebar.text_input("Enter the Worker ID:")

if worker_id_to_search:
    defect_types = ['Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low']
    analyze_worker_defect_types(worker_id_to_search, worker_feedback_df, defect_types)
else:
    st.info("Please enter a Worker ID to get feedback.")
