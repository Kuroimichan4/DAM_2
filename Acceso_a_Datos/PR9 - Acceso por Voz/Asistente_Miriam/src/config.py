# Clase Config: Lee el .env y organiza los datos para que Python los entienda.
# es básicamente un traductor para la configuración

import os #librería que permite interactuar con el sistema operativo
from dotenv import load_dotenv # importa la funcion load_dotenv de la librería dotenv para pillar la info del .env y meter sus valores en variables

class Config:
    def __init__(self): # __init__ es un méthod especial que se ejecuta automáticamente cuando se crea un objeto de una clase, inicializando el objeto.
        # es el equivalente al constructor en otros lenguajes
        load_dotenv() # comando que abre el .env, lo lee y lo carga en memoria para que después os.getenv pueda leer las variables

    def db_params(self) -> dict:  # db_params(self) -> dict: Mete todos los datos (puerto, usuario, contraseña) en un diccionario
        # el dict es meramente informativo para los programadores en realidad no hace nada

        # Devuelve un diccionario con los parámetros que psycopg2 necesita
        return {
            "host": os.getenv("DB_HOST"),
            # os.getenv("DB_HOST"): Busca específicamente la línea que dice DB_HOST en el archivo .env
            "port": os.getenv("DB_PORT"),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
        }