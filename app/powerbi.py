import requests
import os
from app.config import PBI_BASE, TENANT_ID, CLIENT_ID, CLIENT_SECRET

AUTH_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
SCOPE = "https://analysis.windows.net/powerbi/api/.default"

def get_pbi_token() -> str:
    """
    Client Credentials (app-only).
    Gera um access token válido para chamar a API do Power BI.
    """
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE,
        "grant_type": "client_credentials",
    }
    r = requests.post(AUTH_URL, data=data, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]

def get_gateway(gateway_id: str) -> dict:
    """GET /gateways/{id}"""
    token = get_pbi_token()
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    url = f"{PBI_BASE}/{gateway_id}"
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

def is_live(value: str | None) -> bool:
    """Trata 'Live' e 'Online' como OK."""
    if not value:
        return False
    return value.strip().lower() in ("live", "online")
