import os
import jwt
from datetime import datetime, timedelta, timezone
import requests


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

print("SECRET_KEY:", SECRET_KEY)
print("BREVO_API_KEY:", BREVO_API_KEY)
print("SENDER_EMAIL:", SENDER_EMAIL)

# === Модели ===


# === JWT функции ===
def create_token(seat_id: int, first_name: str, last_name: str, email: str):

    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)#Time of JWT tokens living

    # Data, which collect in JWT token.
    payload = {
        "seat_id": seat_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "exp": expire,
        "type": "email_verification"
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #JWT token decoding
        if payload.get("type") != "email_verification":
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# === Email через Brevo ===
def send_email(email: str, token: str):
    url = "https://api.brevo.com/v3/smtp/email"
    verify_link = f"https://tavastiagames.com/seat-verify.html?token={token}" # Заменить на ссылку на апи страницу сервера

    payload = {
        "sender": {"email": SENDER_EMAIL},
        "to": [{"email": email}],
        "subject": "Verify email",
        "htmlContent": f"""
        <h3>Verify email</h3>
        <p>Verify:</p>
        <a href="{verify_link}">{verify_link}</a>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers)

    return res.status_code, res.text


def send_seat_email(email: str, seat: int):
    url = "https://api.brevo.com/v3/smtp/email"
    verify_link = f"https://tavastiagames.com/seat-verify.html?token={token}" # Заменить на ссылку на апи страницу сервера

    payload = {
        "sender": {"email": SENDER_EMAIL},
        "to": [{"email": email}],
        "subject": "Paikka",
        "htmlContent": f"""
        <h3>Paikka varaus</h3>
        <p>Varasit paikan {seat}:</p>
        <a href="{verify_link}">{verify_link}</a>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers)

    return res.status_code, res.text
