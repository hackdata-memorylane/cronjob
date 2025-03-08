import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
uri = os.getenv("DB")

# Connect to MongoDB
client = MongoClient(uri)
db = client["blockchainDB"]  
blockchain_collection = db["blockchain"]  

# Check if collection has data
count = blockchain_collection.count_documents({})
print(f"Total blocks in collection: {count}")

# Fetch some sample data
sample = blockchain_collection.find_one()
print("Sample block:", sample)

blockchain_collection.insert_one({
    "index": 1,
    "previous_hash": "0",
    "timestamp": 1710000000,
    "data": "Genesis Block",
    "hash": "abc123"
})
