from nlp.base_core import BaseCore
from transformers import pipeline
from bson import ObjectId

class SentCore(BaseCore):
    def __init__(self):
        super().__init__(
            task="sentiment-analysis",
            model_name="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def process_article(self, article_id: str):
        #Retrieve article by ID
        article = self.collection.find_one({"_id": ObjectId(article_id)})

        if not article:
            print(f"No article found with ID: {article_id}")
            return []

        if article.get("sentiment_processed") is True:
            print(f"Article {article_id} already processed.")
            return []

        # We have a check running so only articles with full text are saved
        full_text = article.get("full_text", "")
        # if not full_text:
        #     print(f"Article {article_id} has no full text.")
        #     return

        # Run Sentiment Analysis
        print("about to run Sentiment Analysis")
        results = self.pipeline(full_text)
        print("ran Sentiment Analysis yay")

        # Update article in DB
        self.addToEntryInDB(article_id, {
            "sentiment analysis": results,
            "sentiment_processed": True
        })

        return results
    
    def addToEntryInDB(self, entry_id, updates):
        print("Adding Sentiment Analysis results to database\r\r\r")

        id = ObjectId(entry_id)
        self.collection.update_one(
            {"_id": id},
            {"$set": updates}
        )