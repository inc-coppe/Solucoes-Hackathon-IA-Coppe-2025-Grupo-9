# Cole este código em services/regulation_service/src/models.py

from sqlalchemy import Column, Integer, String, DateTime, func, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from .data_generator import generate_fake_data

class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(String, index=True, nullable=False)
    unidade_solicitante_id_cnes = Column(String, nullable=False)
    procedimento_id = Column(String, nullable=False)
    
    # Status da regulação
    status = Column(String, default="PENDENTE") 
    
    justificativa = Column(String, nullable=True)
    
    # Timestamps automáticos
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())

    # Adicionaremos mais campos aqui conforme avançamos

class Unidade(Base):
    __tablename__ = "unidades"
    id = Column(Integer, primary_key=True, index=True)
    cnes_id = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class Procedimento(Base):
    __tablename__ = "procedimentos"
    id = Column(Integer, primary_key=True, index=True)
    procedimento_id = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)

class OfertaProgramada(Base):
    __tablename__ = "ofertas_programadas"
    id = Column(Integer, primary_key=True, index=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    procedimento_id = Column(Integer, ForeignKey("procedimentos.id"), nullable=False)
    data_agendamento = Column(Date, nullable=False)
    vagas_disponiveis = Column(Integer, default=1)
    horario = Column(String)

class Marcacao(Base):
    __tablename__ = "marcacoes"
    id = Column(Integer, primary_key=True, index=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacoes.id"), nullable=False)
    oferta_id = Column(Integer, ForeignKey("ofertas_programadas.id"), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    # O status da confirmação do paciente que planejamos
    status_confirmacao_paciente = Column(String, default="PENDENTE")