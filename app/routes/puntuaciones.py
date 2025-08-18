from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db.dbconnection import Connection

points_edit = Blueprint("points_edit", __name__, url_prefix="/puntuaciones")

@points_edit.route("/editar-puntuaciones", methods=["GET", "POST"])
def editar_puntuaciones():
    db = Connection()

    if request.method == "POST":
        try:
            # Traer todos los jugadores para saber qué IDs hay
            jugadores = db.select("SELECT id, username, puntos_totales FROM jugadores")

            for jugador in jugadores:
                puntos_str = request.form.get(f"puntos_totales{jugador['id']}")
                if puntos_str is not None:
                    nuevos_puntos = int(puntos_str)
                    db.execute(
                        "UPDATE jugadores SET puntos_totales = %s WHERE id = %s",
                        (nuevos_puntos, jugador['id'])
                    )
            
            flash("✅ Puntuaciones actualizadas correctamente", "success")
            return redirect(url_for("points_edit.editar_puntuaciones"))
        except Exception as e:
            flash(f"❌ Error al actualizar puntuaciones: {e}", "error")

    # Si es GET -> mostrar formulario
    jugadores = db.select("SELECT id, username, puntos_totales FROM jugadores ORDER BY puntos_totales DESC")
    return render_template("puntuaciones.html", jugadores=jugadores)
