from pymongo import MongoClient
from datetime import datetime
from models.session import Session
from models.volume_event import VolumeEvent
from config.settings import MONGODB_URI, DATABASE_NAME, SESSIONS_COLLECTION, EVENTS_COLLECTION


class MongoDAO:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI) # conecta con el mongodb local
        self.db = self.client[DATABASE_NAME]
        self.sessions = self.db[SESSIONS_COLLECTION]
        self.events = self.db[EVENTS_COLLECTION]

    def start_session(self): # crea una sesión cuando empieza el programa
        session = Session()

        result = self.sessions.insert_one(session.to_dict())
        return result.inserted_id

    def end_session(self, session_id): # cierra la sesión
        self.sessions.update_one(
            {"_id": session_id},
            {"$set": {"end_time": datetime.now()}}
        )

    def save_event(self, session_id, volumen_anterior, volumen_nuevo, distancia): # guarda el cambio de volum,en de cada sesión
        event = VolumeEvent(session_id, volumen_anterior, volumen_nuevo, distancia)
        print("Guardando evento: ", event.to_dict())
        event = VolumeEvent(session_id, volumen_anterior, volumen_nuevo, distancia)
        self.events.insert_one(event.to_dict())