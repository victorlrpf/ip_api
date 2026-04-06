from pydantic import BaseModel
from typing import Optional


class IPDataResponse(BaseModel):
    type: Optional[str] = None
    continent: Optional[str] = None
    continent_code: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    region: Optional[str] = None
    region_code: Optional[str] = None
    city: Optional[str] = None
    capital: Optional[str] = None


class IPResponse(BaseModel):
    ip: str
    data: Optional[IPDataResponse] = None
    message: Optional[str] = None