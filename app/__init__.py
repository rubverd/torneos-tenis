from flask import Flask, render_template
from .routes import main, auth, puntuaciones
import os

def create_app():
    app = Flask(__name__)

    # Importar y registrar rutas
    app.secret_key = os.urandom(24)

    app.register_blueprint(main.main)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(puntuaciones.points_edit)

    register_error_handlers(app)

    return app

def register_error_handlers(app):
    @app.errorhandler(405)
    def error404(error):
        return render_template('error.html'), 405