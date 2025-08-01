import os
from pymongo import MongoClient
from celery import current_app
from celery.exceptions import NotRegistered

# Default to local MongoDB when not using docker
#mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
#mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
# mongodb_uri = os.getenv(
#     "MONGODB_URI",
#     "mongodb://myuser:mypassword@localhost:27017/justinsightdb?authSource=admin"
# )
# Include username, password, and authentication database

client = MongoClient("mongodb://myuser:mypassword@mongo:27017/justinsightdb?authSource=admin")

# Get (or create) a database
db = client["justinsightdb"]

# Get (or create) a collection
collection = db["articles"]

def save_entry(entry, using_celery):
    #locally import tasks just in this method to prevent circular import
    from justinsight.tasks import runNER_task

    #dont save entries without body text
    if entry["full_text"] == "" or entry["full_text"] == None:
        return

    #check if the entry has already been saved and if it has not then save it
    entry_hash = entry["id"]
    if collection.count_documents({"id": entry_hash}) == 0:

        collection.insert_one(entry)
        print(f"I have now saved: {entry['title']}")

def update_article(article_id: str, updates: dict):
    collection.update_one({"id": article_id}, {"$set": updates})

        result = collection.insert_one(entry)
        inserted_id = result.inserted_id

        if using_celery:
            # Ensure we’re inside a celery app context and the task is known
            try:
                current_app.tasks[runNER_task.name]
                runNER_task.apply_async(args=[str(inserted_id)], queue='gpu')
            except NotRegistered:
                # fallback to inline
                runNER_task(str(inserted_id))
        else:
            # Inline execution
            runNER_task(str(inserted_id))


        #print(f"I have now saved: {entry['title']}")

