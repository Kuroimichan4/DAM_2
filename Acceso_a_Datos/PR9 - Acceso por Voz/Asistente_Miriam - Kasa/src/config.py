# Clase Config: Lee el .env y organiza los datos para que Python los entienda.

import os
from dotenv import load_dotenv

load_dotenv() # comando que abre el .env, lo lee y lo inyecyta en las variables en la memoria del programa

class Config:
    def __init__(self):
        load_dotenv()

    def db_params(selfself) -> dict:  # db_params(self) -> dict: Mete todos los datos (puerto, usuario, contraseña) en un diccionario

        # Devuelve un diccionario con los parámetros que psycopg2 necesita
        return {
            "host": os.getenv("DB_HOST"),
            # os.getenv("DB_HOST"): Busca específicamente la línea que dice DB_HOST en el archivo .env
            "port": os.getenv("DB_PORT"),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
        }