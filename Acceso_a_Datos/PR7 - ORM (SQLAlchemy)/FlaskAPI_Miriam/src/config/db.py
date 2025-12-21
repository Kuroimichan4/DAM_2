from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.config import Config


# 1. Crear el engine (conecta con la BD)
engine = create_engine(Config.DATABASE_URI, echo=True)

# 2. Crear la fábrica de sesiones
SessionLocal = sessionmaker(bind=engine)

# 3. Clase base para los models (tablas)
Base = declarative_base()
