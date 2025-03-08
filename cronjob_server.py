from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
from cronjob import verify_blockchain,verify_signature
from time import sleep

# Load environment variables
load_dotenv()
uri = os.getenv("DB")

if not uri:
    raise ValueError("❌ Database URI not found! Check .env file.")

# Connect to MongoDB
client = MongoClient(uri)
db = client["blockchain_db"]
results_collection = db["blockchain"]

print("✅ Connected to MongoDB successfully!")

def run_scheduled_tasks():
    """Function that runs the blockchain verification."""
    print("🔄 Running blockchain verification cron job...")
    verify_blockchain()

while True:
    run_scheduled_tasks()
    sleep( 20)