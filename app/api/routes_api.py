from fastapi import APIRouter, Depends, Query
from app.core.seguranca import verify_token
from app.schemas.requesicao_ip import IPRequest
from app.services.ip_service import IPService

router = APIRouter(prefix="/ips", tags=["IPs"])
service = IPService()


@router.post("", dependencies=[Depends(verify_token)])
def create_ip(payload: IPRequest):
    return service.create_or_get_ip(payload.ip)


@router.get("", dependencies=[Depends(verify_token)])
def get_ips(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=15, ge=1, le=15),
    filter_ip: str | None = Query(default=None)
):
    return service.list_ips(page=page, limit=limit, filter_ip=filter_ip)
