import ipaddress
import re


def validate_ip(ip: str) -> str:
    try:
        return str(ipaddress.ip_address(ip))
    except ValueError as exc:
        raise ValueError("IP inválido.") from exc


def validate_filter_ip(filter_ip: str) -> str:
    if not filter_ip:
        return filter_ip

    if len(filter_ip) < 3 or len(filter_ip) > 12:
        raise ValueError("filter_ip deve ter entre 3 e 12 caracteres.")

    if not re.match(r"^[0-9a-fA-F:.]+$", filter_ip):
        raise ValueError("filter_ip contém caracteres inválidos.")

    return filter_ip
