import os

class Config:
    # Base de datos SQLite en un archivo llamado students.db
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///libreria.db")
    DEBUG = True
