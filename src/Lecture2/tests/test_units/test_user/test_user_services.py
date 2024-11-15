import pytest
from sqlalchemy.orm import Session
from app.db.models.user_model import Session
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user
from app.core.security import verify_password

def test_create_user_service(db_session: Session):
    user_in = UserCreate(
        username="serviceuser",
        email="serviceuser@example.com",
        legal_name="Service User",
        password="securepassword"
    )
    user = create_user(db=db_session, user_in=user_in)
    assert user.id is not None
    assert user.username == "serviceuser"
    assert user.email == "serviceuser@example.com"
    assert user.legal_name == "Service User"
    assert verify_password("securepassword", user.hashed_password)

def test_create_user_existing_username(db_session: Session):
    user_in = UserCreate(
        username="duplicateuser",
        email="duplicateuser1@example.com",
        name="User One",
        password="password1"
    )
    create_user(db=db_session, user_in=user_in)

    user_in_duplicate = UserCreate(
        username="duplicateuser",
        email="duplicateuser2@example.com",
        name="User Two",
        password="password2"
    )
    with pytest.raises(Exception) as e_info:
        create_user(db=db_session, user_in=user_in_duplicate)
    assert "UNIQUE constraint failed" in str(e_info.value)

def test_create_user_existing_email(db_session: Session):
    user_in = UserCreate(
        username = "useruniqueemail",
        email="uniqueemail@example.com",
        name="User Email",
        password="password"
    )
    create_user(db=db_session, user_in=user_in)

    user_in_duplicate_email = UserCreate(
        username="useruniqueemail2",
        email="uniqueemail@example.com",
        name="User Email 2",
        password="password2"
    )
    with pytest.raises(Exception) as e_info:
        create_user(db=db_session, user_in=user_in_duplicate_email)
    assert "UNIQUE constraint failed" in str(e_info.value)
