from fastapi import HTTPException, status

from app.models.documento_ip import construcao_doc
from app.repositories.repository_ip import RepositorioIP
from app.services.ipwhois_service import ServicoIPWhois
from app.Utilidades.validador import validar_ip, validar_filtro_ip


class ServicoIP:
    def __init__(self):
        self.repositorio = RepositorioIP()
        self.servico_ipwhois = ServicoIPWhois()

    def criar_ou_obter_ip(self, ip: str):
        try:
            ip_normalizado = validar_ip(ip)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc)
            ) from exc

        existente = self.repositorio.encontrar_ip(ip_normalizado)
        if existente:
            return {
                "ip": existente["ip"],
                "data": existente.get("data", {})
            }

        dados_brutos = self.servico_ipwhois.buscar_dados_ip(ip_normalizado)
        dados_mapeados = self.servico_ipwhois.mapear_dados_ip(dados_brutos)

        documento = construcao_doc(
            ip=ip_normalizado,
            raw_data=dados_brutos,
            data=dados_mapeados
        )

        salvo = self.repositorio.criar(documento)

        return {
            "ip": salvo["ip"],
            "data": salvo.get("data", {})
        }

    def listar_ips(self, pagina: int = 1, limite: int = 15, filtro_ip: str | None = None):
        if pagina < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="pagina deve ser maior ou igual a 1."
            )

        if limite < 1 or limite > 15:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="limite deve estar entre 1 e 15."
            )

        try:
            if filtro_ip:
                validar_filtro_ip(filtro_ip)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc)
            ) from exc

        itens = self.repositorio.listar_ips(pagina=pagina, limite=limite, filtro_ip=filtro_ip)

        return {
            "ips": itens
        }
