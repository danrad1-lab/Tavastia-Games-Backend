
import jwt
from datetime import datetime, timedelta, timezone
import requests


SECRET_KEY = "my_super_secret_key_which_is_very_long_123456"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

BREVO_API_KEY = "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"
SENDER_EMAIL = "danrad1@live.kktavastia.fi"



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

    print("EMAIL STATUS:", res.status_code)
    print("EMAIL RESPONSE:", res.text)

    return res.status_code, res.text
