import sqlite3
from typing import List, Dict, Optional

NOMBRE_BD = "notificaciones.db"


def obtener_notificaciones() -> List[Dict]:
    """Lista todas las notificaciones."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute("SELECT id, paciente_id, mensaje FROM notificaciones")
    filas = cur.fetchall()
    con.close()
    return [{"id": f[0], "paciente_id": f[1], "mensaje": f[2]} for f in filas]


def obtener_notificacion_por_id(noti_id: int) -> Optional[Dict]:
    """Obtiene una notificación por ID."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "SELECT id, paciente_id, mensaje FROM notificaciones WHERE id = ?",
        (noti_id,),
    )
    fila = cur.fetchone()
    con.close()
    if not fila:
        return None
    return {"id": fila[0], "paciente_id": fila[1], "mensaje": fila[2]}


def agregar_notificacion(paciente_id: int, mensaje: str) -> int:
    """Crea una notificación y devuelve su ID."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO notificaciones (paciente_id, mensaje) VALUES (?, ?)",
        (paciente_id, mensaje),
    )
    con.commit()
    nuevo_id = cur.lastrowid
    con.close()
    return nuevo_id


def actualizar_notificacion(noti_id: int, mensaje: Optional[str]) -> bool:
    """Actualiza el mensaje de una notificación. Devuelve True si se afectó una fila."""
    if mensaje is None:
        return False
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "UPDATE notificaciones SET mensaje = ? WHERE id = ?",
        (mensaje, noti_id),
    )
    con.commit()
    filas = cur.rowcount
    con.close()
    return filas > 0


def eliminar_notificacion(noti_id: int) -> bool:
    """Elimina una notificación por ID. Devuelve True si se eliminó."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute("DELETE FROM notificaciones WHERE id = ?", (noti_id,))
    con.commit()
    filas = cur.rowcount
    con.close()
    return filas > 0
