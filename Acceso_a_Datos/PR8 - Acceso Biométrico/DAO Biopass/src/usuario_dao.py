# *-------------- Conecta con la BBDD y hace las consultas SQL como con los servlets y los preparedstatments, es el traductor de consultas--------
#  Usa el Singleton para hacer consultas.
import psycopg2 #
from src.conexion_db import DBConnection

class UsuarioDAO:
    def registrar_usuario(self, nombre: str, foto_bytes: bytes, cara_bytes: bytes) -> None:
        conn = DBConnection.get_connection()
        sql = "INSERT INTO usuarios (nombre, foto, cara) VALUES (%s, %s, %s);" # son placeholders el equivalente a VALUES (?,?) de java y los servlets de mierda

        with conn.cursor() as curs:
            curs.execute(sql,(
                nombre,
                psycopg2.Binary(foto_bytes), # psycopg2 Convierte los bytes de la imagen a un formato que PostgreSQL entiende
                psycopg2.Binary(cara_bytes)
            ))
        conn.commit()

    def obtener_todos(self): # para hacer el login y que compare la cara con las que hay en la BBDD
        conn = DBConnection.get_connection()
        sql = "SELECT id, nombre, foto, cara From usuarios ORDER BY id;"

        with conn.cursor() as curs:
            curs.execute(sql)
            return curs.fetchall()

        # -+-------------------------------------------------------- me quedé por aquí------------------------- --------------------

    def obtener_caras(self):

        conn = DBConnection.get_connection()
        sql = "SELECT id, nombre, cara FROM usuarios ORDER BY id;"
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()