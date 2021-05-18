import datetime

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

def findIds():
    global conn, buckets
    curBucket = conn.bucket(buckets["Claims"])
    ret = []
    for keys in curBucket.stream_keys():
        for key in keys:
            ret.append(int(key))
    return set(ret)

def pullRecord(claimId):
    global conn, buckets
    # Pull claim to pull the rest of the data
    claimBucket = conn.bucket(buckets["Claims"])
    filesBucket = conn.bucket(buckets["Files"])
    customerBucket = conn.bucket(buckets["Customers"])
    claim = claimBucket.get(str(claimId)).data
    claim["created"] = datetime.datetime.strptime(claim["created"], '%Y-%m-%d %H:%M:%S')
    
    files = []
    for file in claim["files"]:
        file = filesBucket.get(str(file)).data
        file["date"] = datetime.datetime.strptime(file["date"], '%Y-%m-%d %H:%M:%S')
        files.append(file)
    customer = customerBucket.get(str(claim["customerId"])).data

    retDoc = {
        "_id": claim["claimId"],
        "customer": customer,
        "claim": claim,
        "files": files,
    }
    return retDoc
