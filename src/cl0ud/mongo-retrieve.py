import pymongo
import os

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# Retrieve the document from MongoDB
document = collection.find_one()

if document:
    # Get the text content from the document
    text_content = document["text"]

    # Delete existing "retrieve.txt" file if present
    if os.path.exists("retrieve.txt"):
        os.remove("retrieve.txt")

    # Save the text content to "retrieve.txt" file
    with open("retrieve.txt", "w") as file:
        file.write(text_content)

    print("Text content retrieved from MongoDB and stored in retrieve.txt.")
else:
    print("No document found in MongoDB.")
