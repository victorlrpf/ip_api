from pydantic import BaseModel, Field


class IPRequest(BaseModel):
    ip: str = Field(..., description="Número do IP a ser buscado e salvo.")