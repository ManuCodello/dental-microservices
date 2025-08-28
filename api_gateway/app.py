from flask import Flask
from routes import bp_gateway


def crear_aplicacion():
    app = Flask(__name__)
    app.register_blueprint(bp_gateway)
    return app


if __name__ == "__main__":
    app = crear_aplicacion()
    app.run(port=5000, debug=True)
