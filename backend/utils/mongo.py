import os
import pymongo
import sys
from dotenv import load_dotenv
import uuid
import flask

app = flask.Flask(__name__)

load_dotenv()

# Fetch environment variables
db_password = os.getenv("DB_PASSWORD")

try:
    client = pymongo.MongoClient(f"mongodb+srv://mahesha:{db_password}@cluster0.4xv3s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

db = client.inventory

@app.route("/add_food/<collection: str>/<item_name: str>/<quantity: int>/<unit: str>/<expiryDate: str>",methods=['POST'])
def insert_food(collection, item_name, quantity, unit, expiryDate):
    db_collection = db[collection]
    db_collection.insert_one({"name": item_name, "quantity": quantity, "unit": unit, "expiryDate": expiryDate})


# @app.route("/count/<collection: str>/<name: str>",methods=['GET'])
def get_count(collection, item_name):
    results = db[collection].find({"name": item_name})
    amount = 0
    for result in results:
        amount += result["quantity"]
    # print(amount)
    return amount

@app.route("/delete/<collection: str>/<item_name: str>/<amount: int>",methods=['POST'])
def delete_food(collection, item_name, amount): #amount = 4
    foods = db[collection].find({"name": item_name}).sort({"expiryDate": 1}).to_list()
    total = 0 # 8
    for food in foods:
        total += food["quantity"]
    removed = 0
    i = 0
    while removed < amount and i < len(foods):
        food = foods[i]
        if food["quantity"] <= amount - removed:
            db[collection].delete_one({"_id": food["_id"]})
            removed += food["quantity"]
            i += 1
        else:
            db[collection].update_one({"_id": food["_id"]}, {"$set": {"quantity": food["quantity"] - (amount - removed)}})
            removed = amount

@app.route("/inventory",methods=['GET'])
def get_inventory():
    collections = db.list_collection_names()
    all_documents = []
    visited = set()
    for collection_name in collections:
        collection = db[collection_name]
        documents = collection.find()
        for document in documents:
            if document["name"] not in visited:
                all_documents.append({"name": document["name"], "quantity": get_count(collection_name, document["name"]), "unit": document["unit"]})
                visited.add(document["name"])
    # print(all_documents)
    return all_documents
    



            

# insert_food("fridge", "eggs", 8, None, "01/10/2024")
# insert_food("fridge", "eggs", 16, None, "01/12/2024")
# get_count("fridge", "eggs")
# insert_food("fridge", "milk", 3, "oz", "03/10/2024")
# insert_food("pantry", "bananas", 4, None, "04/10/2024")
# delete_food("pantry", "bananas", 2)
# delete_food("fridge", "milk", 3)
# delete_food("fridge", "eggs", 20)
# delete_food("fridge", "milk", 3)
# delete_food("pantry", "bananas", 4)
get_inventory()