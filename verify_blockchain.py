import os
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
uri = os.getenv("DB")

# Connect to MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["blockchain_db"]  # Blockchain database
blockchain_collection = db["blockchain"]  # Blockchain collection

def fetch_blockchain():
    """Fetch and display all blocks from the blockchain database."""
    blocks = list(blockchain_collection.find().sort("_id", 1))  # Fetch all blocks in order

    if not blocks:
        return {"message": "No blocks found in blockchain database"}
    
    # Convert BSON to JSON-friendly format
    for block in blocks:
        block["_id"] = str(block["_id"])  # Convert ObjectId to string

    return blocks  # Return the blockchain data

if __name__ == "__main__":
    blockchain_data = fetch_blockchain()
    print(json.dumps(blockchain_data, indent=4))
