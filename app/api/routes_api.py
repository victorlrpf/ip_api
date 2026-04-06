from fastapi import APIRouter, Depends

from app.core.seguranca import verify_token
from app.schemas.requesicao_ip import IPRequest
from app.services.ip_service import IPService

router = APIRouter(prefix="/ips", tags=["IPs"])
service = IPService()


@router.post("", dependencies=[Depends(verify_token)])
def create_ip(payload: IPRequest):
    return service.create_or_get_ip(payload.ip)