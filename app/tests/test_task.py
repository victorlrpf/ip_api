from app.workers.tasks import tarefa_atualizar_todos_ips


def test_tarefa_atualizar_todos_ips_sucesso(mocker):
    mocker.patch(
        "app.workers.tasks.RepositorioIP.listar_todos_ips",
        return_value=[
            {"ip": "8.8.8.8"},
            {"ip": "1.1.1.1"}
        ]
    )

    mocker.patch(
        "app.workers.tasks.ServicoIPWhois.buscar_dados_ip",
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
        "app.workers.tasks.ServicoIPWhois.mapear_dados_ip",
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

    mock_atualizacao = mocker.patch(
        "app.workers.tasks.RepositorioIP.atualizar_dados_ip"
    )

    resultado = tarefa_atualizar_todos_ips()

    assert resultado["total"] == 2
    assert resultado["atualizados"] == 2
    assert resultado["falhas"] == 0
    assert mock_atualizacao.call_count == 2


def test_tarefa_atualizar_todos_ips_falha_parcial(mocker):
    mocker.patch(
        "app.workers.tasks.RepositorioIP.listar_todos_ips",
        return_value=[
            {"ip": "8.8.8.8"},
            {"ip": "1.1.1.1"}
        ]
    )

    def efeito_colateral_busca(ip):
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
        "app.workers.tasks.ServicoIPWhois.buscar_dados_ip",
        side_effect=efeito_colateral_busca
    )

    mocker.patch(
        "app.workers.tasks.ServicoIPWhois.mapear_dados_ip",
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

    resultado = tarefa_atualizar_todos_ips()

    assert resultado["total"] == 2
    assert resultado["atualizados"] == 1
    assert resultado["falhas"] == 1
