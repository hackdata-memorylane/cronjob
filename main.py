from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv, dotenv_values
from flask import Flask, jsonify
from bson import ObjectId
import os

load_dotenv() 
uri = os.getenv("DB")

def convert_objectid_to_str(doc):
    """Convert MongoDB ObjectId to string in a document"""
    doc["_id"] = str(doc["_id"])
    return doc


def convert_objectid_to_str(document):
    """Recursively converts ObjectId fields in a document to string."""
    if isinstance(document, list):
        return [convert_objectid_to_str(item) for item in document]
    elif isinstance(document, dict):
        return {key: (str(value) if isinstance(value, ObjectId) else convert_objectid_to_str(value))
                for key, value in document.items()}
    else:
        return document

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["sample_mflix"]  # Make sure this matches your database name
    results_collection = db["comments"]  # Collection storing integrity check results
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Initialize Flask app
app = Flask(__name__)

# API endpoint to fetch all integrity check results
@app.route("/results", methods=["GET"])
def get_results():
    results = list(results_collection.find({}))  # Get all results
    results = [convert_objectid_to_str(doc) for doc in results]  # Convert _id to string
    return jsonify(results) if results else jsonify({"message": "No results found"})


# API endpoint to fetch the latest integrity check
@app.route("/latest", methods=["GET"])
def get_latest():
    latest_result = results_collection.find_one(sort=[("timestamp", -1)], projection={"_id": 0})
    return jsonify(latest_result if latest_result else {"message": "No checks found"})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)