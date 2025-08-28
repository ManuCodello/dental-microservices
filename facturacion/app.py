from flask import Flask
from routes import bp_facturacion
from utils import inicializar_bd


def crear_aplicacion():
    app = Flask(__name__)
    inicializar_bd()
    app.register_blueprint(bp_facturacion)
    return app


if __name__ == "__main__":
    app = crear_aplicacion()
    app.run(port=5003, debug=True)
