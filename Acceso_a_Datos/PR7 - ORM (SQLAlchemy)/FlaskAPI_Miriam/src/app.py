
# pip install Flask SQLAlchemy

# api: tendrá las rutas/endpoints.
# models: las clases que representan tablas (Student, etc.).
# config: cosas de configuración (BD, parámetros…).


from flask import Flask

from src.config.db import Base, engine
from src.models import Libro  # importa el módulo para que SQLAlchemy vea la clase (luego importaremos las rutas)
from src.models import Libro  # importa el módulo para registrar los libros
from src.api.routes import init_api_routes  # son los endpoints basicamente


app = Flask(__name__)


# Crear las tablas en la BD (si no existen)
Base.metadata.create_all(bind=engine)

# Registrar las rutas de la API
init_api_routes(app)

if __name__ == "__main__":
    app.run(debug=True)

# para hacer Run:
# python -m src.app