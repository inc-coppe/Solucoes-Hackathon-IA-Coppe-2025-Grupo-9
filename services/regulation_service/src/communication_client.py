# Em services/regulation_service/src/communication_client.py

import httpx
from .logging_config import logger

COMMUNICATION_SERVICE_URL = "http://communication_service:8000/notifications/send"

def send_notification(paciente_id: str, mensagem: str, token: str):
    """
    Chama a API do communication-service para enviar uma notificação.
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"paciente_id": paciente_id, "mensagem": mensagem}
        
        with httpx.Client() as client:
            # A CORREÇÃO FINAL ESTÁ AQUI: Adicionando 'headers=headers'
            response = client.post(
                COMMUNICATION_SERVICE_URL, 
                json=payload, 
                headers=headers, # <-- ESTE PARÂMETRO ESTAVA FALTANDO
                timeout=5.0
            )
            response.raise_for_status()
        
        logger.info(f"Solicitação de notificação enviada com sucesso para o paciente {paciente_id}.")
        return True
    except httpx.RequestError as e:
        logger.error(f"Erro ao tentar se comunicar com o communication-service: {e}")
        return False