import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from transformers import pipeline
#from transformers import AutoModelForCausalLM, AutoTokenizer
from pymongo import MongoClient
#from bson import ObjectId
from huggingface_hub import snapshot_download
import os

model_path = snapshot_download(
    "tiiuae/falcon-7b-instruct",
    cache_dir="/models",
    local_files_only=True  # prevents any online download
)

client = MongoClient("mongodb://myuser:mypassword@mongo:27017/justinsightdb?authSource=admin")
db = client["justinsightdb"]
MongoCollection = db["articles"]

client = chromadb.HttpClient(
    host="chromadb",  # Docker service name
    port=8000,
    settings=Settings()
)

def get_embedding_model():
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_llm_model():
    #this should load the pre-dowloaded (during the docker set up) model? 
    return  pipeline(
    "text-generation",
    model=model_path,
    device_map="auto",
    trust_remote_code=True
    )


model = get_embedding_model()

LLMmodel = get_llm_model()

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
        else:
            #make sure to not cut off ending sentence
            while end < len(words) and "." not in words[end]:
                end = end + 1
            if end == len(words):
                end = end -1

        if start > 0:
            #make sure to not cut off starting sentence
            while "." not in words[start]:
                start = start + 1
                # if start == 0:
                #     break
        
        #if we arent starting at the beginning we need to go one word past the word that contians "."
        if start != 0:
            start = start + 1

        chunk = " ".join(words[start:end+1])
        chunks.append(chunk)
        start += chunk_size - overlap
        if end == len(words)-1:
            start = len(words) #so we exit while

    return chunks

def retrieve_context(query, k=5, date_after=None):
    q_embedding = model.encode(query)

    where_filter = {}
    if date_after:
        where_filter["date"] = {"$gt": date_after}

    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=k,
        where=where_filter if where_filter else None
    )

    return results


def generate_answer(query, contexts):
    # Extract only what the model needs
    # docs = contexts.get("documents", [[]])[0]
    # titles = [m.get("title", "") for m in contexts.get("metadatas", [[]])[0]]
    
    # context_str = ""
    # for t, d in zip(titles, docs):
    #     context_str += f"Title: {t}\nContent: {d}\n\n"

    # prompt = f"""
    # You are a helpful assistant. Use the following context to answer the question. 
    # If the answer cannot be found, say "I don’t know."

    # Context:
    # {context_str}

    # Question: {query}
    # Answer:
    # """
    prompt = "Hello, I am just testing my ability to connect to this LLM. Please confirm the connection."
    print(f"Prompt: {prompt!r}")
    return LLMmodel(prompt, max_new_tokens=200, do_sample=True, temperature=0.2)


def qa_task(query):
    return generate_answer(query, retrieve_context(query))


def ingest_article(article_id, title, text, date):
    chunks = chunk_text(text)
    embeddings = [model.encode(chunk) for chunk in chunks]
    ids = [f"{article_id}_{i}" for i in range(len(chunks))]
    metadatas = [{"article_id": article_id, "title": title, "date": date} for _ in chunks]
    
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    print(f"Ingested article: {title}")
    
    MongoCollection.update_one(
        {"id": article_id},
        {"$set": {"ChromaIngested": True}}
    )