from app.workers.tasks import refresh_all_ips_task


def test_refresh_all_ips_task_success(mocker):
    mocker.patch(
        "app.workers.tasks.IPRepository.list_all_ips",
        return_value=[
            {"ip": "8.8.8.8"},
            {"ip": "1.1.1.1"}
        ]
    )

    mocker.patch(
        "app.workers.tasks.IPWhoisService.fetch_ip_data",
        side_effect=[
            {
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
            },
            {
                "ip": "1.1.1.1",
                "type": "IPv4",
                "continent": "Oceania",
                "continent_code": "OC",
                "country": "Australia",
                "country_code": "AU",
                "region": "Queensland",
                "region_code": "QLD",
                "city": "South Brisbane",
                "capital": "Canberra"
            }
        ]
    )

    mocker.patch(
        "app.workers.tasks.IPWhoisService.map_ip_data",
        side_effect=[
            {
                "type": "IPv4",
                "continent": "North America",
                "continent_code": "NA",
                "country": "United States",
                "country_code": "US",
                "region": "California",
                "region_code": "CA",
                "city": "Mountain View",
                "capital": "Washington D.C."
            },
            {
                "type": "IPv4",
                "continent": "Oceania",
                "continent_code": "OC",
                "country": "Australia",
                "country_code": "AU",
                "region": "Queensland",
                "region_code": "QLD",
                "city": "South Brisbane",
                "capital": "Canberra"
            }
        ]
    )

    update_mock = mocker.patch(
        "app.workers.tasks.IPRepository.update_ip_data"
    )

    result = refresh_all_ips_task()

    assert result["total"] == 2
    assert result["updated"] == 2
    assert result["failed"] == 0
    assert update_mock.call_count == 2


def test_refresh_all_ips_task_partial_failure(mocker):
    mocker.patch(
        "app.workers.tasks.IPRepository.list_all_ips",
        return_value=[
            {"ip": "8.8.8.8"},
            {"ip": "1.1.1.1"}
        ]
    )

    def fetch_side_effect(ip):
        if ip == "8.8.8.8":
            return {
                "ip": ip,
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
        raise Exception("Falha simulada")

    mocker.patch(
        "app.workers.tasks.IPWhoisService.fetch_ip_data",
        side_effect=fetch_side_effect
    )

    mocker.patch(
        "app.workers.tasks.IPWhoisService.map_ip_data",
        return_value={
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
    )

    result = refresh_all_ips_task()

    assert result["total"] == 2
    assert result["updated"] == 1
    assert result["failed"] == 1