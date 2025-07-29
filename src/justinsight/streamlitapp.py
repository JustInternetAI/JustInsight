import os
import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Default to local MongoDB when not using docker --- NO I dont want a local database at all
#mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# Include username, password, and authentication database
#client = MongoClient(mongo_uri)
client = MongoClient(os.getenv("MONGODB_URI"))

# Get (or create) a database
db = client["justinsightdb"]

# Get (or create) a collection
collection = db["articles"]

st.title("Database Viewing")

# Load data from MongoDB
data = list(collection.find())

# Convert ObjectId to string for each document
for doc in data:
    doc['_id'] = str(doc['_id'])

df = pd.DataFrame(data)
st.dataframe(df)
