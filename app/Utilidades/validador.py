import ipaddress
import re


def validar_ip(ip: str) -> str:
    try:
        return str(ipaddress.ip_address(ip))
    except ValueError as exc:
        raise ValueError("IP inválido.") from exc


def validar_filtro_ip(filtro_ip: str) -> str:
    if not filtro_ip:
        return filtro_ip

    if len(filtro_ip) < 3 or len(filtro_ip) > 12:
        raise ValueError("filtro_ip deve ter entre 3 e 12 caracteres.")

    if not re.match(r"^[0-9a-fA-F:.]+$", filtro_ip):
        raise ValueError("filtro_ip contém caracteres inválidos.")

    return filtro_ip
