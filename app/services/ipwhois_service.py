import httpx
from fastapi import HTTPException, status

from app.core.config import settings


class IPWhoisService:
    def __init__(self):
        self.base_url = settings.ipwhois_base_url.rstrip("/")

    def fetch_ip_data(self, ip: str) -> dict:
        url = f"{self.base_url}/{ip}"

        try:
            response = httpx.get(
                url,
                timeout=10.0,
                follow_redirects=True,
            )
        except httpx.TimeoutException as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Timeout ao consultar serviço externo."
            ) from exc
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Falha de comunicação com serviço externo."
            ) from exc

        if response.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Erro ao consultar serviço externo: {response.status_code} | URL: {url} | body: {response.text}"
            )

        data = response.json()

        # A documentação informa que alguns erros podem vir com HTTP 200
        # e success=false no corpo.
        if data.get("success") is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=data.get("message", "Erro retornado pela API externa.")
            )

        return data

    def map_ip_data(self, raw_data: dict) -> dict:
        return {
            "type": raw_data.get("type"),
            "continent": raw_data.get("continent"),
            "continent_code": raw_data.get("continent_code"),
            "country": raw_data.get("country"),
            "country_code": raw_data.get("country_code"),
            "region": raw_data.get("region"),
            "region_code": raw_data.get("region_code"),
            "city": raw_data.get("city"),
            "capital": raw_data.get("capital"),
        }