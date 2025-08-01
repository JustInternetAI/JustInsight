from celery import Celery
from ingest.save_to_database import collection
from nlp.core import run_ner_hf, process_article

app = Celery("justinsight")  # Use your actual Celery config if not centralized here

@app.task
def ner_task(article_id: str):
    # Fetch the article by ID
    article = collection.find_one({"id": article_id})

    if not article:
        print(f"No article found with ID: {article_id}")
        return

    text = article.get("full_text") or article.get("summary")
    if not text:
        print(f"No usable text found in article {article_id}")
        return

    # Run Named Entity Recognition
    entities = run_ner_hf(text)

    # Process article with NER results
    process_article(article_id, {
        "entities": entities,
        "ner_processed": True  # flag added here
    })

    print(collection)
    print(collection.__module__)
    print(f"Processed article {article_id} with {len(entities)} entities.")
    return entities