from flask import Blueprint, request, jsonify
from typing import Any, Dict
import requests
from utils import validar_token
from models import (
    obtener_registros,
    agregar_registro,
    obtener_registros_por_paciente_id,
    obtener_registro_por_id,
    actualizar_registro,
    eliminar_registro,
)

bp_seguimiento = Blueprint("seguimiento", __name__)
PACIENTES_URL = "http://localhost:5001"  # servicio pacientes


@bp_seguimiento.route("/seguimiento", methods=["GET"])
def listar_registros():
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    return jsonify(obtener_registros())


@bp_seguimiento.route("/seguimiento", methods=["POST"])
def crear_registro():
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    datos: Dict[str, Any] = request.get_json(silent=True) or {}
    paciente_id = datos.get("paciente_id")
    nota = datos.get("nota")
    if paciente_id is None or not nota:
        return jsonify({"error": "Campos requeridos: paciente_id, nota"}), 400
    nuevo_id = agregar_registro(int(paciente_id), str(nota))
    return jsonify({"mensaje": "Registro clínico agregado", "id": nuevo_id}), 201


@bp_seguimiento.route("/seguimiento/<int:seg_id>", methods=["GET"])
def obtener_registro(seg_id: int):
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    reg = obtener_registro_por_id(seg_id)
    if not reg:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(reg)


@bp_seguimiento.route("/seguimiento/<int:seg_id>", methods=["PUT"])
def actualizar_registro_endpoint(seg_id: int):
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    datos: Dict[str, Any] = request.get_json(silent=True) or {}
    ok = actualizar_registro(seg_id, datos.get("nota"))
    if not ok:
        return jsonify({"error": "No se actualizó (verifique ID o campos)"}), 400
    return jsonify({"mensaje": "Registro actualizado"})


@bp_seguimiento.route("/seguimiento/<int:seg_id>", methods=["DELETE"])
def eliminar_registro_endpoint(seg_id: int):
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    ok = eliminar_registro(seg_id)
    if not ok:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"mensaje": "Registro eliminado"})


@bp_seguimiento.route("/seguimiento/por-cedula/<string:cedula>", methods=["GET"])
def listar_por_cedula(cedula: str):
    """Obtiene los registros de seguimiento de un paciente consultando su cédula en el servicio de pacientes."""
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    # Llamamos al servicio pacientes para resolver la cédula a un ID de paciente
    try:
        resp = requests.get(
            f"{PACIENTES_URL}/pacientes/por-cedula/{cedula}",
            headers={"Authorization": request.headers.get("Authorization", "")},
            timeout=5,
        )
    except requests.RequestException as e:
        return jsonify({"error": "Servicio pacientes inaccesible", "detalle": str(e)}), 502

    if resp.status_code != 200:
        return jsonify({"error": "Paciente no encontrado por cédula"}), 404
    paciente = resp.json()
    pac_id = paciente.get("id")
    if pac_id is None:
        return jsonify({"error": "Paciente inválido"}), 400
    return jsonify(obtener_registros_por_paciente_id(int(pac_id)))


