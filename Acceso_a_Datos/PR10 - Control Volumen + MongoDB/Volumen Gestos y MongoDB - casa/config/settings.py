import os
from dotenv import load_dotenv

# settings para que lea lea al las variables del .env como siempre

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "control_volumen_db")
SESSIONS_COLLECTION = os.getenv("SESSIONS_COLLECTION", "sessions")
EVENTS_COLLECTION = os.getenv("EVENTS_COLLECTION", "volume_events")



