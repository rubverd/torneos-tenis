from flask import Flask
from .routes import main, auth
from app.config import SECRET_KEY

def create_app():
    app = Flask(__name__)

    # Importar y registrar rutas
    app.secret_key = SECRET_KEY

    app.register_blueprint(main.main)
    app.register_blueprint(auth.auth_bp)

    return app
