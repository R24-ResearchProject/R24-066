import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['SeamSense']

st.title("View Defect and Demographic Data")

# Fetch DefectDetails data
defect_details = list(db['DefectDetails'].find())
if defect_details:
    df_defect_details = pd.DataFrame(defect_details)
    st.subheader("Defect Details")
    st.write(df_defect_details)
else:
    st.subheader("Defect Details")
    st.write("No data available")

# Fetch DemographicData data
demographic_data = list(db['DemographicData'].find())
if demographic_data:
    df_demographic_data = pd.DataFrame(demographic_data)
    st.subheader("Demographic Data")
    st.write(df_demographic_data)
else:
    st.subheader("Demographic Data")
    st.write("No data available")
