import os
import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.set_page_config(layout="wide")

# Include username, password, and authentication database
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

columns_to_show = st.multiselect("Columns to display", options=df.columns.tolist(), default=df.columns.tolist())
st.dataframe(df[columns_to_show])#, use_container_width=True)

# for i, row in df[columns_to_show].iterrows():
#     st.markdown(f"### Entry {i+1}")
#     st.write(row.to_dict())



