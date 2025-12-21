# Path trabaja con rutas de archivos y carpetas de forma cómoda y multiplataforma (Windows, Linux, macOS) es mejor que usar os.loquesea
from pathlib import Path
from dominio.Alumno import Alumno

class AlumnosMatriculados:
    # ruta del archivo (static)
    ruta_archivo: str = str(Path("data") / "alumnos.txt") # en data creará un txt llamado alumnos

    # he creado la carpeta data previamente pero si borramos el archivo siempre comprovará su existencia cuando vayamos a grabar y si no existe se creará
    @staticmethod
    def crear_fichero():
        Path("data").mkdir(exist_ok=True)

    @staticmethod # crea un metodo statico
    def matricular_alumno(alumno: Alumno): # le pasa el nombre del alumno del input
        AlumnosMatriculados.crear_fichero()
        # x - creará el ficheroy falla si ya existe
        # a - append añade al final del fichero y crea el archivo si no existe
        # w - write sobrescribe (trunca) el archivo
        # encoding="utf-8" admite formato de escritura con acentos y simbolos
        #
        try: # Con "a" no hace falta “crear el archivo” antes (se crea solo), pero sí la carpeta data
            with open(AlumnosMatriculados.ruta_archivo, "a", encoding="utf-8") as archivo: # el nombre de archivo es arbitrario
                archivo.write(f'{alumno}\n') # se guarda lo del input en el archivo
        except Exception as e:
            print(f"Ha ocurrido un error al matricular: {e}")

    @staticmethod
    def listar_alumnos() -> list[str]:
        ruta = Path(AlumnosMatriculados.ruta_archivo)
        if not ruta.exists():
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return [linea.strip() for linea in f if linea.strip()]
        except Exception as e:
            print(f"Ha ocurrido un error al leer: {e}")
            return []

    @staticmethod
    def eliminar_alumnos() -> None:
        ruta = Path(AlumnosMatriculados.ruta_archivo)

        if ruta.exists():
            ruta.unlink()  # esto es como el os.remove de los apuntes



