from nlp.base_core import BaseCore
from transformers import pipeline
from bson import ObjectId

class NERCore(BaseCore):
    def __init__(self):
        super().__init__(
            task="ner",
            model_name="dslim/bert-base-NER",
            aggregation_strategy="simple"
        )
    
    def process_article(self, article_id: str):
        #Retrieve article by ID
        article = self.collection.find_one({"_id": ObjectId(article_id)})

        if not article:
            print(f"No article found with ID: {article_id}")
            return []

        if article.get("processed") is True:
            print(f"Article {article_id} already processed.")
            return []

        # We have a check running so only articles with full text are saved
        full_text = article.get("full_text", "")
        # if not full_text:
        #     print(f"Article {article_id} has no full text.")
        #     return

        # Run NER
        entities = self.pipeline(full_text) # run_ner_hf(full_text)
 
        # Update article in DB
        self.addToEntryInDB(article_id, {
            "ner": entities,
            "processed": True
        })

        return entities

    def format_ner_tags(self, ner_list):
        formatted = []
        for ent in ner_list:
            label = ent.get("label") or ent.get("entity") or ent.get("entity_group", "UNKNOWN")
            text = ent.get("text") or ent.get("word") or ""
            formatted.append(f"{label}: {text}")
        return ", ".join(formatted)

    def addToEntryInDB(self, entry_id, updates):
        print("Adding NER results to database\r\r\r")

        if "ner" in updates:
            for ent in updates["ner"]:
                ent["score"] = float(ent["score"])  # convert np.float32 to Python float
                
            updates["ner_pretty"] = self.format_ner_tags(updates["ner"]) # so we can actually read the NER

        id = ObjectId(entry_id)
        self.collection.update_one(
            {"_id": id},
            {"$set": updates}
        )