# CLASE SINGLETON: Usa Config para conectar.
# permite que python se comunique con postgreSQL mediante Singleton para que solo exista una conexión
import psycopg2 # librería que hace de traductor que permite enviar comandos a postgre connect(), cursor(), execute()
from src.config import Config
# llama a la clase config que está en el src.config.py que sabe leer el .env y así DBConnection no necesita la contra, se la pide a Config.py

class DBConnection:
    _connection = None # esto le dice que no abra una clase cada vez

# el If de si ya existe una conexión no crea otra
    @classmethod # Indica que este metod pertenece a la clase en sí
    def get_connection(cls): #cls es como el self o el this se usa por convención. cls porque es una clase, la clase DBConection. Guarda en cls la conexión con toda la info
        if cls._connection is not None and cls._connection.closed == 0:
            return cls._connection

        params = Config().db_params()
        cls._connection = psycopg2.connect(**params) # abre la conexión y el símbolo ** le dice a python que use todos los parámetros de config para conectar ({"host":"localhost","port":"5432"})
        return cls._connection # retorna la conexión simplemente

# *------------------------------------------------------------ mirar bien el cierre de la conexión -----------------------------------------------
    @classmethod
    def close_connection(cls):
        if cls._connection is not None and cls._connection.closed == 0:
            cls._connection.close()
            cls._connection = None

