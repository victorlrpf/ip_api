import pytest
from fastapi import HTTPException

from app.services.ip_service import ServicoIP


def test_listar_ips_pagina_invalida():
    servico = ServicoIP()

    with pytest.raises(HTTPException) as exc:
        servico.listar_ips(pagina=0, limite=10)

    assert exc.value.status_code == 400


def test_listar_ips_filtro_invalido(mocker):
    servico = ServicoIP()

    with pytest.raises(HTTPException) as exc:
        servico.listar_ips(pagina=1, limite=10, filtro_ip="x")

    assert exc.value.status_code == 400


def test_criar_ou_obter_ip_retorna_ip_existente(mocker):
    servico = ServicoIP()

    mocker.patch.object(
        servico.repositorio,
        "encontrar_ip",
        return_value={
            "ip": "8.8.8.8",
            "data": {"country": "United States"}
        }
    )

    resultado = servico.criar_ou_obter_ip("8.8.8.8")

    assert resultado["ip"] == "8.8.8.8"
    assert resultado["data"]["country"] == "United States"
