from pymongo import MongoClient

conn = None
database = None
collection = None
def createConnection(config):
    global conn, database, collection
    conn = MongoClient(config["Mongo"]["MongoURI"])
    database = config["Mongo"]["Database"]
    collection = config["Mongo"]["Collection"]

def close():
    global conn
    conn.close()

def insertDoc(doc):
    global conn, database, collection
    # Insert document into collection
    doc["_id"] = doc["claim"]["claimId"]
    conn[database][collection].insert_one(doc)

def clearDB():
    global conn, database
    conn.drop_database(database)
