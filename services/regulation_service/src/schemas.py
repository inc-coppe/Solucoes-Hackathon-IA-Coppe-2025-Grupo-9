# Cole este código em services/regulation_service/src/schemas.py

from pydantic import BaseModel
from datetime import datetime, date

# Schema para os dados recebidos na criação de uma solicitação (entrada da API)
class SolicitacaoCreate(BaseModel):
    paciente_id: str
    unidade_solicitante_id_cnes: str
    procedimento_id: str

# Schema para os dados retornados pela API após a criação (saída da API)
# Isso evita vazar dados internos do banco, como senhas hasheadas, etc.
class SolicitacaoResponse(BaseModel):
    id: int
    paciente_id: str
    unidade_solicitante_id_cnes: str
    procedimento_id: str
    status: str
    data_criacao: datetime

    class Config:
        #orm_mode = True # Permite que o Pydantic leia dados de objetos SQLAlchemy
        from_attributes = True

# Schema para o corpo da requisição de atualização de status
class SolicitacaoStatusUpdate(BaseModel):
    status: str # Ex: "ACEITA", "NEGADA", "CANCELADA"
    justificativa: str | None = None # Opcional, mas obrigatório para alguns status

class OfertaCreate(BaseModel):
    unidade_id: int
    procedimento_id: int
    data_agendamento: date
    vagas_disponiveis: int
    horario: str

class OfertaResponse(BaseModel):
    id: int
    unidade_id: int
    procedimento_id: int
    data_agendamento: date
    vagas_disponiveis: int
    horario: str

    class Config:
        from_attributes = True