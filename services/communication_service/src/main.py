# Cole este código final em services/communication_service/src/main.py

import logging
from typing import Annotated
from fastapi import FastAPI, Depends
import os

# Nossas importações de segurança
from . import security
from .schemas import NotificationRequest

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Communication Service",
    description="Serviço para enviar notificações simuladas aos pacientes.",
    version="1.0.0"
)
'''
@app.get("/debug-env")
def debug_environment():
    """
    Endpoint de teste para verificar as variáveis de ambiente lidas pelo serviço.
    """
    secret_key_read = os.getenv("SECRET_KEY")
    algorithm_read = os.getenv("JWT_ALGORITHM")
    
    return {
        "message": "Variáveis de ambiente lidas pelo communication-service",
        "SECRET_KEY_READ": secret_key_read,
        "JWT_ALGORITHM_READ": algorithm_read
    }
'''
# Adicionamos a proteção ao endpoint aqui
@app.post("/notifications/send")
async def send_notification(
    request: NotificationRequest,
    auth_info: dict = Depends(security.get_current_user)
):
    """
    Recebe e processa uma solicitação de notificação. Requer autenticação.
    """
    # Extraímos o payload do usuário corretamente
    current_user = auth_info["payload"]
    
    # A CORREÇÃO ESTÁ AQUI: Acessamos o atributo '.username' diretamente
    logger.info(f"Notificação solicitada pelo usuário autenticado: '{current_user.username}'")
    
    logger.info(f"--- SIMULANDO ENVIO DE NOTIFICAÇÃO ---")
    logger.info(f"Para: Paciente ID {request.paciente_id}")
    logger.info(f"Mensagem: \"{request.mensagem}\"")
    logger.info(f"------------------------------------")
    
    return {"status": "success", "message": "Notification processed."}