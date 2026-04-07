from celery.utils.log import get_task_logger

from app.repositories.repository_ip import IPRepository
from app.services.ipwhois_service import IPWhoisService
from app.workers.celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task(name="app.workers.tasks.refresh_all_ips_task")
def refresh_all_ips_task():
    repository = IPRepository()
    ipwhois_service = IPWhoisService()

    ips = repository.list_all_ips()

    total = len(ips)
    updated = 0
    failed = 0

    logger.info("Iniciando atualização periódica de %s IPs.", total)

    for item in ips:
        ip = item["ip"]

        try:
            raw_data = ipwhois_service.fetch_ip_data(ip)
            mapped_data = ipwhois_service.map_ip_data(raw_data)

            repository.update_ip_data(
                ip=ip,
                raw_data=raw_data,
                data=mapped_data
            )

            updated += 1
            logger.info("IP %s atualizado com sucesso.", ip)

        except Exception as exc:
            failed += 1
            logger.exception("Falha ao atualizar IP %s: %s", ip, exc)

    result = {
        "total": total,
        "updated": updated,
        "failed": failed,
    }

    logger.info("Atualização periódica finalizada: %s", result)
    return result