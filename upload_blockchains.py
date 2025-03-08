from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv() 

# Replace with your MongoDB Atlas connection string
MONGO_URI = os.getenv("DB")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["blockchain_db"]
collection = db["blockchain"]

# Blockchain dataset with full-length RSA public keys
blockchain_data = [
    {
        "_id": "abc123",
        "block_id": 1,
        "hash": "abcd9876",
        "previous_hash": "xyz1234",
        "timestamp": "2025-03-08T12:00:00",
        "data": {
            "transaction": "Transaction details here",
            "pk": """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7Vn6DrfV7gIwEdjArKhV
bq50YGhGRhv4mUebKRCm72pi4uT8/yNk68mBXfuSLf1huYPph6z4u01L1dEZcD52
9E5dpHkR6iGxysRWTukz8X+nUN9jUBUBHjIzXYRaVqL5tq4bJkdytG9ltZG0JnpV
BzSzfGbAz5Tqz6+UoAWqPbA8mBNh9pJboUL0pPUN5xTtZZmI5GnI1sApH1zdhdbL
C4uM6YmhrzqU8nXxHQj/Y2RbGek5RjE0ZgKK4fcsL+YP0qNfshZp85d7LihSTc+n
/cfHBymAQQBnt8ZoTzY/NH3YwwYAKy7KYPH5gYJLh0BAebXzZ7SIZ8UyynHZWiT2
4wIDAQAB
-----END PUBLIC KEY-----"""
        }
    },
    {
        "_id": "def456",
        "block_id": 2,
        "hash": "mnop3456",
        "previous_hash": "abcd9876",
        "timestamp": "2025-03-08T12:05:00",
        "data": {
            "transaction": "Payment processed",
            "pk": """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv9sUBCmM/MhfRq3c4i3m
SbE+l2EpHdrrtZ5opTUbGH6wmE07F1Pj6S2V6Cf05P1LgA6ZLtDeiCLOHnFPA1h5
d/A8K/INjsgjlUGtP+VrHtHAY+Uxn3p3NMC3MbexU5yPfbf4S+b+X4nV/RDujFxF
IVhPxyW9AKJdkdqfVqByYgU+mpn3P6+JaT8PPqBM8uMrHlyWAl5b+UuOYB9lYPfJ
GmE1Ja+zHn/VfO54pqF4M8p+9+B+JKh7GVhImTzJ5tPAWVaSxWvTlx9H+RJ+lNR5
53b1CVORU0oworVdP0yk5JtL8Tf0QOGdI2HEUtT5nUoIqFhJ1c6ic/OzKwIDAQAB
-----END PUBLIC KEY-----"""
        }
    },
    {
        "_id": "ghi789",
        "block_id": 3,
        "hash": "qrst5678",
        "previous_hash": "mnop3456",
        "timestamp": "2025-03-08T12:10:00",
        "data": {
            "transaction": "User registration verified",
            "pk": """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8HqE5prvx/PRD4vvqbd8
3eDklPQ4/PUVYKokGb3G5qEoU0Q5JZbXKowETI6JBOP/0lyXlxLSMh3Bwl0/M3rK
or2hOQRoOlB6P4+y8x9ktXxMtTkJ8YKeMEVCds6QELPUnk0X7NcVqkRfdmgXZo+W
G7+xLqRfQg8/jbm+PWTGrljPRMK4il1IUsRPSH7U1vN4MnzmgLds4EGF5j77pkj+
qJcMIwAaiWBo+o6hb3a9uU5LwYpXzSP73W1mdqP6XOV+R9f3tfgWJ8iD4xyKPBpZ
K1HhThFkOxE7DoQ15Rq/DuYFV+57SwjbP9wvfJ2hbcP+R+LFeOIBmIzNtwIDAQAB
-----END PUBLIC KEY-----"""
        }
    },
    {
        "_id": "jkl012",
        "block_id": 4,
        "hash": "uvwx9012",
        "previous_hash": "qrst5678",
        "timestamp": "2025-03-08T12:15:00",
        "data": {
            "transaction": "Asset transfer recorded",
            "pk": """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAn/sm/qQF/AJDUQcx0E5T
hV27CBkpP1bM1X+H7iKhgrvHcZ5ZWaT69DQRSc9BGmtZxBprLC6Ueb7nC4GbZKrb
npXExPo/DwaMFxPPUjTUGe6kLv6rjMY4sRIfZLV4mGMeLK1FyrTqI44XMIjBw2Lp
W/xTo3gXtM1ugyLsmWzfj4tz8py9A7O3/VuQzCk3KwO+xTpXBw8Xs5Vnv0BpLYyH
Ap6smvcP+WXC1MoB8z5nlZ9fXlXEB0U+5TkvKJ7p3LyN10/pIfpYvMTVfPoyHyxD
X5b+Nuv0dGlR6AwNhgpDlH1M+UsFYJ/YwPSrYEdlENaxTksHavxE9b78qQIDAQAB
-----END PUBLIC KEY-----"""
        }
    }
]

# Insert data into MongoDB
try:
    result = collection.insert_many(blockchain_data)
    print("Inserted block IDs:", result.inserted_ids)
except Exception as e:
    print("Error inserting data:", e)

# Close connection
client.close()
