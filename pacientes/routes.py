from flask import Blueprint, request, jsonify
from typing import Any, Dict
from utils import validar_token
from models import (
    obtener_pacientes,
    agregar_paciente,
    obtener_paciente_por_id,
    actualizar_paciente,
    eliminar_paciente,
    obtener_paciente_por_cedula,
)

bp_pacientes = Blueprint("pacientes", __name__)


@bp_pacientes.route("/pacientes", methods=["GET"])
def listar_pacientes():
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    return jsonify(obtener_pacientes())


@bp_pacientes.route("/pacientes", methods=["POST"])
def crear_paciente():
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    datos: Dict[str, Any] = request.get_json(silent=True) or {}
    nombre = datos.get("nombre")
    edad = datos.get("edad")
    cedula = datos.get("cedula")
    if not nombre or edad is None or not cedula:
        return jsonify({"error": "Campos requeridos: nombre, edad, cedula"}), 400
    nuevo_id = agregar_paciente(str(nombre), int(edad), str(cedula))
    return jsonify({"mensaje": "Paciente agregado", "id": nuevo_id}), 201


@bp_pacientes.route("/pacientes/<int:paciente_id>", methods=["GET"])
def obtener_paciente(paciente_id: int):
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    paciente = obtener_paciente_por_id(paciente_id)
    if not paciente:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(paciente)


@bp_pacientes.route("/pacientes/<int:paciente_id>", methods=["PUT"])
def actualizar_paciente_endpoint(paciente_id: int):
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    datos: Dict[str, Any] = request.get_json(silent=True) or {}
    ok = actualizar_paciente(
        paciente_id,
        datos.get("nombre"),
        datos.get("edad"),
        datos.get("cedula"),
    )
    if not ok:
        return jsonify({"error": "No se actualizó (verifique ID o campos)"}), 400
    return jsonify({"mensaje": "Paciente actualizado"})


@bp_pacientes.route("/pacientes/<int:paciente_id>", methods=["DELETE"])
def eliminar_paciente_endpoint(paciente_id: int):
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    ok = eliminar_paciente(paciente_id)
    if not ok:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"mensaje": "Paciente eliminado"})


@bp_pacientes.route("/pacientes/por-cedula/<string:cedula>", methods=["GET"])
def obtener_por_cedula(cedula: str):
    """Busca un paciente por cédula (para consumo de Seguimiento)."""
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    paciente = obtener_paciente_por_cedula(cedula)
    if not paciente:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(paciente)
