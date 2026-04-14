# Clase DAO: Consultas y manejo de JSONB
# lo del Singleton era lo de abrir solo una instancia de la conexión para no saturar con multiples conexiones
# JSONB de PostgreSQL es el estándar industrial para guardar metadatos variables de forma eficiente.
# Almacena los datos en un formato binario que permite indexación
# y búsquedas ultrarrápidas, siendo mucho más ágil en su explotación que el JSON simple
# o el texto plano cuando se manejan grandes volúmenes de datos

import psycopg2 # librería traductora para hablar con PostgreSQL: connect(), cursor(), execute() o commit()
from datetime import datetime # obtiene la hora y fechas actuales
from src.conexion_db import DBConnection # importamos la clase de config para la conexióin
import json # para convertir el dict a json


class AuthDAO:
    def usuario_existente(self, username: str) -> bool:
        conn = DBConnection.get_connection()

        try:
            with conn.cursor() as curs: # el with cerraba el cursor de forma automática sin tener que hacer un close dentro de un finally
                # creamos un cursor que es el objeto que ejecuta SQL

                sql = "SELECT 1 FROM usuarios_voz WHERE username = %s;"
                curs.execute(sql, (username,)) # Execute de psycopg2 tiene que recibir, sí o sí una lista/tupla de valores
                # Como en esta sentencia solo hay 1 parametro se pone una coma al final, para hacer creer a psycopg2 que es una tupla/lista de varios elementos

                resultado = curs.fetchone() #fetchone trae solo una fila

                return resultado is not None # si existe es not null y devuelve True
        except Exception as e:
            print("Error al verificar usuario: ", e)
            return False


    def registrar_usuario(self, username: str, passphrase: str):

        # primero comprobar si existe el usuario
        if self.usuario_existente(username):
            print("El usuario ya existe")
            return

        conn = DBConnection.get_connection()

        try:
            with conn.cursor() as curs:

                sql = "INSERT INTO usuarios_voz(username, passphrase_text) VALUES(%s, %s);"
                curs.execute(sql, (username, passphrase))

                conn.commit()

                print(f"Usuario {username} registrado correctamente")

        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error en la base de datos: {e}")
        except Exception as e:
            conn.rollback()  # si algo falla, volver atras
            print("Error en el registro: ", e)

    def validar_login(self, username: str, passphrase: str) -> bool:
        conn = DBConnection.get_connection()

        try:
            with conn.cursor() as curs:
                sql = "SELECT passphrase_text FROM usuarios_voz WHERE username = %s;"
                curs.execute(sql, (username,))
                resultado = curs.fetchone()

                if resultado is None:
                    print("El usuario no existe")
                    return False
                if self.usuario_bloqueado(username):
                    print("Usuario bloqueado 30 segundos")
                    self.registrar_log(username, False, "usuario bloqueado")
                    return False

                passphrase_guardada = resultado[0] # la frase seleccionada

                # compara la frase dicha con la passphrase_guardada
                if passphrase == passphrase_guardada:
                    print(f"Usuario {username} verificado correctamente")
                    self.registrar_log(username, True, "login correcto")
                    self.resetear_intentos_fallidos(username)
                    return True
                else:
                    print("Frase incorrecta")
                    self.intentos_fallidos(username)

                    intentos = self.obtener_intentos(username)
                    if intentos >= 3:
                        print("Demasiados intentos: usuario bloqueado 30 segundos")
                        self.bloqueo_usuarios(username)
                        self.registrar_log(username, False, "bloqueado por 3 intentos")
                        return False

                    self.registrar_log(username, False, "Frase incorrecta")
                    return False

        except Exception as e:
            print("Error al verificar usuario: ", e)
            return False

    def intentos_fallidos(self, username: str):
        conn = DBConnection.get_connection()

        try:
            with conn.cursor() as curs:
                sql = "UPDATE usuarios_voz SET intentos_fallidos = intentos_fallidos + 1 WHERE username = %s;"
                curs.execute(sql, (username,))
                conn.commit()

        except Exception as e:
            conn.rollback()
            print("Error al actualizar fallidos: ", e)

    def bloqueo_usuarios(self, username: str):
        conn = DBConnection.get_connection()

        try:
            with conn.cursor() as curs:
                sql = "UPDATE usuarios_voz SET bloqueado_hasta = NOW() + INTERVAL '30 seconds' WHERE username = %s;"

                curs.execute(sql, (username,))
                conn.commit()

        except Exception as e:
            conn.rollback()
            print("Error al bloquear usuario: ", e)

    def obtener_intentos(self, username: str) -> int:
        conn = DBConnection.get_connection()
        try:
            with conn.cursor() as curs:
                sql = "SELECT intentos_fallidos FROM usuarios_voz WHERE username = %s;"

                curs.execute(sql, (username,))
                fila = curs.fetchone()

                if fila :
                    return fila[0] # posición 0 de la tupla

                return 0 # si no existe pues no hay intentos y ya
        except Exception as e:
            print("Error al obtener intentos: ", e)
        return 0

    def usuario_bloqueado(self, username: str) -> bool:
        conn = DBConnection.get_connection()

        try:
            with conn.cursor() as curs:
                sql = "SELECT bloqueado_hasta FROM usuarios_voz WHERE username = %s;"
                curs.execute(sql,(username,))
                fila = curs.fetchone()

                # Si no existe
                if fila is None:
                    return False

                bloqueado_hasta = fila[0]

                # si es null es que no está bloqueadpo
                if bloqueado_hasta is None:
                    return False

                # se compara la hora de python con la de la BBDD xq la zona horaria puede ser distinta
                ahora = datetime.now()

                # devuelve la hora y fecha hasta cuando está bloqueado
                # cuando se comparan 2 datetime en python se escribe así. Está preguntando si ahora ha llegado a la hora de bloqueo hasta
                return ahora < bloqueado_hasta

        except Exception as e:
            print("Error al obtener bloqueado: ", e)
            return False

    def resetear_intentos_fallidos(self, username: str):
        conn = DBConnection.get_connection()

        try:
            with conn.cursor() as curs:
                sql ="UPDATE usuarios_voz SET intentos_fallidos = 0, bloqueado_hasta = NULL  WHERE username = %s;"
                curs.execute(sql, (username,))
                conn.commit()

        except Exception as e:
            conn.rollback()
            print("Error al resetear fallidos: ", e)

    # para el registro de log del usuario
    def get_id_usuario(self, username: str):
        conn = DBConnection.get_connection()

        try:
            with conn.cursor() as curs:
                sql = "SELECT id FROM usuarios_voz WHERE username = %s;"
                curs.execute(sql, (username,))
                fila = curs.fetchone()

                if fila is None:
                    return None

                return fila[0]

        except Exception as e:
            print("Error al obtener ID ", e)
            return None


    def registrar_log(self, username: str, exito: bool, motivo: str):
        """
        Inserta un registro en log_accesos_voz con JSONB.
        - exito: True/False
        - motivo: texto corto explicando el resultado
        """
        conn = DBConnection.get_connection()

        try:
            usuario_id = self.get_id_usuario(username)

            # Si el usuario no existe, no podemos meter usuario_id (sería NULL),

            if usuario_id is None:
                print("No se registra log: usuario no existe")
                return

            # Preparamos el JSON (diccionario de Python)
            resultado = {
                "username": username,
                "exito": exito,
                "motivo": motivo
            }

            with conn.cursor() as curs:
                # lo de  ::jsonb es para castear/convertir el texto a Json binario
                sql = """
                    INSERT INTO log_accesos_voz (usuario_id, resultado_json)
                    VALUES (%s, %s::jsonb);
                """

                # json.dumps convierte diccionario a texto JSON
                curs.execute(sql, (usuario_id, json.dumps(resultado)))
                conn.commit()

        except Exception as e:
            conn.rollback()
            print("Error al registrar log:", e)



