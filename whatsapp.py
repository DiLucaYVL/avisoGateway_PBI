import logging, requests
from config import EVOLUTION_BASE_URL, EVOLUTION_APIKEY, EVOLUTION_INSTANCE, WHATSAPP_TO, WHATSAPP_TO_LIST

def evolution_send(text: str):
    if not (EVOLUTION_BASE_URL and EVOLUTION_APIKEY and EVOLUTION_INSTANCE and (WHATSAPP_TO or WHATSAPP_TO_LIST)):
        logging.error("Config da Evolution API incompleta; não foi possível enviar mensagem.")
        return False, "config_incompleta"

    url = f"{EVOLUTION_BASE_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {"apikey": EVOLUTION_APIKEY, "Content-Type": "application/json"}

    numbers = WHATSAPP_TO_LIST if WHATSAPP_TO_LIST else [WHATSAPP_TO]

    results = []
    all_ok = True
    for number in numbers:
        payload = {
            "number": number,
            "textMessage": { "text": text }
        }
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=20)
            ok = r.status_code in (200, 201)
            logging.info("Mensagem enviada para -> %s | status=%s body=%s", number, r.status_code, (r.text or "")[:300])
            results.append(f"{number}:{r.status_code}")
            if not ok:
                all_ok = False
        except Exception as e:
            logging.exception("Erro ao enviar WhatsApp para %s: %s", number, e)
            results.append(f"{number}:EXC")
            all_ok = False

    return all_ok, "; ".join(results)