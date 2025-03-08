import hashlib
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
from bson import ObjectId
import os
from datetime import datetime

# Load environment variables
load_dotenv() 
uri = os.getenv("DB")  # Ensure your .env file contains DB="mongodb://localhost:27017/" (or your connection string)

# Connect to MongoDB using the database "blockchain_db"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["blockchain_db"]

# Collections: "blockchain" for the blockchain data, and "results" for integrity check results
blockchain_collection = db["blockchain"]
results_collection = db["results"]

def parse_data(block):
    """Ensure block['data'] is a dictionary."""
    data = block.get("data", {})
    if isinstance(data, str):  # If it's a JSON string, parse it
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            data = {}  # Default to empty dictionary if parsing fails
    return data

def hash_block(block):
    """Create a SHA-256 hash of the JSON stringified block."""
    
    def convert_mongo_types(obj):
        """Ensure MongoDB-specific types are JSON serializable."""
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        elif isinstance(obj, bytes):
            return obj.hex()  # Convert bytes to hex string
        return obj

    # Convert the entire block to a JSON string with sorted keys
    block_json = json.dumps(block, default=convert_mongo_types, sort_keys=True)
    return hashlib.sha256(block_json.encode()).hexdigest()

def verify_signature(public_key_pem, signature, block_hash):
    """Verify ECDSA signature using the block hash."""
    try:
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        public_key.verify(bytes.fromhex(signature), block_hash.encode(), ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        print(f"Signature verification error: {e}")
        return False

def verify_blockchain():
    """Check blockchain integrity and store results in the 'results' collection."""
    # Fetch blockchain data in order from the "blockchain" collection
    blocks = list(blockchain_collection.find().sort("_id", 1))
    if not blocks:
        print("No blocks found in the blockchain.")
        return
    
    integrity_results = []
    for i in range(1, len(blocks)):  # Start from the second block
        prev_block = blocks[i - 1]
        curr_block = blocks[i]

        # Parse the 'data' field to ensure it's a dictionary
        prev_data = parse_data(prev_block)
        curr_data = parse_data(curr_block)

        # Hash the previous block
        calculated_prev_hash = hash_block(prev_block)

        # Initialize the result structure for this block comparison
        block_result = {
            "block_index": i,
            "timestamp": datetime.utcnow().isoformat(),
            "valid": True,
            "errors": []
        }

        # Check previous hash consistency
        prev_hash_stored = curr_data.get("constructordata", {}).get("prevHash")
        if prev_hash_stored != calculated_prev_hash:
            block_result["valid"] = False
            block_result["errors"].append("Previous hash mismatch")

        # Hash the current block
        block_hash = hash_block(curr_block)

        # Verify nonce validity (example: valid if block_hash starts with '0000')
        # You can adjust difficulty as needed (default here is 4 leading zeroes)
        difficulty = curr_block.get("difficulty", 4)
        if not block_hash.startswith("0" * difficulty):
            block_result["valid"] = False
            block_result["errors"].append(f"Invalid nonce (expected {difficulty} leading zeroes)")

        # Verify digital signature (signature should be computed on block_hash)
        public_key_field = curr_data.get("constructordata", {}).get("pk", "")
        signature_field = curr_block.get("signature", "")
        try:
            if not verify_signature(public_key_field, signature_field, block_hash):
                block_result["valid"] = False
                block_result["errors"].append("Invalid signature")
        except Exception as e:
            block_result["valid"] = False
            block_result["errors"].append(f"Signature verification error: {str(e)}")

        # Verify next public key consistency
        prev_next_pk = prev_data.get("constructordata", {}).get("nextPk", "").strip()
        curr_pk = curr_data.get("constructordata", {}).get("pk", "").strip()
        if prev_next_pk != curr_pk:
            block_result["valid"] = False
            block_result["errors"].append("Next public key mismatch")

        # Append the result for this block
        integrity_results.append(block_result)

    # Insert results into the "results" collection only if there are any results
    if integrity_results:
        results_collection.insert_many(integrity_results)
        print("Integrity issues found and recorded in MongoDB.")
    else:
        print("Blockchain integrity is intact.")

if __name__ == "__main__":
    verify_blockchain()
