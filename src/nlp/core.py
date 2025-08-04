from transformers import pipeline
from pymongo import MongoClient
from bson import ObjectId

# Include username, password, and authentication database
client = MongoClient("mongodb://myuser:mypassword@mongo:27017/justinsightdb?authSource=admin")
db = client["justinsightdb"]
collection = db["articles"]

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def process_article(article_id: str):
    #Retrieve article by ID
    article = collection.find_one({"_id": ObjectId(article_id)})

    if not article:
        print(f"No article found with ID: {article_id}")
        return []

    if article.get("processed") is True:
        print(f"Article {article_id} already processed.")
        return

    # We have a check running so only articles with full text are saved
    full_text = article.get("full_text", "")
    # if not full_text:
    #     print(f"Article {article_id} has no full text.")
    #     return

    # Run NER
    entities = ner(full_text) # run_ner_hf(full_text)

    # Update article in DB
    addToEntryInDB(article_id, {
        "ner": entities,
        "processed": True
    })

    return


def addToEntryInDB(entry_id, updates):
    print("Adding NER results to database\r\r\r")

    if "ner" in updates:
        for ent in updates["ner"]:
            ent["score"] = float(ent["score"])  # convert np.float32 to Python float

    id = ObjectId(entry_id)
    collection.update_one(
        {"_id": id},
        {"$set": updates}
    )