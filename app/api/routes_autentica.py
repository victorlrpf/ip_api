from fastapi import APIRouter, HTTPException, status
from app.core.seguranca import criar_token_acesso
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Autenticação"])

class RequisicaoLogin(BaseModel):
    token: str

@router.post("/login")
def login(payload: RequisicaoLogin):
    if payload.token != settings.app_token:
        raise HTTPException(status_code=401, detail="Token mestre inválido")

    token_acesso = criar_token_acesso(dados={"sub": "admin"})
    return {"access_token": token_acesso, "token_type": "bearer"}
