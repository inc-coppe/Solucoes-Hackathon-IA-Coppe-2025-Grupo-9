# Cole este código em services/review_service/src/main.py

from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Nossas importações
from . import security, models, schemas, crud
from .database import engine, SessionLocal
from .logging_config import logger

# --- Lógica de Inicialização ---
# Cria a tabela 'reviews' quando o serviço inicia
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Review Service",
    description="Serviço para coletar avaliações de pacientes.",
    version="1.0.0"
)

# --- Dependência para a sessão do BD ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoint Principal ---
@app.post("/reviews", response_model=schemas.ReviewResponse)
def submit_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: security.TokenData = Depends(security.get_current_user)
):
    """
    Submete uma nova avaliação para um agendamento concluído.
    - Requer autenticação.
    """
    logger.info(f"Usuário '{current_user.username}' submetendo avaliação para a marcação ID {review.marcacao_id}.")
    
    # Em um sistema real, verificaríamos se a marcação realmente existe e se pertence ao paciente
    
    return crud.create_review(db=db, review=review)