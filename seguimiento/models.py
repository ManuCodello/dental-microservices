import sqlite3
from typing import List, Dict, Optional

NOMBRE_BD = "seguimiento.db"


def obtener_registros() -> List[Dict]:
    """Lista todos los registros de seguimiento."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute("SELECT id, paciente_id, nota FROM seguimiento")
    filas = cur.fetchall()
    con.close()
    return [{"id": f[0], "paciente_id": f[1], "nota": f[2]} for f in filas]


def obtener_registros_por_paciente_id(paciente_id: int) -> List[Dict]:
    """Obtiene registros por ID de paciente."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "SELECT id, paciente_id, nota FROM seguimiento WHERE paciente_id = ?",
        (paciente_id,),
    )
    filas = cur.fetchall()
    con.close()
    return [{"id": f[0], "paciente_id": f[1], "nota": f[2]} for f in filas]


def obtener_registro_por_id(seg_id: int) -> Optional[Dict]:
    """Obtiene un registro de seguimiento por su ID."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "SELECT id, paciente_id, nota FROM seguimiento WHERE id = ?",
        (seg_id,),
    )
    fila = cur.fetchone()
    con.close()
    if not fila:
        return None
    return {"id": fila[0], "paciente_id": fila[1], "nota": fila[2]}


def agregar_registro(paciente_id: int, nota: str) -> int:
    """Crea un registro y devuelve su ID."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO seguimiento (paciente_id, nota) VALUES (?, ?)",
        (paciente_id, nota),
    )
    con.commit()
    nuevo_id = cur.lastrowid
    con.close()
    return nuevo_id


def actualizar_registro(seg_id: int, nota: Optional[str]) -> bool:
    """Actualiza la nota del registro. Devuelve True si se afectó una fila."""
    if nota is None:
        return False
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute("UPDATE seguimiento SET nota = ? WHERE id = ?", (nota, seg_id))
    con.commit()
    filas = cur.rowcount
    con.close()
    return filas > 0


def eliminar_registro(seg_id: int) -> bool:
    """Elimina un registro por ID. Devuelve True si se eliminó."""
    con = sqlite3.connect(NOMBRE_BD)
    cur = con.cursor()
    cur.execute("DELETE FROM seguimiento WHERE id = ?", (seg_id,))
    con.commit()
    filas = cur.rowcount
    con.close()
    return filas > 0
