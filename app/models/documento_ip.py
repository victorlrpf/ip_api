from datetime import datetime


def construcao_doc(ip: str, raw_data: dict | None = None, data: dict | None = None) -> dict:
    now = datetime.utcnow()
    return {
        "ip": ip,
        "raw_data": raw_data or {},
        "data": data or {},
        "created_at": now,
        "updated_at": now,
        "last_sync_at": now,
    }