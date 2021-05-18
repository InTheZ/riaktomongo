import configparser
from signal import signal, SIGINT
from sys import exit

import util, mongo, riakdb

DEFAULT_CONFIG = "etl.conf"

def startup():
    # Read configuration
    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG)

    # Create necessary database connections to use
    riakdb.createConnection(config)
    mongo.createConnection(config)

def shutdown():
    # Create necessary database connections to use
    riakdb.close()
    mongo.close()

def etlMain():
    # Find missing keys from RiakDB
    mongoIds = mongo.findIds()
    riakIds = riakdb.findIds()
    missing = riakIds - mongoIds
    print("Missing items: " + str(len(missing)))

    # Pull missing keys from Riak and insert into Mongo
    transferedDocs = 0
    missingCount = len(missing)
    for item in missing:
        doc = riakdb.pullRecord(item)
        try:
            mongo.insertDoc(doc)
        except:
            pass
        transferedDocs += 1
        util.printProgressBar(transferedDocs, missingCount)


def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    shutdown()
    exit(0)

if __name__ == "__main__":
    signal(SIGINT, handler)
    startup()
    etlMain()
    shutdown()
    print("Finished ETL Job!")