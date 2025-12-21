from flask import jsonify, request
from src.config.db import SessionLocal
from src.models.Libro import Libro

def init_api_routes(app): # esto son los endpoints basicamente

# Get de el total de la BBDD
    @app.route("/api/libros", methods=["GET"])
    def get_libros():
        session = SessionLocal() # herramienta de SQLAlchemy ORM para abrir una conexión privada con la BBDD
        try:
            libros = session.query(Libro).all() # aqui le digo que en la conexión a la BBDD quiero lanzar una query a la tabla de libros
            # y que quiero todos los resultados en libros. No se usa lenguaje de sql, el all es como un select * from...
            # como los objetos son hechos con SQLAlchemy hace las peticiones en su idioma y después las parsea para la BBDD
            # también se puede hacer de esta forma más nueva: session.scalars(select(Libro)).all()
            libros_list = [
                {
                    "id": l.id,
                    "titulo": l.titulo,
                    "autor": l.autor,
                    "ano": l.ano,
                    "genero": l.genero
                }
                for l in libros
            ]
            return jsonify(libros_list), 200 # jsonify es una función de flask que coge un diccionario y lo parsea a JSON
        finally: # para que lo ejecute siempre, falle o no
            session.close() # cierra el canal para no consumir recursos como siempre

# GET por ID
    @app.route("/api/libros/<int:id>", methods=["GET"]) # lo del <int:id> pilla el id de la url
    def get_libro_id(id):
        session = SessionLocal()
        try:
            libro = session.get(Libro, id) # también puede ser así: session.get(Libro).get(id) pero está deprecado

            if libro is None:
                return jsonify({"mensaje": "Libro no encontrado"}), 404

            return jsonify({
                "id": libro.id,
                "titulo": libro.titulo,
                "autor": libro.autor,
                "ano": libro.ano,
                "genero": libro.genero
            }), 200

        finally: session.close()

    @app.route("/api/libros", methods=["POST"])
    def crear_libro():
           session = SessionLocal()
           try:
               data = request.get_json()

               if not data or not data.get("titulo") or not data.get("autor"):
                    return jsonify({"mensaje": "Faltan campos obligatorios (título o autor)"}), 400

               nuevo_libro = Libro(
                   titulo=data.get("titulo"),
                   autor=data.get("autor"),
                   ano=data.get("ano"),
                   genero=data.get("genero")
               )

               session.add(nuevo_libro)
               session.commit()

               return jsonify({
                   "mensaje": "Libro creado correctamente",
                   "id": nuevo_libro.id
               }), 201

           finally:
               session.close()
# para hacer el POST:
# http://127.0.0.1:5000/api/libros
#{
#  "titulo": "El Archivo de las Tormentas: El camino de los Reyes",
#  "autor": "Brandon Sanderson",
#  "ano": 2010,
#  "genero": "Alta Fantasía"
#}

    @app.route("/api/libros/<int:id>", methods=["PUT"])
    def modificar_libro(id):
        session = SessionLocal()
        try:
            libro = session.query(Libro).get(id)

            if libro is None:
                return jsonify({"mensaje": "Libro no encontrado"}), 404

            data = request.get_json()

            if not data:
                return jsonify({"mensaje": "No se han enviado datos"}), 400

            if "titulo" in data:
                libro.titulo = data["titulo"]
            if "autor" in data:
                libro.autor = data["autor"]
            if "ano" in data:
                libro.ano = data["ano"]
            if "genero" in data:
                libro.genero = data["genero"]

            session.commit()

            return jsonify({"mensaje": "Libro modificado correctamente"}), 200
        finally:
            session.close()

    @app.route("/api/libros/<int:id>", methods=["DELETE"])
    def borrar_libro(id):
        session = SessionLocal()
        try:
            libro = session.query(Libro).get(id)

            if libro is None:
                return jsonify({"mensaje": "Libro no encontrado"}), 404

            session.delete(libro)
            session.commit()

            return jsonify({"mensaje": "Libro borrado correctamente"}), 200

        finally: session.close()