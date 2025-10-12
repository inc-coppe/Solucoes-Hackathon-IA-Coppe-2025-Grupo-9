# Cole este código em services/regulation_service/src/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def create_solicitacao(db: Session, solicitacao: schemas.SolicitacaoCreate):
    """
    Cria um novo registro de solicitação no banco de dados.
    """
    # Cria um objeto do modelo SQLAlchemy a partir dos dados do schema Pydantic
    db_solicitacao = models.Solicitacao(
        paciente_id=solicitacao.paciente_id,
        unidade_solicitante_id_cnes=solicitacao.unidade_solicitante_id_cnes,
        procedimento_id=solicitacao.procedimento_id,
        status="PENDENTE" # O status inicial é sempre PENDENTE
    )
    # Adiciona o objeto à sessão do banco de dados
    db.add(db_solicitacao)
    # Comita a transação para salvar no banco
    db.commit()
    # Atualiza o objeto db_solicitacao com os dados do banco (como o ID gerado)
    db.refresh(db_solicitacao)
    return db_solicitacao

def get_solicitacao(db: Session, solicitacao_id: int):
    """
    Busca uma única solicitação pelo seu ID.
    """
    return db.query(models.Solicitacao).filter(models.Solicitacao.id == solicitacao_id).first()


def update_solicitacao_status(db: Session, solicitacao_id: int, status_update: schemas.SolicitacaoStatusUpdate):
    """
    Atualiza o status e a justificativa de uma solicitação.
    """
    # Primeiro, busca a solicitação no banco
    db_solicitacao = get_solicitacao(db, solicitacao_id)
    
    if db_solicitacao:
        # Atualiza os campos
        db_solicitacao.status = status_update.status
        db_solicitacao.justificativa = status_update.justificativa
        
        # Comita a transação
        db.commit()
        # Atualiza a instância com os novos dados do banco
        db.refresh(db_solicitacao)
        
    return db_solicitacao

def create_marcacao(db: Session, solicitacao: models.Solicitacao, oferta: models.OfertaProgramada):
    """Cria a marcação, vincula à solicitação e atualiza status."""
    
    # Cria a marcação
    db_marcacao = models.Marcacao(solicitacao_id=solicitacao.id, oferta_id=oferta.id)
    db.add(db_marcacao)
    
    # Atualiza o status da solicitação para AGENDADA
    solicitacao.status = "AGENDADA"
    
    # Decrementa o número de vagas disponíveis
    if oferta.vagas_disponiveis > 0:
        oferta.vagas_disponiveis -= 1
        
    db.commit()
    db.refresh(solicitacao)
    
    return solicitacao

def create_oferta(db: Session, oferta: schemas.OfertaCreate):
    """Cria uma nova oferta de vaga."""
    db_oferta = models.OfertaProgramada(**oferta.model_dump())
    db.add(db_oferta)
    db.commit()
    db.refresh(db_oferta)
    return db_oferta

def get_marcacao(db: Session, marcacao_id: int):
    """Busca uma marcação pelo seu ID."""
    return db.query(models.Marcacao).filter(models.Marcacao.id == marcacao_id).first()

def update_marcacao_status_paciente(db: Session, db_marcacao: models.Marcacao, status: str):
    """Atualiza o status de confirmação do paciente em uma marcação."""
    db_marcacao.status_confirmacao_paciente = status
    db.commit()
    db.refresh(db_marcacao)
    return db_marcacao