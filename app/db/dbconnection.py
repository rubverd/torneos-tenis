import pymysql
from pymysql.cursors import DictCursor
from app.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# Cargar variables de entorno desde .env (asegúrate de tenerlo en .gitignore)

class Connection:
    """
    Clase para gestionar la conexión a la base de datos MySQL/MariaDB usando pymysql.
    """

    def __init__(self):
        # Parámetros de conexión obtenidos de variables de entorno
        self.connection_params = {
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME,
            "user": DB_USER,
            "password": DB_PASSWORD,
            "charset": "utf8mb4",
            "cursorclass": DictCursor
        }
        self.connection = None

    def get_connection(self):
        """
        Abre una conexión y la guarda en self.connection si no existe.
        """
        if not self.connection:
            try:
                self.connection = pymysql.connect(**self.connection_params)
            except pymysql.MySQLError as e:
                print(f"❌ Error al conectarse a la base de datos: {e}")
                self.connection = None
        return self.connection

    def close_connection(self):
        """
        Cierra la conexión activa si existe.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def select(self, query: str, args: tuple = (), one: bool = False):
        """
        Ejecuta una consulta SELECT.
        """
        conn = self.get_connection()
        if not conn:
            return None
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                return cursor.fetchone() if one else cursor.fetchall()
        except Exception as e:
            print(f"❌ Error al ejecutar SELECT: {e}")
            return None

    def execute(self, query: str, args: tuple = (), return_last_id: bool = False):
        """
        Ejecuta INSERT, UPDATE o DELETE.
        """
        conn = self.get_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                last_id = cursor.lastrowid
            conn.commit()
            return last_id if return_last_id else True
        except Exception as e:
            print(f"❌ Error al ejecutar operación: {e}")
            return False

    def call_procedure(self, procedure: str, args: tuple = ()):
        """
        Llama a un procedimiento almacenado.
        """
        conn = self.get_connection()
        if not conn:
            return None
        try:
            with conn.cursor() as cursor:
                cursor.callproc(procedure, args)
                result = cursor.fetchall()
            conn.commit()
            return result
        except Exception as e:
            print(f"❌ Error al ejecutar procedimiento: {e}")
            return None
