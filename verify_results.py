from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
uri = os.getenv("DB")

# Connect to MongoDB
client = MongoClient(uri)
results_db = client["blockchainResults"]
results_collection = results_db["results"]

# Fetch all stored results
results = list(results_collection.find({}))

if results:
    for result in results:
        print(result)
else:
    print("No results found in MongoDB.")
