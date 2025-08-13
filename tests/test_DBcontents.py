from pymongo import MongoClient

def dbstats():
    # Include username, password, and authentication database
    client = MongoClient("mongodb://myuser:mypassword@mongo:27017/justinsightdb?authSource=admin")
    db = client["justinsightdb"]
    collection = db["articles"]

    numEntries = collection.count_documents({})
    print("Number of articles:", numEntries)

    entries = collection.find({})
    
    totalcount = 0
    min = -1
    max = -1
    for row in entries:
        wordcount = len(row["full_text"].split())
        totalcount = totalcount + wordcount
        if wordcount < min or min == -1:
            min = wordcount
        if wordcount > max:
            max = wordcount

    print("The average word count per article is: ", totalcount/numEntries)
    print("The max word count is: ", max)
    print("The min word count is: ", min)


if __name__ == '__main__':
    dbstats()