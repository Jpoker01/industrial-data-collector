import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "iot")

COLLECTIONS = {
    "mqtt": "mqtt_measurements",
    "modbus": "modbus_measurements",
}


class MeasurementRepository:
    def __init__(self):
        self._db = MongoClient(MONGO_URI)[MONGO_DB]

    def list(self, source=None, client_id=None, limit=100):
        # pick collections: one if source given, both otherwise
        names = [COLLECTIONS[source]] if source in COLLECTIONS else list(COLLECTIONS.values())

        query = {}
        if client_id:
            query["client_id"] = client_id

        results = []
        for name in names:
            for doc in self._db[name].find(query).sort("received_at", -1).limit(limit):
                doc["_id"] = str(doc["_id"])          # ObjectId -> string for JSON
                results.append(doc)

        results.sort(key=lambda d: d["received_at"], reverse=True)
        return results[:limit]