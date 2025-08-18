from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.db.dbconnection import Connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        username = request.form.get('username')
        password = request.form.get('password')

        # Validar campos vacíos
        if not nombre or not apellidos or not username or not password:
            flash("Todos los campos son obligatorios.", "error")
            return render_template('register.html')

        conn = Connection()

        # Verificar si el usuario ya existe
        existing_user = conn.select("SELECT * FROM jugadoress WHERE username = %s", (username,), one=True)
        if existing_user:
            flash("El nombre de usuario ya existe.", "error")
            return render_template('register.html')

        # Insertar usuario en la base de datos
        hashed_password = generate_password_hash(password)
        success = conn.execute(
            "INSERT INTO jugadoress (nombre, apellidos, username, password, puntos_totales) VALUES (%s, %s, %s, %s, %s)",
            (nombre, apellidos, username, hashed_password, 0)
        )

        if success:
            flash("Usuario registrado correctamente. ¡Ahora puedes iniciar sesión!", "success")
            return render_template('index.html')
        else:
            flash("Ocurrió un error al registrar el usuario.", "error")
            return render_template('register.html')

    return render_template('register.html')
