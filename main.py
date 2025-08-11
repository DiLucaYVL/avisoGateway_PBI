import logging, requests
from config import PBI_BEARER, GW_IDS
from powerbi import get_gateway, is_live
from whatsapp import evolution_send
from email_notifier import send_email

# ---- Logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)

def _fallback_email_then_file(subject: str, body: str):
    """Tenta enviar e-mail; se falhar, grava em alert_fallback.log."""
    ok_mail, info_mail = send_email(subject, body)
    logging.info("Email: %s (%s)", ok_mail, info_mail)
    if not ok_mail:
        try:
            with open("alert_fallback.log", "a", encoding="utf-8") as f:
                f.write(body + "\n\n")
            logging.info("Fallback em arquivo: alert_fallback.log")
        except Exception as e:
            logging.exception("Falha ao gravar fallback em arquivo: %s", e)

# Função main
def main():
    if not PBI_BEARER or not PBI_BEARER.lower().startswith("bearer "):
        raise SystemExit("Defina PBI_BEARER no .env (incluindo 'Bearer ').")

    for gid in GW_IDS:
        if not gid:
            continue
        try:
            gw = get_gateway(gid)
            name = gw.get("name") or gid
            status = gw.get("gatewayStatus")

            logging.info("Gateway '%s' (%s): gatewayStatus=%s", name, gid, status)

            if not is_live(status):
                subject = "[ALERTA] Power BI Gateway offline"
                msg = (
                    "----------------- [ALERTA: POWER BI] -----------------\n\n"
                    f"> Gateway: {name}\n"
                    f"> ID: {gid}\n"
                    f"> Status: {status or 'desconhecido'}\n"
                )
                ok, info = evolution_send(msg)
                logging.info("WhatsApp: %s (%s)", ok, info)
                if not ok:
                    _fallback_email_then_file(subject, msg)

        except requests.HTTPError as http_err:
            subject = "[ERRO] Verificação de Gateway"
            body = (
                "----------------- [ERRO VERIFICAÇÃO POWER BI] -----------------\n\n"
                f"> Gateway ID: {gid}\n"
                f"> HTTPError: {http_err}\n"
                f"> Body: {getattr(http_err, 'response', None).text if getattr(http_err, 'response', None) else ''}\n"
            )
            logging.error("HTTPError ao consultar gateway %s: %s", gid, http_err)
            _fallback_email_then_file(subject, body)

        except Exception as e:
            subject = "[ERRO] Verificação de Gateway"
            body = (
                "----------------- [ERRO VERIFICAÇÃO POWER BI] -----------------\n\n"
                f"> Gateway ID: {gid}\n"
                f"> Exception: {e}\n"
            )
            logging.exception("Erro geral ao processar gateway %s: %s", gid, e)
            _fallback_email_then_file(subject, body)

if __name__ == "__main__":
    main()