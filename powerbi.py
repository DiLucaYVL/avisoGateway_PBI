import requests
from config import PBI_BASE, PBI_BEARER

# Obtém informações do gateway
def get_gateway(gateway_id: str):
    """Chama GET /gateways/{id} e retorna JSON."""
    url = f"{PBI_BASE}/{gateway_id}"
    headers = {"Authorization": PBI_BEARER, "Accept": "application/json"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def is_live(value: str) -> bool:
    """Compara status com 'Live' de forma tolerante."""
    if not value:
        return False
    v = value.strip().lower()
    # Alguns tenants podem retornar 'online'; deixe tratado também.
    return v in ("live", "online")
