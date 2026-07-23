import logging

import requests
from fastapi import HTTPException

from app.config import settings

logger = logging.getLogger(__name__)


def verify_webhook(mode: str, token: str, challenge: str) -> str:
    if mode == "subscribe" and token == settings.VERIFY_TOKEN:
        return challenge
    raise HTTPException(status_code=403, detail="Token de verificacion invalido")


def send_message(to: str, text: str) -> bool:
    url = f"https://graph.facebook.com/{settings.VERSION}/{settings.PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            logger.info("Mensaje enviado a %s", to)
            return True
        else:
            logger.error("Error al enviar mensaje: %s - %s", response.status_code, response.text)
            return False
    except requests.RequestException as e:
        logger.error("Excepcion al enviar mensaje: %s", e)
        return False


def process_message(body: dict) -> dict:
    try:
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        messages = value.get("messages", [])
        if not messages:
            return {"status": "ok"}

        msg = messages[0]
        from_ = msg["from"]
        text = msg.get("text", {}).get("body", "")

        response_text = generate_response(from_, text)
        send_message(from_, response_text)

        return {"status": "ok"}

    except (KeyError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid webhook payload")


def generate_response(from_: str, text: str) -> str:
    return f"Recibido: {text}"
