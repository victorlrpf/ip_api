from fastapi import HTTPException, status

from app.models.documento_ip import construcao_doc
from app.repositories.repository_ip import IPRepository
from app.utils.validador import validate_ip


class IPService:
    def __init__(self):
        self.repository = IPRepository()

    def create_or_get_ip(self, ip: str):
        try:
            normalized_ip = validate_ip(ip)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc)
            ) from exc

        existing = self.repository.encontrar_ip(normalized_ip)
        if existing:
            return {
                "ip": existing["ip"],
                "data": existing.get("data", {}),
                "message": "IP já cadastrado. Retornando dados persistidos."
            }

        # Sprint 1: ainda sem integração com ipwhois
        document = construcao_doc(
            ip=normalized_ip,
            raw_data={},
            data={}
        )

        saved = self.repository.create(document)

        return {
            "ip": saved["ip"],
            "data": saved.get("data", {}),
            "message": "IP salvo com sucesso. Integração externa será adicionada na próxima sprint."
        }