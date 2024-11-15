from sqlalchemy.orm import Session
from app.db.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        legal_name = user_in.legal_name,
        preferred_name=user_in.preferred_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user