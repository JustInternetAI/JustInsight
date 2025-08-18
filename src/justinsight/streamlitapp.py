import os
import streamlit as st
from pymongo import MongoClient
import pandas as pd
from nlp.insertIntoChroma import retrieve_context
from nlp.insertIntoChroma import generate_answer
from nlp.insertIntoChroma import chunk_text
from bson import ObjectId

st.set_page_config(layout="wide")

# Include username, password, and authentication database
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["justinsightdb"]
collection = db["articles"]

st.title("Database Viewing and News Article RAG")

# Load data from MongoDB
data = list(collection.find())

# Convert ObjectId to string for each document and check if ingested
for doc in data:
    doc['_id'] = str(doc['_id'])

df = pd.DataFrame(data)

columns_to_show = st.multiselect("Columns to display", options=df.columns.tolist(), default=df.columns.tolist())
st.dataframe(df[columns_to_show])#, use_container_width=True)

query = st.text_input("Ask something about the news:")
if query:
    # For debugging purposes
    if "Chunks: " in query:
        objId = query[8:]
        chunks = chunk_text(collection.find_one({'_id' : ObjectId(objId)})['full_text'])
        st.write(chunks)

    else:
        results = retrieve_context(query, k=5)
        st.write("Top relevant chunks:")
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            st.markdown(f"**{meta['title']} ({meta['date']})**\n\n{doc}\n---")

        answer = generate_answer(query, results)
        st.write(answer)

