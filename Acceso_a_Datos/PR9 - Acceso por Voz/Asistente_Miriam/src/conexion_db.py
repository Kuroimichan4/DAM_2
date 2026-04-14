# Clase SINGLETON: Gestiona la conexión única a postgree
# evita abrir conexiones nuevas constantemente

import psycopg2 ## librería traductora para hablar con PostgreSQL: connect(), cursor(), execute()
from src.config import Config
import os

class DBConnection:
    _connection = None # esto le dice que no abra una clase cada vez (_ delante de connection para indicar que es una variable privada)

    # el If de si ya existe una conexión no crea otra
    @classmethod # Indica que este metod pertenece a la clase en sí. Nos permite usar cls para acceder a la variable de conexión compartida. Y trabajar con la clase directamente
    # esto se pone para no tener que instanciar/crear un objeto que creara una conexión cada vez, haciendop perder el sentido a lo de singleton
    def get_connection(cls):  #cls es como el self o el this se usa por convención. cls porque es una clase, la clase DBConection. Guarda en cls la conexión con toda la info
        """
        - Si ya existe y está abierta, la reutiliza.
        - Si no existe o está cerrada, crea una nueva.
        """
        if cls._connection is not None and cls._connection.closed == 0:
            return cls._connection

        # si no, cargamos el .env y montamos parámetros con Config
        params = Config().db_params()

        #  Creamos la conexión nueva
        cls._connection = psycopg2.connect(**params)
        # abre la conexión y el símbolo ** le dice a python que use todos los parámetros de config para conectar ({"host":"localhost","port":"5432"})

        # retorna la conexión simplemente
        return cls._connection


# por si quiero cerrar la conexión aunque ya se cierra de forma auto cuando se cierra el progrtama que es lo que se quiere con una clase singleton
    @classmethod
    def close_connection(cls):
        if cls._connection is not None and cls._connection.closed == 0:
            cls._connection.close()
            cls._connection = None