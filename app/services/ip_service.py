from fastapi import HTTPException, status

from app.models.documento_ip import construcao_doc
from app.repositories.repository_ip import IPRepository
from app.services.ipwhois_service import IPWhoisService
from app.utils.validador import validate_ip, validate_filter_ip


class IPService:
    def __init__(self):
        self.repository = IPRepository()
        self.ipwhois_service = IPWhoisService()

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
                "data": existing.get("data", {})
            }

        raw_data = self.ipwhois_service.fetch_ip_data(normalized_ip)
        mapped_data = self.ipwhois_service.map_ip_data(raw_data)

        document = construcao_doc(
            ip=normalized_ip,
            raw_data=raw_data,
            data=mapped_data
        )

        saved = self.repository.create(document)

        return {
            "ip": saved["ip"],
            "data": saved.get("data", {})
        }

    def list_ips(self, page: int = 1, limit: int = 15, filter_ip: str | None = None):
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="page deve ser maior ou igual a 1."
            )

        if limit < 1 or limit > 15:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="limit deve estar entre 1 e 15."
            )

        try:
            if filter_ip:
                validate_filter_ip(filter_ip)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc)
            ) from exc

        items = self.repository.list_ips(page=page, limit=limit, filter_ip=filter_ip)

        return {
            "ips": items
        }
