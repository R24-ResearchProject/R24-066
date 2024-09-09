# Function to fetch data for a specific worker and date range from the database
import datetime
import sqlite3
from turtle import pd, st


def fetch_worker_data(worker_id, start_date, end_date):
    conn = sqlite3.connect('/Users/minu/Desktop/R24-066/Component 04/Database/SeamSense.db')
    cursor = conn.cursor()
    
    # Convert dates to string in the format YYYY-MM-DD
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT * FROM DefectDetails WHERE Worker_ID = ? AND Date BETWEEN ? AND ?
    ''', (worker_id, start_date_str, end_date_str))
    data = cursor.fetchall()
    conn.close()
    return data

# Streamlit app layout
st.set_page_config(layout="wide")

# Title of the app
st.title("Defect Details Portal")

# Section to view data per worker
st.header("View Data per Worker")

# Input for Worker ID to view data
view_worker_id = st.text_input("Enter Worker ID to View Data", value="W_")

# Date range selection
start_date = st.date_input("Start Date", value=datetime.today() - datetime.timedelta(days=7))
end_date = st.date_input("End Date", value=datetime.today())

if st.button("Show Worker Data"):
    if not view_worker_id or not view_worker_id.startswith("W_"):
        st.error("Invalid Worker ID. Please ensure it starts with 'W_'.")
    elif start_date > end_date:
        st.error("Start Date cannot be after End Date.")
    else:
        data = fetch_worker_data(view_worker_id, start_date, end_date)
        if data:
            # Convert the fetched data to a DataFrame for better display
            columns = ['Worker_ID', 'Date', 'Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low', 'Production_Volume', 'Shift', 'Defect_Count', 'count']
            df = pd.DataFrame(data, columns=columns)
            st.subheader(f"Data for {view_worker_id} from {start_date} to {end_date}")
            st.dataframe(df)
        else:
            st.error(f"No data found for Worker ID: {view_worker_id} in the selected date range.")
