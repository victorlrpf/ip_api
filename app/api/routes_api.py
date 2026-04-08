from fastapi import APIRouter, Depends, Query
from app.core.seguranca import verificar_token
from app.schemas.requesicao_ip import IPRequest
from app.services.ip_service import ServicoIP
from app.workers.tasks import tarefa_atualizar_todos_ips

router = APIRouter(prefix="/ips", tags=["IPs"])
servico = ServicoIP()

@router.post("", dependencies=[Depends(verificar_token)])
def criar_ip(payload: IPRequest):
    return servico.criar_ou_obter_ip(payload.ip)

@router.get("", dependencies=[Depends(verificar_token)])
def listar_ips(
    pagina: int = Query(default=1, ge=1),
    limite: int = Query(default=15, ge=1, le=15),
    filtro_ip: str | None = Query(default=None)
):
    return servico.listar_ips(pagina=pagina, limite=limite, filtro_ip=filtro_ip)

@router.post("/refresh", dependencies=[Depends(verificar_token)])
def atualizar_ips_manualmente():
    tarefa = tarefa_atualizar_todos_ips.delay()
    return {
        "message": "Atualização enfileirada com sucesso.",
        "task_id": tarefa.id
    }
