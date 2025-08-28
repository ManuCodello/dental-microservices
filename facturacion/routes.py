from flask import Blueprint, request, jsonify
from utils import validar_token
from models import obtener_facturas, agregar_factura

bp_facturacion = Blueprint("facturacion", __name__)


@bp_facturacion.route("/facturas", methods=["GET"])
def listar_facturas():
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    return jsonify(obtener_facturas())


@bp_facturacion.route("/facturas", methods=["POST"])
def crear_factura():
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    datos = request.get_json(silent=True) or {}
    paciente_id = datos.get("paciente_id")
    monto = datos.get("monto")
    estado = datos.get("estado")
    if paciente_id is None or monto is None or not estado:
        return jsonify({"error": "Campos requeridos: paciente_id, monto, estado"}), 400
    agregar_factura(paciente_id, float(monto), estado)
    return jsonify({"mensaje": "Factura creada"}), 201
