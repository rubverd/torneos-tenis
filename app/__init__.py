from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importar y registrar rutas
    from . import routes
    app.register_blueprint(routes.main)

    return app
