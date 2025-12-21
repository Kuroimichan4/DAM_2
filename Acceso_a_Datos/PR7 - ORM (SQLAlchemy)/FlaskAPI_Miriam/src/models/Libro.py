from sqlalchemy import Column, Integer, String
from src.config.db import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=True)
    genero = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Libros id={self.id} name={self.titulo}>"

