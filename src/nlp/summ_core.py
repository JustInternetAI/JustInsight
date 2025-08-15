from nlp.base_core import BaseCore
from transformers import pipeline
from bson import ObjectId

class SummCore(BaseCore):
    def __init__(self):
        super().__init__(
            task="summarization",
            model_name="facebook/bart-large-cnn"
        )

    def process_article(self, article_id: str):
        #Retrieve article by ID
        article = self.collection.find_one({"_id": ObjectId(article_id)})

        if not article:
            print(f"No article found with ID: {article_id}")
            return []

        if article.get("summary_processed") is True:
            print(f"Article {article_id} already processed.")
            return []

        # We have a check running so only articles with full text are saved
        full_text = article.get("full_text", "")
        # if not full_text:
        #     print(f"Article {article_id} has no full text.")
        #     return

        # Run Summarization
        print("about to run Summarization")
        summary = self.pipeline(
            full_text,
            max_length=150,
            min_length=30,
            do_sample=False) # run_ner_hf(full_text)
        print("ran Summarization yay")

        # Update article in DB
        self.addToEntryInDB(article_id, {
            "hf summary": summary,
            "summary_processed": True
        })

        return summary
    
    def addToEntryInDB(self, entry_id, updates):
        print("Adding Summarization results to database\r\r\r")
                
        id = ObjectId(entry_id)
        self.collection.update_one(
            {"_id": id},
            {"$set": updates}
        )