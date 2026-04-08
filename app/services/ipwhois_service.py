import httpx
from fastapi import HTTPException, status

from app.core.config import settings


class ServicoIPWhois:
    def __init__(self):
        self.url_base = settings.ipwhois_base_url.rstrip("/")

    def buscar_dados_ip(self, ip: str) -> dict:
        url = f"{self.url_base}/{ip}"

        try:
            resposta = httpx.get(
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

        if resposta.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Erro ao consultar serviço externo: {resposta.status_code} | URL: {url} | corpo: {resposta.text}"
            )

        dados = resposta.json()

        # A documentação informa que alguns erros podem vir com HTTP 200
        # e success=false no corpo.
        if dados.get("success") is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=dados.get("message", "Erro retornado pela API externa.")
            )

        return dados

    def mapear_dados_ip(self, dados_brutos: dict) -> dict:
        return {
            "type": dados_brutos.get("type"),
            "continent": dados_brutos.get("continent"),
            "continent_code": dados_brutos.get("continent_code"),
            "country": dados_brutos.get("country"),
            "country_code": dados_brutos.get("country_code"),
            "region": dados_brutos.get("region"),
            "region_code": dados_brutos.get("region_code"),
            "city": dados_brutos.get("city"),
            "capital": dados_brutos.get("capital"),
        }
