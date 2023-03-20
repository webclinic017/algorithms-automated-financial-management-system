import logging

from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from model.etf import ETF
from model.exceptions.repository_exception import RepositoryException


class ETFRepository:

    def __init__(self):
        self._db_config = dotenv_values(".env")
        self._client = self._connect_to_mongo_db()
        self._collection = self._create_database_unsharded_collection(self._client)

    def _connect_to_mongo_db(self):
        host = self._db_config["MONGO_HOST"]
        port = self._db_config["MONGO_PORT"]
        username = self._db_config["MONGO_USERNAME"]
        password = self._db_config["MONGO_PASSWORD"]

        connection_uri = f"mongodb://{username}:{password}@{host}:{port}"

        client = MongoClient(connection_uri)
        db = client.admin
        server = db.command("serverStatus")
        logging.info("Server status: " + str(server))

        try:
            client.server_info()
        except ServerSelectionTimeoutError:
            raise RepositoryException(
                "Invalid API for MongoDB connection string or timed out when attempting to connect!"
            )

        logging.info("Databases: " + str(client.list_database_names()))
        return client

    def _create_database_unsharded_collection(self, client):
        db_name = self._db_config["MONGO_DB_NAME"]
        unsharded_collection_name = self._db_config["MONGO_COLLECTION_NAME"]
        db = client[db_name]

        if db_name not in client.list_database_names():
            db.command({'customAction': "CreateDatabase", 'offerThroughput': 400})
            logging.info("Created db {} with sharded throughput".format(db_name))

        if unsharded_collection_name not in db.list_collection_names():
            db.create_collection(name=unsharded_collection_name)
            logging.info("Created collection {}".format(unsharded_collection_name))

        return db[unsharded_collection_name]

    def clear_repository_collection(self):
        result = self._collection.delete_many({})

        if result == 0:
            raise RepositoryException("No document was deleted!")

        logging.info("Cleared all documents from repository!")

    def get_all(self):
        all_etfs_json = list(self._collection.find({}))
        all_etfs = []

        for etf in all_etfs_json:
            all_etfs.append(
                ETF(
                    contract_id=etf["contract_id"],
                    symbol=etf["symbol"],
                    full_name=etf["full_name"],
                    price_history=etf["price_history"]
                )
            )

        logging.info(f"Fetched {len(all_etfs)} ETFs!")
        return all_etfs

    def save(self, etf):
        json_etf = {
            "contract_id": etf.get_contract_id(),
            "symbol": etf.get_symbol(),
            "full_name": etf.get_full_name(),
            "price_history": etf.get_price_history()
        }

        self._collection.insert_one(json_etf)
        logging.info(f"Saved data for ETF: {etf.get_symbol()}")
