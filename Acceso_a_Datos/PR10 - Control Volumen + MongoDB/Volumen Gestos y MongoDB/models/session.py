from datetime import datetime


class Session:
    def __init__(self, start_time=None, end_time=None): # el None es para que no pete si no le pasamos hora
        self.start_time = start_time if start_time else datetime.now() # para que pille la hora actual o la que le pasemos nosotros
        self.end_time =end_time

# para convertir el objeto de la sesión a diccionario
    def to_dict(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time
        }

