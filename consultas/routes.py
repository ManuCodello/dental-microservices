from flask import Blueprint, request, jsonify
from utils import validar_token
from models import obtener_consultas, agregar_consulta

bp_consultas = Blueprint("consultas", __name__)


@bp_consultas.route("/consultas", methods=["GET"])
def listar_consultas():
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    return jsonify(obtener_consultas())


@bp_consultas.route("/consultas", methods=["POST"])
def crear_consulta():
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    datos = request.get_json(silent=True) or {}
    paciente_id = datos.get("paciente_id")
    fecha = datos.get("fecha")
    motivo = datos.get("motivo")
    if paciente_id is None or not fecha or not motivo:
        return jsonify({"error": "Campos requeridos: paciente_id, fecha, motivo"}), 400
    agregar_consulta(paciente_id, fecha, motivo)
    return jsonify({"mensaje": "Consulta registrada"}), 201
