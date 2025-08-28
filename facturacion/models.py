import sqlite3

NOMBRE_BD = "facturas.db"


def obtener_facturas():
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute("SELECT id, paciente_id, monto, estado FROM facturas")
    filas = cur.fetchall()
    con.close()
    return [
        {"id": f[0], "paciente_id": f[1], "monto": f[2], "estado": f[3]}
        for f in filas
    ]


def agregar_factura(paciente_id: int, monto: float, estado: str):
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO facturas (paciente_id, monto, estado) VALUES (?, ?, ?)",
        (paciente_id, monto, estado),
    )
    con.commit()
    con.close()
