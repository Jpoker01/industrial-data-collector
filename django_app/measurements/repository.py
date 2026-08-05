"""
Data repository pattern bridging PyMongo and Django REST API views.
"""

import os

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "iot")

COLLECTIONS = {
    "mqtt": "mqtt_measurements",
    "modbus": "modbus_measurements",
}


class MeasurementRepository:
    """For handling MongoDB queries"""

    def __init__(self) -> None:
        self._db = MongoClient(MONGO_URI)[MONGO_DB]

    def list(
        self,
        protocol: str | None = None,
        client_id: str | None = None,
        limit: int = 100,
    ):
        """
        Retrieves recent measurements stored by time

        Args:
            source: Which protocol to use
            client_id: Which client to get measurements from
            limit: Maximum number of documents to return

        Returns:
            List of dictionary measurements for JSON serialization

        """

        # pick collections: one if source given, both otherwise
        names = (
            [COLLECTIONS[protocol]]
            if protocol in COLLECTIONS
            else list(COLLECTIONS.values())
        )
        query = {}
        if client_id:
            query["client_id"] = client_id

        results = []
        for name in names:
            for doc in self._db[name].find(query).sort("received_at", -1).limit(limit):
                doc["_id"] = str(doc["_id"])  # Convert BSON ObjectId to JSON string
                results.append(doc)

        results.sort(key=lambda d: d["received_at"], reverse=True)
        return results[:limit]
