# Component04/Database/setup_database.py
from pymongo import MongoClient

# Establish connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['SeamSense']

# Create collections
db.create_collection('DefectDetails')
db.create_collection('DemographicData')

print("Collections created successfully.")