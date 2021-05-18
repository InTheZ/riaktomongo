import pymongo

conn = None
database = None
collection = None

def createConnection(config):
    global conn, database, collection
    conn = pymongo.MongoClient(config["Mongo"]["MongoURI"])
    collection = config["Mongo"]["Collection"]
    database = config["Mongo"]["Database"]

def close():
    global conn
    conn.close()

def findIds():
    global conn, database, collection
    res = list(conn[database][collection].find({}, {"_id": 1}))
    ret = []
    for item in res:
        ret.append(item["_id"])
    return set(ret)

def insertDoc(doc):
    global conn, database, collection
    # Insert document into collection
    conn[database][collection].insert_one(doc)
