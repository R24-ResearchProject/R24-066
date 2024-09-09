import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Set Streamlit to wide mode and dark theme
st.set_page_config(
    page_title="Defect Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Add a friendly title to the app
st.title("📊 SeamSense: Real-Time Defect Analysis")

# Define paths for model and datasets
model_path = '/Users/minu/Desktop/R24-066/Component 04/Backend/Save_model/LassoRegression_best_model.pkl'
defect_data_path = '/Users/minu/Desktop/R24-066/Component 04/Dataset/worker_defect_production_data.csv'
demographic_data_path = '/Users/minu/Desktop/R24-066/Component 04/Dataset/demographic_data_dataset.csv'

# Verify and Load the Model
if os.path.exists(model_path):
    lasso_model = joblib.load(model_path)
    # st.success("Lasso Regression Model Loaded Successfully!")
else:
    st.error(f"Model file not found at {model_path}. Please check the path.")

# Verify and Load the Datasets
if os.path.exists(defect_data_path) and os.path.exists(demographic_data_path):
    defect_data = pd.read_csv(defect_data_path)
    demographic_data = pd.read_csv(demographic_data_path)
    # st.success("Datasets Loaded Successfully!")
else:
    st.error(f"Dataset files not found. Please check the paths.")

# Merge the datasets on Worker_ID
if 'defect_data' in locals() and 'demographic_data' in locals():
    combined_data = pd.merge(defect_data, demographic_data, on='Worker_ID', how='left')
else:
    combined_data = pd.DataFrame()

# Feature engineering: Add time-related features
if 'Date' in combined_data.columns:
    combined_data['Date'] = pd.to_datetime(combined_data['Date'], errors='coerce')  # Coerce errors to handle incorrect formats
    combined_data['DayOfWeek'] = combined_data['Date'].dt.dayofweek
    combined_data['WeekOfYear'] = combined_data['Date'].dt.isocalendar().week
    combined_data['Month'] = combined_data['Date'].dt.month
    combined_data['Quarter'] = combined_data['Date'].dt.quarter

# Function to plot charts for the selected defect type
def plot_metrics(data, defect_type):
    # Filter rows where the defect type count is greater than 0
    subset = data[data[defect_type] > 0]

    # Dynamically adjust figure size based on the content
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    # Plot Age Distribution for the selected defect type
    if 'Age' in subset.columns:
        sns.histplot(subset['Age'], ax=ax[0], kde=True, color='skyblue')
        ax[0].set_title(f'Age Distribution for {defect_type.replace("_", " ")}')
        ax[0].set_xlabel('Age')
        ax[0].set_ylabel('Frequency')
    else:
        st.warning("Column 'Age' not found in the dataset.")

    # Plot Skill Level Distribution for the selected defect type
    if 'Skill_Level' in subset.columns:
        sns.countplot(x='Skill_Level', data=subset, ax=ax[1], palette='pastel')
        ax[1].set_title(f'Skill Level Distribution for {defect_type.replace("_", " ")}')
        ax[1].set_xlabel('Skill Level')
        ax[1].set_ylabel('Count')
    else:
        st.warning("Column 'Skill_Level' not found in the dataset.")

    # Adjust layout to prevent overlap and dynamically fit the content
    plt.tight_layout()
    st.pyplot(fig)

# Mapping of defect types to user-friendly names
defect_types = {
    'Run_Off': 'Run Off',
    'Open_Seam': 'Open Seam',
    'SPI_Errors': 'SPI Errors',
    'High_Low': 'High Low'
}

# Create a selectbox with the cleaned names
selected_defect_name = st.selectbox('Select Defect Type to Display', list(defect_types.values()))

# Find the original defect type based on the user-friendly name
selected_defect = list(defect_types.keys())[list(defect_types.values()).index(selected_defect_name)]

# Display the plots if data is loaded and merged successfully
if not combined_data.empty:
    st.write(f"#### Defect Distribution by Age and Skill Level for {selected_defect_name}")
    plot_metrics(combined_data, selected_defect)
