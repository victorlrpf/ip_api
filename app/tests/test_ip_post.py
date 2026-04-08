def test_post_ips_returns_existing_ip(client, auth_headers, mocker):
    existing_ip = {
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

    mocker.patch(
        "app.services.ip_service.IPRepository.encontrar_ip",
        return_value=existing_ip
    )

    response = client.post(
        "/ips",
        json={"ip": "8.8.8.8"},
        headers=auth_headers
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ip"] == "8.8.8.8"
    assert body["data"]["country"] == "United States"


def test_post_ips_fetches_and_saves_when_ip_not_exists(client, auth_headers, mocker):
    mocker.patch(
        "app.services.ip_service.IPRepository.encontrar_ip",
        side_effect=[None, {
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
        }]
    )

    raw_data = {
        "ip": "8.8.8.8",
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

    mapped_data = {
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

    create_mock = mocker.patch(
        "app.services.ip_service.IPRepository.create",
        return_value={
            "ip": "8.8.8.8",
            "data": mapped_data
        }
    )

    mocker.patch(
        "app.services.ip_service.IPWhoisService.fetch_ip_data",
        return_value=raw_data
    )

    mocker.patch(
        "app.services.ip_service.IPWhoisService.map_ip_data",
        return_value=mapped_data
    )

    response = client.post(
        "/ips",
        json={"ip": "8.8.8.8"},
        headers=auth_headers
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ip"] == "8.8.8.8"
    assert body["data"]["country"] == "United States"
    assert create_mock.called


def test_post_ips_with_invalid_ip_returns_422(client, auth_headers):
    response = client.post(
        "/ips",
        json={"ip": "ip-invalido"},
        headers=auth_headers
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "IP inválido."