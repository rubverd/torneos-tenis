from flask import Flask
from .routes import main, auth
import os

def create_app():
    app = Flask(__name__)

    # Importar y registrar rutas
    app.secret_key = os.urandom(24)

    app.register_blueprint(main.main)
    app.register_blueprint(auth.auth_bp)

    return app
