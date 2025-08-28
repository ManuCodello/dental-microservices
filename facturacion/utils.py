import sqlite3
import os
import jwt
from flask import request
from dotenv import load_dotenv

load_dotenv()

CLAVE_SECRETA = os.getenv("CLAVE_SECRETA", "super_secreto")
NOMBRE_BD = "facturas.db"


def inicializar_bd():
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            monto REAL,
            estado TEXT
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
