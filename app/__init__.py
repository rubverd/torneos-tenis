from flask import Flask
from .routes import main, auth

def create_app():
    app = Flask(__name__)

    # Importar y registrar rutas
    
    app.register_blueprint(main.main)
    app.register_blueprint(auth.auth_bp)

    return app
