import os
from pymongo import MongoClient

# Default to local MongoDB when not using docker
mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

#mongodb_uri = os.getenv("mongodb://localhost:27017", "mongodb://myuser:mypassword@mongo:27017/justinsightdb?authSource=admin")

# Include username, password, and authentication database
client = MongoClient(mongodb_uri)

# Get (or create) a database
db = client["justinsightdb"]

# Get (or create) a collection
collection = db["articles"]

def save_entry(entry):
    #check if the entry has already been saved and if it has not then save it
    entry_hash = entry["id"]
    if collection.count_documents({"id": entry_hash}) == 0:
        collection.insert_one(entry)
        print(f"I have now saved: {entry['title']}")

def update_article(article_id: str, updates: dict):
    collection.update_one({"id": article_id}, {"$set": updates})