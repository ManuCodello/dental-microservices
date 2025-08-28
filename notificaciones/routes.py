from flask import Blueprint, request, jsonify
from typing import Any, Dict
from utils import validar_token
from models import (
    obtener_notificaciones,
    agregar_notificacion,
    obtener_notificacion_por_id,
    actualizar_notificacion,
    eliminar_notificacion,
)

bp_notificaciones = Blueprint("notificaciones", __name__)


@bp_notificaciones.route("/notificaciones", methods=["GET"])
def listar_notificaciones():
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    return jsonify(obtener_notificaciones())


@bp_notificaciones.route("/notificaciones", methods=["POST"])
def crear_notificacion():
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    datos: Dict[str, Any] = request.get_json(silent=True) or {}
    paciente_id = datos.get("paciente_id")
    mensaje = datos.get("mensaje")
    if paciente_id is None or not mensaje:
        return jsonify({"error": "Campos requeridos: paciente_id, mensaje"}), 400
    nuevo_id = agregar_notificacion(int(paciente_id), str(mensaje))
    return jsonify({"mensaje": "Notificación enviada", "id": nuevo_id}), 201


@bp_notificaciones.route("/notificaciones/<int:noti_id>", methods=["GET"])
def obtener_notificacion(noti_id: int):
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    noti = obtener_notificacion_por_id(noti_id)
    if not noti:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(noti)


@bp_notificaciones.route("/notificaciones/<int:noti_id>", methods=["PUT"])
def actualizar_notificacion_endpoint(noti_id: int):
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    datos: Dict[str, Any] = request.get_json(silent=True) or {}
    ok = actualizar_notificacion(noti_id, datos.get("mensaje"))
    if not ok:
        return jsonify({"error": "No se actualizó (verifique ID o campos)"}), 400
    return jsonify({"mensaje": "Notificación actualizada"})


@bp_notificaciones.route("/notificaciones/<int:noti_id>", methods=["DELETE"])
def eliminar_notificacion_endpoint(noti_id: int):
    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403
    ok = eliminar_notificacion(noti_id)
    if not ok:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"mensaje": "Notificación eliminada"})
