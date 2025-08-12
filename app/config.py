# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# ---- Power BI (Service Principal) ----
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# IDs dos gateways
SVD_DOMINIO = os.getenv("SVD_DOMINIO")
SVD2_AUXILIAR = os.getenv("SVD2_AUXILIAR")
GW_IDS = [SVD_DOMINIO, SVD2_AUXILIAR]

# Endpoint base do Power BI
PBI_BASE = "https://api.powerbi.com/v1.0/myorg/gateways"

# ---- Evolution / WhatsApp ----
EVOLUTION_BASE_URL = (os.getenv("EVOLUTION_URL") or "").rstrip("/")
EVOLUTION_APIKEY = os.getenv("EVOLUTION_TOKEN")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")

def parse_numbers(raw: str | None):
    if not raw:
        return []
    raw = raw.replace(";", ",")
    return [n.strip() for n in raw.split(",") if n.strip()]

WHATSAPP_TO_LIST = parse_numbers(WHATSAPP_TO)

# ---- E-mail / SMTP ----
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_TO_LIST = parse_numbers(EMAIL_TO)
