from riak import RiakClient

conn = None
buckets = None
def createConnection(config):
    global conn, buckets
    conn =  RiakClient(protocol='http', host=config["RiakDB"]["Host"], http_port=config["RiakDB"]["Port"])
    buckets = {
        "Customers": config["RiakDB"]["Customers"],
        "Files": config["RiakDB"]["Files"],
        "Claims": config["RiakDB"]["Claims"],
    }


def close():
    return

def clearDB():
    global conn, buckets
    for bucket in buckets.keys():
        curBucket = conn.bucket(buckets[bucket])
        for keys in curBucket.stream_keys():
            for key in keys:
                curBucket.delete(key)

def insertClaim(claim):
    global conn, buckets
    curBucket = conn.bucket(buckets["Claims"])
    claim["created"] = claim["created"].strftime("%Y-%m-%d %H:%M:%S")
    key = curBucket.new(str(claim["claimId"]), data=claim)
    key.store()

def insertFile(file):
    global conn, buckets
    curBucket = conn.bucket(buckets["Files"])
    file["date"] = file["date"].strftime("%Y-%m-%d %H:%M:%S")
    key = curBucket.new(str(file["fileId"]), data=file)
    key.store()

def insertCustomer(customer):
    global conn, buckets
    curBucket = conn.bucket(buckets["Customers"])
    key = curBucket.new(str(customer["customerId"]), data=customer)
    key.store()

def insertDoc(doc):
    global conn, buckets

    # Insert customer
    insertCustomer(doc["customer"])

    # Insert files
    files = doc["files"]
    for file in files:
        insertFile(file)
    
    # Insert claim as master record
    claim = doc["claim"]
    claim["customerId"] = doc["customer"]["customerId"]

    fileIds = []
    for file in doc["files"]:
        fileIds.append(file["fileId"])
    claim["files"] = fileIds
    insertClaim(claim)
