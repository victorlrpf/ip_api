import ipaddress


def validate_ip(ip: str) -> str:
    try:
        validated_ip = ipaddress.ip_address(ip)
        return str(validated_ip)
    except ValueError:
        raise ValueError("IP inválido.")