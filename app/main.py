from fastapi import FastAPI

from app.api.routes_api import router as ips_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(ips_router)