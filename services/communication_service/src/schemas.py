# Em services/communication_service/src/schemas.py
from pydantic import BaseModel

class NotificationRequest(BaseModel):
    paciente_id: str
    mensagem: str