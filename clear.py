from consumer import riakdb, mongo

import configparser

DEFAULT_CONFIG = "consumer/consumer.conf"

if __name__ == "__main__":
    # Read configuration
    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG)

    # Create necessary database connections to use
    riakdb.createConnection(config)
    mongo.createConnection(config)

    riakdb.clearDB()
    mongo.clearDB()

    riakdb.close()
    mongo.close()