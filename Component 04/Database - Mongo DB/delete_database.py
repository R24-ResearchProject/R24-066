from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Select the database
db = client['SeamSense']

# Drop the database
client.drop_database('SeamSense')

print("Database 'SeamSense' deleted successfully.")
