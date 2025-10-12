from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    marcacao_id = Column(Integer, unique=True, nullable=False) # Vinculado à marcação original
    paciente_id = Column(String, index=True, nullable=False)
    nota = Column(Integer, nullable=False) # Nota de 1 a 5
    comentario = Column(Text, nullable=True)