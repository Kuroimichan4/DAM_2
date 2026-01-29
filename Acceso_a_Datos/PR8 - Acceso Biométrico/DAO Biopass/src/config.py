#  CLASE CONFIG: Solo lee el .env. No conecta.
# tiene una única misión: leer mi archivo .env y organizar los datos para que Python los entienda.

import os
from dotenv import load_dotenv
# load_dotenv() abre .env y carga las variables en la memoria del pc
#

class Config:
    def __init__(self):
        load_dotenv()

    def db_params(self) -> dict: # db_params(self) -> dict: Mete todos los datos (puerto, usuario, contraseña) en un diccionario
        return {
            "host": os.getenv("DB_HOST"), # os.getenv("DB_HOST"): Busca específicamente la línea que dice DB_HOST en el archivo .env
            "port": os.getenv("DB_PORT"),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
        }



