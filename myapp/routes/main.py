from flask import Blueprint, render_template
from myapp.db.dbconnection import Connection

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html',ranking=get_ranking())

def get_ranking():
    conn = Connection()
    ranking = conn.select(
        "SELECT username, puntos_totales FROM jugadores ORDER BY puntos_totales DESC"
    )
    return ranking
