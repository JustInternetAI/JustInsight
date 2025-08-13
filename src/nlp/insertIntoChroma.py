import chromadb
from chromadb.config import Settings
import uuid
from datetime import datetime
from textwrap import wrap
from sentence_transformers import SentenceTransformer

client = chromadb.HttpClient(
    host="chromadb",  # Docker service name
    port=8000,
    settings=Settings()
)

def get_embedding_model():
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

model = get_embedding_model()

# Create / get collection
collection = client.get_or_create_collection(name="news_articles")

# def embed_text(text, model):
#     return model.encode(text)

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        if end > len(words)-1:
            end = len(words)-1
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
        if end == len(words)-1:
            start = len(words) #so we exit while
    return chunks

def retrieve(query, k=5, date_after=None):
    q_embedding = model.encode(query)

    where_filter = {}
    # if category:
    #     where_filter["category"] = category
    if date_after:
        where_filter["date"] = {"$gt": date_after}

    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=k,
        where=where_filter if where_filter else None
    )

    return results

def ingest_article(article_id, title, text, date):
    chunks = chunk_text(text)
    embeddings = [model.encode(chunk) for chunk in chunks]
    ids = [f"{article_id}_{i}" for i in range(len(chunks))]
    metadatas = [{"article_id": article_id, "title": title, "date": date} for _ in chunks]
    
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f"Ingested article: {title}")

# # Example
# if __name__ == "__main__":
#     sample_article = {
#         "article_id": str(uuid.uuid4()),
#         "title": "Sample News Title",
#         "text": "Your article text here...",
#         "date": datetime.now().isoformat(),
#     }
#     ingest_article(**sample_article)
