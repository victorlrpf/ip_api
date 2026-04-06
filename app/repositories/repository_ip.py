from app.core.database import get_ips_collection


class IPRepository:
    def __init__(self):
        self.collection = get_ips_collection()

    def encontrar_ip(self, ip: str):
        return self.collection.find_one({"ip": ip}, {"_id": 0})

    def create(self, document: dict):
        self.collection.insert_one(document)
        return self.encontrar_ip(document["ip"])