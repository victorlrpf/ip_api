from pydantic import BaseModel
from typing import List, Optional


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


class IPItemResponse(BaseModel):
    ip: str
    data: IPDataResponse


class IPListResponse(BaseModel):
    ips: List[IPItemResponse]