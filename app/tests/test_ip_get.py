def test_get_ips_returns_paginated_list(client, auth_headers, mocker):
    mocker.patch(
        "app.services.ip_service.IPRepository.list_ips",
        return_value=[
            {
                "ip": "8.8.8.8",
                "data": {
                    "type": "IPv4",
                    "continent": "North America",
                    "continent_code": "NA",
                    "country": "United States",
                    "country_code": "US",
                    "region": "California",
                    "region_code": "CA",
                    "city": "Mountain View",
                    "capital": "Washington D.C."
                }
            }
        ]
    )

    response = client.get("/ips?page=1&limit=10", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert "ips" in body
    assert len(body["ips"]) == 1
    assert body["ips"][0]["ip"] == "8.8.8.8"


def test_get_ips_with_filter(client, auth_headers, mocker):
    mocker.patch(
        "app.services.ip_service.IPRepository.list_ips",
        return_value=[
            {
                "ip": "192.168.0.1",
                "data": {
                    "type": "IPv4",
                    "continent": "South America",
                    "continent_code": "SA",
                    "country": "Brazil",
                    "country_code": "BR",
                    "region": "São Paulo",
                    "region_code": "SP",
                    "city": "Americana",
                    "capital": "Brasília"
                }
            }
        ]
    )

    response = client.get("/ips?filter_ip=192", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert len(body["ips"]) == 1
    assert body["ips"][0]["ip"].startswith("192")


def test_get_ips_with_invalid_limit_returns_422(client, auth_headers):
    response = client.get("/ips?limit=20", headers=auth_headers)
    assert response.status_code == 422
