import smtplib
from email.message import EmailMessage
from typing import Tuple
from config import EMAIL_USER, EMAIL_PASS, EMAIL_TO_LIST, EMAIL_HOST, EMAIL_PORT

def send_email(subject: str, body: str) -> Tuple[bool, str]:
    """
    Envia e-mail (texto simples) para todos os destinatários.
    Retorna (ok, info).
    """
    if not (EMAIL_USER and EMAIL_PASS and EMAIL_TO_LIST and EMAIL_HOST and EMAIL_PORT):
        return False, "config_email_incompleta"

    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_USER
        msg["To"] = ", ".join(EMAIL_TO_LIST)
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        return True, f"email_ok:{len(EMAIL_TO_LIST)}"
    except Exception as e:
        return False, f"email_erro:{e}"
