import os
from dotenv import load_dotenv
import jwt

load_dotenv()

CLAVE_SECRETA = os.getenv("CLAVE_SECRETA", "super_secreto")


def validar_token(req):
    auth = req.headers.get("Authorization")
    if not auth:
        return False
    try:
        partes = auth.split()
        if len(partes) != 2 or partes[0].lower() != "bearer":
            return False
        token = partes[1]
        jwt.decode(token, CLAVE_SECRETA, algorithms=["HS256"])  # valida firma y exp
        return True
    except Exception:
        return False
