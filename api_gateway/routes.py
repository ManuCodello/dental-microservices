from flask import Blueprint, request, jsonify
import os
import time
import requests
import jwt
from utils import validar_token, CLAVE_SECRETA

bp_gateway = Blueprint("gateway", __name__)

# Mapa de microservicios
MICROSERVICIOS = {
    "pacientes": "http://localhost:5001",
    "consultas": "http://localhost:5002",
    "facturacion": "http://localhost:5003",
    "seguimiento": "http://localhost:5004",
    "notificaciones": "http://localhost:5005",
}


@bp_gateway.route("/auth/token", methods=["POST"])
def emitir_token():
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario", "demo")
    ahora = int(time.time())
    payload = {
        "sub": usuario,
        "iat": ahora,
        "exp": ahora + 60 * 60,  # 1 hora
        "alcance": ["api"],
    }
    token = jwt.encode(payload, CLAVE_SECRETA, algorithm="HS256")
    return jsonify({"token": token})


@bp_gateway.route("/<servicio>/<path:endpoint>", methods=["GET", "POST"])  # proxy simple
def proxy(servicio, endpoint):
    if servicio not in MICROSERVICIOS:
        return jsonify({"error": "Servicio no encontrado"}), 404

    if not validar_token(request):
        return jsonify({"error": "Token inválido"}), 403

    url_destino = f"{MICROSERVICIOS[servicio]}/{endpoint}"
    try:
        if request.method == "GET":
            response = requests.get(url_destino, headers=_headers_a_encaminar())
        else:
            response = requests.post(
                url_destino,
                json=request.get_json(silent=True),
                headers=_headers_a_encaminar(),
            )
    except requests.RequestException as e:
        return jsonify({"error": "Microservicio inaccesible", "detalle": str(e)}), 502

    # Intenta devolver JSON, si no es JSON devuelve texto
    try:
        cuerpo = response.json()
    except ValueError:
        cuerpo = {"texto": response.text}
    return jsonify(cuerpo), response.status_code
 

def _headers_a_encaminar():
    # Encaminamos Authorization por si los servicios también verifican
    encabezados = {}
    auth = request.headers.get("Authorization")
    if auth:
        encabezados["Authorization"] = auth
    return encabezados
    
#falta idempotencia 