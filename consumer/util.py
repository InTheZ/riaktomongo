import datetime

def parseDocument(doc):
    files = []
    for i in doc["files"]:
        files.append({
            "date": datetime.datetime.strptime(i["date"], "%m/%d/%Y %I:%M %p"),
            "name": i["name"],
            "fileId": i["fileId"],
            "description": i["description"]
        })
    
    newDoc = {
            "customer": {
                "customerId": doc["customer"]["customerId"],
                "name": doc["customer"]["name"],
                "address": doc["customer"]["address"],
                "city": doc["customer"]["city"],
                "state": doc["customer"]["state"],
                "zip": doc["customer"]["zip"]
        },
        "files": files,
        "claim": {
            "created": datetime.datetime.strptime(doc["claim"]["created"], "%Y-%m-%d %H:%M:%S"),
            "claimId": doc["claim"]["claimId"],
            "policyId": doc["claim"]["policyId"],
            "status": doc["claim"]["status"],
            "agentId": doc["claim"]["agentId"],
            "cost": doc["claim"]["cost"],
            "accepted": doc["claim"]["accepted"],
        }
    }
    return newDoc