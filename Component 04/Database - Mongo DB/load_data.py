import pandas as pd
from pymongo import MongoClient

def load_data():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['SeamSense']

        # Load CSV data
        demographic_df = pd.read_csv('/Users/minu/Desktop/R24-066/Component 04/Dataset/demographic_data_dataset.csv')
        defect_df = pd.read_csv('/Users/minu/Desktop/R24-066/Component 04/Dataset/worker_defect_production_data.csv')

        # Insert data into MongoDB
        db['DemographicData'].insert_many(demographic_df.to_dict('records'))
        db['DefectDetails'].insert_many(defect_df.to_dict('records'))

        print("Data loaded successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the MongoDB connection
        client.close()

load_data()
