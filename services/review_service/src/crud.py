# Cole este código em services/review_service/src/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def create_review(db: Session, review: schemas.ReviewCreate):
    """Cria uma nova avaliação no banco de dados."""
    db_review = models.Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review