import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# Read the text file
file_path = "./temp.txt"  # Assuming the file is named "temp.txt" and located in the same folder
with open(file_path, "r") as file:
    text_content = file.read()

# Create a document to store in MongoDB
document = {"text": text_content}

# Insert the document into the collection
collection.insert_one(document)

print("Text content stored in MongoDB successfully.")
