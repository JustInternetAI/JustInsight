from transformers import pipeline
from ingest.save_to_database import collection, update_article

# Load once, reuse
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

def run_ner_hf(text: str):
    results = ner_pipeline(text)
    return [
        {
            "text": ent["word"],
            "label": ent["entity_group"],
            "start": ent["start"],
            "end": ent["end"]
        }
        for ent in results
    ]

def process_article(article_id: str):
    #Retrieve article by ID
    article = collection.find_one({"id": article_id})

    if not article:
        print(f"No article found with ID: {article_id}")
        return []

    if article.get("processed") is True:
        print(f"Article {article_id} already processed.")
        return []

    full_text = article.get("full_text", "")
    if not full_text:
        print(f"Article {article_id} has no full text.")
        return []

    # Run NER
    entities = run_ner_hf(full_text)

    # Update article in DB
    update_article(article_id, {
        "ner": entities,
        "processed": True
    })

    return entities

