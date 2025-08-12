from flask import Flask
from . import routes

def create_app():
    app = Flask(__name__)

    # Importar y registrar rutas
    
    app.register_blueprint(routes.main)

    return app
