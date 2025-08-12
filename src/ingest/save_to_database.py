from pymongo import MongoClient
from celery import current_app
from celery.exceptions import NotRegistered

client = MongoClient("mongodb://myuser:mypassword@mongo:27017/justinsightdb?authSource=admin")

# Get (or create) a database
db = client["justinsightdb"]

# Get (or create) a collection
collection = db["articles"]

def save_entry(entry, using_celery):
    #locally import tasks just in this method to prevent circular import
    from justinsight.tasks import ner_task

    # #dont save entries without body text --moved this check earlier in the code
    # if entry["full_text"] == "" or entry["full_text"] == None:
    #     print("Unable to fetch full text.")
    #     return

    #check if the entry has already been saved and if it has not then save it
    entry_hash = entry["id"]
    if collection.count_documents({"id": entry_hash}) == 0:

        result = collection.insert_one(entry)
        print(f"I have now saved: {entry['title']}")
        inserted_id = result.inserted_id

        print("Right before the try")
        if using_celery:
            print("I am within the try")
            # Ensure we’re inside a celery app context and the task is known
            try:
                current_app.tasks[ner_task.name]
                #TODO: The following line can be used when connected to EC2 to actually use a GPU
                #ner_task.apply_async(args=[str(inserted_id)], queue='gpu')
                print("Checkpoint 1")
                ner_task.apply_async(args=[str(inserted_id)])
            except NotRegistered:
                # fallback to inline
                print("Checkpoint 2")
                ner_task(str(inserted_id))
        else:
            # Inline execution
            print("Checkpoint 3")
            ner_task(str(inserted_id))
