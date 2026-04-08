from celery.utils.log import get_task_logger

from app.repositories.repository_ip import RepositorioIP
from app.services.ipwhois_service import ServicoIPWhois
from app.workers.celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task(name="app.workers.tasks.tarefa_atualizar_todos_ips")
def tarefa_atualizar_todos_ips():
    repositorio = RepositorioIP()
    servico_ipwhois = ServicoIPWhois()

    ips = repositorio.listar_todos_ips()

    total = len(ips)
    atualizados = 0
    falhas = 0

    logger.info("Iniciando atualização periódica de %s IPs.", total)

    for item in ips:
        ip = item["ip"]

        try:
            dados_brutos = servico_ipwhois.buscar_dados_ip(ip)
            dados_mapeados = servico_ipwhois.mapear_dados_ip(dados_brutos)

            repositorio.atualizar_dados_ip(
                ip=ip,
                dados_brutos=dados_brutos,
                dados=dados_mapeados
            )

            atualizados += 1
            logger.info("IP %s atualizado com sucesso.", ip)

        except Exception as exc:
            falhas += 1
            logger.exception("Falha ao atualizar IP %s: %s", ip, exc)

    resultado = {
        "total": total,
        "atualizados": atualizados,
        "falhas": falhas,
    }

    logger.info("Atualização periódica finalizada: %s", resultado)
    return resultado
