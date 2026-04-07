from app.core.database import get_ips_collection


class IPRepository:
    def __init__(self):
        self.collection = get_ips_collection()

    def encontrar_ip(self, ip: str):
        return self.collection.find_one({"ip": ip}, {"_id": 0})

    def create(self, document: dict):
        self.collection.insert_one(document)
        return self.encontrar_ip(document["ip"])

    def list_ips(self, page: int = 1, limit: int = 15, filter_ip: str | None = None):
        query = {}

        if filter_ip:
            query["ip"] = {"$regex": f"^{filter_ip}"}

        skip = (page - 1) * limit

        cursor = (
            self.collection
            .find(query, {"_id": 0, "ip": 1, "data": 1})
            .sort("ip", 1)
            .skip(skip)
            .limit(limit)
        )

        return list(cursor)
