import configparser
import datetime
import json
from util import randomChoice
import requests
import time

import util

QUEUE = []
DEFAULT_CONFIG = "producer.conf"

genIds = {
    "customer": [],
    "file": [],
    "claim": []
}
def genId(type, length):
    global genIds
    genId = util.randomInt(length)
    while genId in genIds[type]:
        genId = util.randomInt(length)
    genIds[type].append(genId)
    return genId

def genData():
    files = []
    for i in range(0,util.randomInt(2)):
        files.append({
            "date": util.randomDate(afterDate="03/01/2020 8:00 AM",toDate="05/15/2021 05:00 PM"),
            "name": util.randomString(util.randomInt(2)),
            "fileId": genId("file", 16),
            "description": util.randomString(util.randomInt(3))
        })
    cost = round(util.randomMoney(min=100.00, max=1000000.00), 2)
    return {
        "customer": {
            "customerId": genId("customer", 12),
            "name": util.generateName(),
            "address": util.randomStreetAddress(),
            "city": util.randomCity(),
            "state": util.randomState(),
            "zip": util.randomZipCode()
        },
        "files": files,
        "claim": {
            "claimId": genId("claim", 16),
            "policyId": util.randomInt(12),
            "status": util.randomChoice(["New", "Submitted", "In Progress", "Accepted", "Declined"]),
            "agentId": util.randomInt(8),
            "cost": cost,
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accepted": round(util.randomMoney(min=100.00, max=cost), 2)
        }
    }

def produceData(conf):
    endpoint = conf["GENERAL"]["Endpoint"]
    interval = int(conf["GENERAL"]["Interval"])
    batch = int(conf["GENERAL"]["Batch"])
    while True:
        for i in range(0,batch):
            QUEUE.append(genData())
        error = False
        while len(QUEUE)>0 and not error:
            item = QUEUE.pop()
            try:
                requests.post(endpoint, data=json.dumps(item), headers={"Content-Type": "application/json"})
            except Exception as e:
                # Issue connecting to server, put this item back in the queue
                QUEUE.append(item)
                error = True
                pass
        
        # Wait the interval until we try again
        print("Current Queue Length: " + str(len(QUEUE)))
        time.sleep(interval)

def main():
    # Read configuration
    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG)
    produceData(config)

if __name__ == "__main__":
    main()