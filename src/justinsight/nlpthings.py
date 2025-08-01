import os
from pymongo import MongoClient
from bson import ObjectId

# Default to local MongoDB when not using docker
mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# Include username, password, and authentication database
#client = MongoClient(mongodb_uri)
client = MongoClient("mongodb://myuser:mypassword@mongo:27017/justinsightdb?authSource=admin")

# Get (or create) a database
db = client["justinsightdb"]

# Get (or create) a collection
collection = db["articles"]

def dummy_addToEntryInDB(entry_id):
    id = ObjectId(entry_id)
    collection.update_one(
        {"_id": id},
        {"$set": {"DummyField": "I added something!"}}
    )
    print("\n\n I am trying to add a row to an entry \n\n")
