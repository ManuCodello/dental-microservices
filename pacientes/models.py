import sqlite3
from typing import List, Dict, Optional

NOMBRE_BD = "pacientes.db"


def obtener_pacientes() -> List[Dict]:
    """Obtiene todos los pacientes."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute("SELECT id, nombre, edad, cedula FROM pacientes")
    filas = cur.fetchall()
    con.close()
    return [
        {"id": f[0], "nombre": f[1], "edad": f[2], "cedula": f[3]}
        for f in filas
    ]


def obtener_paciente_por_id(paciente_id: int) -> Optional[Dict]:
    """Obtiene un paciente por su ID."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "SELECT id, nombre, edad, cedula FROM pacientes WHERE id = ?",
        (paciente_id,),
    )
    fila = cur.fetchone()
    con.close()
    if not fila:
        return None
    return {"id": fila[0], "nombre": fila[1], "edad": fila[2], "cedula": fila[3]}


def obtener_paciente_por_cedula(cedula: str) -> Optional[Dict]:
    """Obtiene un paciente por su cédula."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "SELECT id, nombre, edad, cedula FROM pacientes WHERE cedula = ?",
        (cedula,),
    )
    fila = cur.fetchone()
    con.close()
    if not fila:
        return None
    return {"id": fila[0], "nombre": fila[1], "edad": fila[2], "cedula": fila[3]}


def agregar_paciente(nombre: str, edad: int, cedula: str) -> int:
    """Crea un nuevo paciente y devuelve su ID."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO pacientes (nombre, edad, cedula) VALUES (?, ?, ?)",
        (nombre, edad, cedula),
    )
    con.commit()
    nuevo_id = cur.lastrowid
    con.close()
    return nuevo_id


def actualizar_paciente(paciente_id: int, nombre: Optional[str], edad: Optional[int], cedula: Optional[str]) -> bool:
    """Actualiza campos de un paciente. Devuelve True si se afectó una fila."""
    campos = []
    valores = []
    if nombre is not None:
        campos.append("nombre = ?")
        valores.append(nombre)
    if edad is not None:
        campos.append("edad = ?")
        valores.append(edad)
    if cedula is not None:
        campos.append("cedula = ?")
        valores.append(cedula)
    if not campos:
        return False
    valores.append(paciente_id)
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(f"UPDATE pacientes SET {', '.join(campos)} WHERE id = ?", valores)
    con.commit()
    filas = cur.rowcount
    con.close()
    return filas > 0


def eliminar_paciente(paciente_id: int) -> bool:
    """Elimina un paciente por ID. Devuelve True si se eliminó."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    con.commit()
    filas = cur.rowcount
    con.close()
    return filas > 0
