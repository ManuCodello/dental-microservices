from flask import Flask
from routes import bp_seguimiento
from utils import inicializar_bd


def crear_aplicacion():
    app = Flask(__name__)
    inicializar_bd()
    app.register_blueprint(bp_seguimiento)
    return app


if __name__ == "__main__":
    app = crear_aplicacion()
    app.run(port=5004, debug=True)
