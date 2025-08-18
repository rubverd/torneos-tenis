from flask import Flask
from .routes import main, auth, puntuaciones
import os

def create_app():
    app = Flask(__name__)

    # Importar y registrar rutas
    app.secret_key = os.urandom(24)

    app.register_blueprint(main.main)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(puntuaciones.points_edit)

    return app
