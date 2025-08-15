from pymongo import MongoClient
from bson import ObjectId
from transformers import pipeline

class BaseCore:
    # Include username, password, and authentication database
    client = MongoClient("mongodb://myuser:mypassword@mongo:27017/justinsightdb?authSource=admin")
    db = client["justinsightdb"]
    collection = db["articles"]

    model = None #Set in subclass

    def __init__(self, task: str, model_name: str, aggregation_strategy: str = None):
        self.task = task
        self.model_name = model_name
        self.aggregation_strategy = aggregation_strategy
        self.pipeline = self.load_pipeline()

    def load_pipeline(self):
        args = {"model": self.model_name}
        if self.task == "ner" and self.aggregation_strategy:
            args["aggregation_strategy"] = self.aggregation_strategy
        
        print(f"pipeline loading...")
        return pipeline(self.task, args)

    def process_article(self, article_id: str):
        #Retrieve article by ID
        article = self.collection.find_one({"_id": ObjectId(article_id)})

        if not article:
            print(f"No article found with ID: {article_id}")
            return []

        # We have a check running so only articles with full text are saved
        full_text = article.get("full_text", "")
        # if not full_text:
        #     print(f"Article {article_id} has no full text.")
        #     return

        entities = self.pipeline(full_text)

        self.collection.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {
                "entities": entities
            }}
        )
        return entities
