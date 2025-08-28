import sqlite3

NOMBRE_BD = "consultas.db"


def obtener_consultas():
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute("SELECT id, paciente_id, fecha, motivo FROM consultas")
    filas = cur.fetchall()
    con.close()
    return [
        {"id": f[0], "paciente_id": f[1], "fecha": f[2], "motivo": f[3]}
        for f in filas
    ]


def agregar_consulta(paciente_id: int, fecha: str, motivo: str):
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO consultas (paciente_id, fecha, motivo) VALUES (?, ?, ?)",
        (paciente_id, fecha, motivo),
    )
    con.commit()
    con.close()
