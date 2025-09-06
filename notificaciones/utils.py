import sqlite3
import os
import jwt
from flask import request
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(BASE_DIR, "api_gateway", ".env")
load_dotenv(dotenv_path=ENV_PATH)


CLAVE_SECRETA = os.getenv("CLAVE_SECRETA", "super_secreto")
NOMBRE_BD = "notificaciones.db"


def inicializar_bd():
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            mensaje TEXT
        )
        """
    )
    con.commit()
    con.close()


def validar_token(req: request) -> bool:
    auth = req.headers.get("Authorization")
    if not auth:
        return False
    try:
        partes = auth.split()
        if len(partes) != 2 or partes[0].lower() != "bearer":
            return False
        token = partes[1]
        jwt.decode(token, CLAVE_SECRETA, algorithms=["HS256"])  # valida firma/exp
        return True
    except Exception:
        return False
