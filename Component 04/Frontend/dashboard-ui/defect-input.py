import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
from pymongo import MongoClient
import time  # Import the time module

# Function to display the live time
def display_live_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to insert data into the MongoDB database
def insert_into_db(worker_id, date, run_off, open_seam, spi_errors, high_low, production_volume, shift):
    defect_count = run_off + open_seam + spi_errors + high_low
    count = production_volume - defect_count

    # Establish connection to the MongoDB database
    client = MongoClient('mongodb://localhost:27017/')
    db = client['SeamSense']
    collection = db['DefectDetails']

    # Convert the date to a string in the required format
    date_str = date.strftime('%Y-%m-%d')

    # Check if the record already exists
    existing_record = collection.find_one({"Worker_ID": worker_id, "Date": date_str})
    if existing_record:
        st.error(f"Data for worker {worker_id} on {date_str} already exists.")
        return False

    try:
        new_data = {
            "Worker_ID": worker_id,
            "Date": date_str,
            "Run_Off": run_off,
            "Open_Seam": open_seam,
            "SPI_Errors": spi_errors,
            "High_Low": high_low,
            "Production_Volume": production_volume,
            "Shift": shift,
            "defect_count": defect_count,
            "count": count
        }
        collection.insert_one(new_data)
        st.success("Data saved successfully to the database.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False
    return True

# Streamlit app layout
st.set_page_config(layout="wide")

# Title of the app
st.title("Defect Details Submit Portal")

# Create two columns, with the right column for the time display
col1, col2 = st.columns([9, 1])

with col2:
    time_placeholder = st.empty()
    time_placeholder.markdown(f"<p style='text-align: right; font-size: 14px;'>{display_live_time()}</p>", unsafe_allow_html=True)

# Worker ID input field
worker_id = st.text_input("Worker ID", value="W_")  # Default value can be set as "W_"

# Input fields for defect details
run_off_count = st.number_input("Run Off", min_value=0, step=1)
open_seam_count = st.number_input("Open Seam", min_value=0, step=1)
spi_error_count = st.number_input("SPI Error", min_value=0, step=1)
high_low_count = st.number_input("High Low", min_value=0, step=1)
production_volume = st.number_input("Production Volume", min_value=0, step=1)
shift = st.selectbox("Shift", options=["Morning", "Night"])

# Define today's and yesterday's dates
today = datetime.today().date()
yesterday = today - timedelta(days=1)

# Date selection with restriction
selected_date = st.date_input("Select Date", value=today, max_value=today, min_value=yesterday)

if st.button("Submit"):
    # Validate all required fields are filled
    if not worker_id or not worker_id.startswith("W_"):
        st.error("Invalid Worker ID. Please ensure it starts with 'W_'.")
    elif any(field is None for field in [run_off_count, open_seam_count, spi_error_count, high_low_count, production_volume]):
        st.error("All fields are required. Please fill in all fields.")
    else:
        # Insert the data into the MongoDB database
        success = insert_into_db(worker_id, selected_date, run_off_count, open_seam_count, spi_error_count, high_low_count, production_volume, shift)
        if success:
            # Save the data to a CSV file (Optional, if you want to maintain a backup)
            file_path = '/Users/minu/Desktop/R24-066/Component 04/Dataset/worker_defect_production_data.csv'
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if os.path.exists(file_path):
                df_existing = pd.read_csv(file_path)
            else:
                df_existing = pd.DataFrame(columns=['Worker_ID', 'Date', 'Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low', 'Production_Volume', 'Shift', 'defect_count', 'count'])

            # Calculate defect_count and count again
            defect_count = run_off_count + open_seam_count + spi_error_count + high_low_count
            count = production_volume - defect_count

            new_data = pd.DataFrame({
                'Worker_ID': [worker_id],
                'Date': [selected_date],
                'Run_Off': [run_off_count],
                'Open_Seam': [open_seam_count],
                'SPI_Errors': [spi_error_count],
                'High_Low': [high_low_count],
                'Production_Volume': [production_volume],
                'Shift': [shift],
                'defect_count': [defect_count],
                'count': [count]
            })

            df_existing = pd.concat([df_existing, new_data], ignore_index=True)
            try:
                df_existing.to_csv(file_path, index=False)
            except Exception as e:
                st.error(f"Error saving data to CSV: {e}")

            # Display the new data
            st.subheader("Submission Details")
            st.dataframe(new_data)
        else:
            st.error("Failed to save data to the database. It might already exist for this worker and date.")

# The app will automatically refresh the live time
while True:
    time_placeholder.markdown(f"<p style='text-align: right; font-size: 14px;'>{display_live_time()}</p>", unsafe_allow_html=True)
    time.sleep(1)
