import os
import psycopg2
from psycopg2.extras import RealDictCursor

class Connection:
    """
    Clase para gestionar la conexión a PostgreSQL en Railway usando psycopg2.
    """

    def __init__(self):
        # Railway expone DATABASE_URL como variable de entorno
        self.db_url = os.getenv("DATABASE_URL")

        if not self.db_url:
            raise ValueError("❌ No se encontró la variable de entorno DATABASE_URL")

        self.connection = None

    def get_connection(self):
        """
        Abre una conexión y la guarda en self.connection si no existe.
        """
        if not self.connection:
            try:
                self.connection = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
            except psycopg2.Error as e:
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
                result = cursor.fetchone() if one else cursor.fetchall()
                return result
        except Exception as e:
            print(f"❌ Error al ejecutar SELECT: {e}")
            return None

    def execute(self, query: str, args: tuple = (), return_last_id: bool = False):
        """
        Ejecuta INSERT, UPDATE o DELETE.
        Si `return_last_id=True`, devuelve el id insertado (requiere RETURNING en el query).
        """
        conn = self.get_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, args)

                if return_last_id:
                    last_id = cursor.fetchone()
                    conn.commit()
                    return last_id
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error al ejecutar operación: {e}")
            return False

    def call_procedure(self, procedure: str, args: tuple = ()):
        """
        Llama a un procedimiento almacenado (en PostgreSQL sería una función).
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
