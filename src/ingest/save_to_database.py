from pymongo import MongoClient

# Include username, password, and authentication database
client = MongoClient("mongodb://myuser:mypassword@mongo:27017/justinsightdb?authSource=admin")

# Get (or create) a database
db = client["justinsightdb"]

# Get (or create) a collection
collection = db["articles"]

def save_entry(entry):
    #check if the entry has already been saved and if it has not then save it
    entry_hash = entry["id"]
    if collection.count_documents({"id": entry_hash}) == 0:
        collection.insert_one(entry)
    else:
        print(f"{entry['title']} already in use!")
