# Versão final e completa de services/regulation_service/src/main.py

from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Nossas importações
from . import security, models, schemas, crud, agent, communication_client
from .database import engine, SessionLocal
from .logging_config import logger

# --- Lógica de Inicialização ---
app = FastAPI(
    title="Regulation Service",
    description="Serviço principal para a lógica de negócio da regulação de saúde.",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    logger.info("Evento de STARTUP acionado.")
    try:
        logger.info("Criando tabelas do banco de dados...")
        models.Base.metadata.create_all(bind=engine)
        logger.info("Tabelas verificadas/criadas com sucesso.")
        
        from .data_generator import generate_fake_data
        db = SessionLocal()
        try:
            generate_fake_data(db)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Erro CRÍTICO durante a inicialização: {e}")

# --- Dependência para a sessão do BD ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Regulation Service is running"}

@app.get("/me")
async def read_users_me(
    auth_info: dict = Depends(security.get_current_user)
):
    current_user = auth_info["payload"]
    return {"username": current_user.username}

@app.post("/solicitacoes", response_model=schemas.SolicitacaoResponse)
def create_new_solicitacao(
    solicitacao: schemas.SolicitacaoCreate,
    db: Session = Depends(get_db),
    auth_info: dict = Depends(security.get_current_user)
):
    current_user = auth_info["payload"]
    logger.info(f"Usuário '{current_user.username}' criando nova solicitação para o paciente '{solicitacao.paciente_id}'.")
    return crud.create_solicitacao(db=db, solicitacao=solicitacao)

@app.put("/solicitacoes/{solicitacao_id}/status", response_model=schemas.SolicitacaoResponse)
def update_status_solicitacao(
    solicitacao_id: int,
    status_update: schemas.SolicitacaoStatusUpdate,
    db: Session = Depends(get_db),
    auth_info: dict = Depends(security.get_current_user)
):
    current_user = auth_info["payload"]
    token = auth_info["token_string"]
    logger.info(f"Usuário '{current_user.username}' atualizando status da solicitação ID {solicitacao_id} para '{status_update.status}'.")
    
    if status_update.status in ["NEGADA", "CANCELADA"] and not status_update.justificativa:
        raise HTTPException(status_code=400, detail="Justificativa é obrigatória para status NEGADA ou CANCELADA.")

    db_solicitacao = crud.get_solicitacao(db=db, solicitacao_id=solicitacao_id)
    if not db_solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
    
    if status_update.status == "ACEITA":
        logger.info(f"Status da solicitação {solicitacao_id} mudou para ACEITA. Acionando agente inteligente...")
        melhor_oferta = agent.find_best_slot(db=db, solicitacao=db_solicitacao)
        
        if melhor_oferta:
            final_solicitacao = crud.create_marcacao(db=db, solicitacao=db_solicitacao, oferta=melhor_oferta)
            logger.info(f"Agente agendou com sucesso a solicitação {solicitacao_id}. Novo status: {final_solicitacao.status}")
            
            marcacao = db.query(models.Marcacao).filter(models.Marcacao.solicitacao_id == final_solicitacao.id).first()
            if marcacao:
                oferta = db.query(models.OfertaProgramada).get(marcacao.oferta_id)
                unidade = db.query(models.Unidade).get(oferta.unidade_id)
                procedimento = db.query(models.Procedimento).get(oferta.procedimento_id)

                mensagem = (f"Seu agendamento para '{procedimento.nome}' foi confirmado para a data {oferta.data_agendamento.strftime('%d/%m/%Y')} "
                            f"na unidade '{unidade.nome}'. Por favor, confirme o seu agendamento.")
                
                communication_client.send_notification(
                    paciente_id=final_solicitacao.paciente_id,
                    mensagem=mensagem,
                    token=token
                )

            return final_solicitacao
        else:
            status_update.status = "EM FILA"
            logger.warning(f"Agente não encontrou vagas para a solicitação {solicitacao_id}. Status movido para EM FILA.")
            
    updated_solicitacao = crud.update_solicitacao_status(
        db=db, solicitacao_id=solicitacao_id, status_update=status_update
    )
    
    return updated_solicitacao

@app.post("/ofertas", response_model=schemas.OfertaResponse)
def create_new_oferta(
    oferta: schemas.OfertaCreate,
    db: Session = Depends(get_db),
    auth_info: dict = Depends(security.get_current_user)
):
    current_user = auth_info["payload"]
    logger.info(f"Usuário '{current_user.username}' criando nova oferta.")
    return crud.create_oferta(db=db, oferta=oferta)

@app.post("/marcacoes/{marcacao_id}/confirmar", response_model=schemas.SolicitacaoResponse)
def confirm_marcacao(
    marcacao_id: int,
    db: Session = Depends(get_db),
    auth_info: dict = Depends(security.get_current_user)
):
    current_user = auth_info["payload"]
    logger.info(f"Ação de confirmação para marcação {marcacao_id} pelo usuário '{current_user.username}'.")
    
    db_marcacao = crud.get_marcacao(db, marcacao_id=marcacao_id)
    if not db_marcacao:
        raise HTTPException(status_code=404, detail="Marcação não encontrada.")
    
    crud.update_marcacao_status_paciente(db, db_marcacao, "CONFIRMADO")
    db_solicitacao = crud.get_solicitacao(db, db_marcacao.solicitacao_id)
    logger.info(f"Marcação {marcacao_id} confirmada pelo paciente.")
    return db_solicitacao

@app.post("/marcacoes/{marcacao_id}/negar", response_model=schemas.SolicitacaoResponse)
def deny_marcacao(
    marcacao_id: int,
    db: Session = Depends(get_db),
    auth_info: dict = Depends(security.get_current_user)
):
    current_user = auth_info["payload"]
    logger.info(f"Ação de negação para marcação {marcacao_id} pelo usuário '{current_user.username}'.")

    db_marcacao = crud.get_marcacao(db, marcacao_id=marcacao_id)
    if not db_marcacao:
        raise HTTPException(status_code=404, detail="Marcação não encontrada.")

    db_solicitacao = crud.get_solicitacao(db, db_marcacao.solicitacao_id)
    status_update = schemas.SolicitacaoStatusUpdate(
        status="CANCELADA",
        justificativa="Agendamento recusado pelo paciente."
    )
    crud.update_solicitacao_status(db, db_solicitacao.id, status_update)
    logger.info(f"Marcação {marcacao_id} negada pelo paciente. Solicitação cancelada.")
    return crud.get_solicitacao(db, db_marcacao.solicitacao_id)

@app.post("/marcacoes/{marcacao_id}/concluir", response_model=schemas.SolicitacaoResponse)
def complete_marcacao(
    marcacao_id: int,
    db: Session = Depends(get_db),
    auth_info: dict = Depends(security.get_current_user)
):
    current_user = auth_info["payload"]
    token = auth_info["token_string"]
    logger.info(f"Ação de conclusão para marcação {marcacao_id} pelo usuário '{current_user.username}'.")

    db_marcacao = crud.get_marcacao(db, marcacao_id=marcacao_id)
    if not db_marcacao:
        raise HTTPException(status_code=404, detail="Marcação não encontrada.")

    db_solicitacao = crud.get_solicitacao(db, db_marcacao.solicitacao_id)
    status_update = schemas.SolicitacaoStatusUpdate(status="CONCLUIDA")
    crud.update_solicitacao_status(db, db_solicitacao.id, status_update)
    logger.info(f"Marcação {marcacao_id} concluída.")
    
    mensagem = (f"Olá! Vimos que seu procedimento foi concluído. "
                f"Gostaríamos de saber sua opinião sobre o atendimento.")
    
    communication_client.send_notification(
        paciente_id=db_solicitacao.paciente_id,
        mensagem=mensagem,
        token=token
    )
    
    return crud.get_solicitacao(db, db_marcacao.solicitacao_id)