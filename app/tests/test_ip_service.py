import pytest
from fastapi import HTTPException

from app.services.ip_service import IPService


def test_list_ips_invalid_page():
    service = IPService()

    with pytest.raises(HTTPException) as exc:
        service.list_ips(page=0, limit=10)

    assert exc.value.status_code == 400


def test_list_ips_invalid_filter(mocker):
    service = IPService()

    with pytest.raises(HTTPException) as exc:
        service.list_ips(page=1, limit=10, filter_ip="x")

    assert exc.value.status_code == 400


def test_create_or_get_ip_returns_existing_ip(mocker):
    service = IPService()

    mocker.patch.object(
        service.repository,
        "find_by_ip",
        return_value={
            "ip": "8.8.8.8",
            "data": {"country": "United States"}
        }
    )

    result = service.create_or_get_ip("8.8.8.8")

    assert result["ip"] == "8.8.8.8"
    assert result["data"]["country"] == "United States"