# Cole este código em services/review_service/src/schemas.py

from pydantic import BaseModel, Field

# Schema para os dados de entrada ao criar uma avaliação
class ReviewCreate(BaseModel):
    marcacao_id: int
    paciente_id: str
    nota: int = Field(..., ge=1, le=5) # Garante que a nota seja entre 1 e 5
    comentario: str | None = None

# Schema para os dados de saída
class ReviewResponse(BaseModel):
    id: int
    marcacao_id: int
    paciente_id: str
    nota: int
    comentario: str | None = None

    class Config:
        from_attributes = True