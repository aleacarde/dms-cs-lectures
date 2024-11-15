from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.models.user_model import User
from app.schemas.user_schema import UserOut, UserCreate
from app.dependencies import get_db
from app.api import deps
from app import services

router = APIRouter()

@router.post("/classes/", response_model=UserOut)
def create_user(
    user_in: UserCreate,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return services.user_service.create_user(db_session, user_in, current_user)