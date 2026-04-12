from datetime import datetime

class VolumeEvent:
    def __init__(self, session_id, volumen_anterior, volumen_nuevo, distancia, timestamp=None):
        self.session_id = session_id
        self.volumen_anterior = volumen_anterior
        self.volumen_nuevo = volumen_nuevo
        self.distancia = distancia
        self.timestamp = timestamp if timestamp else datetime.now()

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "volumen_anterior": self.volumen_anterior,
            "volumen_nuevo": self.volumen_nuevo,
            "distancia": self.distancia,
            "timestamp": self.timestamp,
        }