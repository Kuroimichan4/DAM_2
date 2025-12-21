class Alumno:

    def __init__(self, nombre):
        self._nombre = nombre

    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, value):
        set._nombre = value

    def __str__(self) -> str:
        return self._nombre