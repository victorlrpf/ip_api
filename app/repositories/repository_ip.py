from app.core.database import get_ips_collection
from datetime import datetime


class RepositorioIP:
    def __init__(self):
        self.colecao = get_ips_collection()

    def encontrar_ip(self, ip: str):
        return self.colecao.find_one({"ip": ip}, {"_id": 0})

    def criar(self, documento: dict):
        self.colecao.insert_one(documento)
        return self.encontrar_ip(documento["ip"])

    def listar_ips(self, pagina: int = 1, limite: int = 15, filtro_ip: str | None = None):
        consulta = {}

        if filtro_ip:
            consulta["ip"] = {"$regex": f"^{filtro_ip}"}

        pular = (pagina - 1) * limite

        cursor = (
            self.colecao
            .find(consulta, {"_id": 0, "ip": 1, "data": 1})
            .sort("ip", 1)
            .skip(pular)
            .limit(limite)
        )

        return list(cursor)

    def listar_todos_ips(self):
        cursor = self.colecao.find({}, {"_id": 0, "ip": 1})
        return list(cursor)

    def atualizar_dados_ip(self, ip: str, dados_brutos: dict, dados: dict):
        agora = datetime.utcnow()

        self.colecao.update_one(
            {"ip": ip},
            {
                "$set": {
                    "raw_data": dados_brutos,
                    "data": dados,
                    "updated_at": agora,
                    "last_sync_at": agora,
                }
            }
        )

        return self.encontrar_ip(ip)
