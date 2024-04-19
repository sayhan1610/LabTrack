from pymongo import MongoClient

uri = "mongodb+srv://admin:admin@cluster0.zlujgzq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client.get_database("item_db")

collection_name = db["item_collection"]