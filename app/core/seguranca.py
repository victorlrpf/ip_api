from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import settings

security = HTTPBearer(auto_error=True)

def criar_token_acesso(dados: dict):
    para_codificar = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=settings.token_expiration)
    para_codificar.update({"exp": expiracao})
    return jwt.encode(para_codificar, settings.chave_secreta, algorithm=settings.algoritmo)

def verificar_token(credenciais: HTTPAuthorizationCredentials = Depends(security)):
    token = credenciais.credentials

    if token == settings.app_token:
        return {"user": "admin", "type": "static"}

    try:
        payload = jwt.decode(token, settings.chave_secreta, algorithms=[settings.algoritmo])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )
