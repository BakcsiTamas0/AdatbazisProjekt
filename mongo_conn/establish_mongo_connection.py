import pymongo

def establish_mongo_database_connection(ip, port_str):
    port = int(port_str)
    client = pymongo.MongoClient(ip, port)
    return client

def get_collection_contents(client, database_name, collection_name):
    db = client[database_name]
    collection = db[collection_name]
    documents = collection.find()
    return documents

def insert_into_manufacturer_mongo(id, manufacturer_name, ip, port, database_name, collection_name):
    client = establish_mongo_database_connection(ip, port)
    db = client[database_name]
    collection = db[collection_name]
    collection.insert_one({"id": id, "manufacturer_name": manufacturer_name})

def update_manufacturer_mongo(manufacturer_id, manufacturer_name, product_name, category, price, ip, port, database_name, collection_name):
    client = establish_mongo_database_connection(ip, port)
    db = client[database_name]
    collection = db[collection_name]

    update_query = {
        "id": manufacturer_id,
        "manufacturer_name": manufacturer_name
    }

    update_data = {
        "$set": {
            "id": manufacturer_id,
            "manufacturer_name": manufacturer_name
        },
        "$push": {
            "products": {
                "name": product_name,
                "category": category,
                "price": price
            }
        }
    }

    collection.update_one(update_query, update_data, upsert=True)
