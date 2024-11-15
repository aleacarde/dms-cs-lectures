import pytest
from pydantic import ValidationError
from app.schemas.user_schema import UserCreate, UserUpdate, UserOut

def test_user_create_schema():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "legal_name": "Test User",
        "preferred_name": "Tester",
        "password": "securepassword"
    }
    user = UserCreate(**user_data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.legal_name == "Test User"
    assert user.preferred_ame == "Tester"
    assert user.password == "securepassword"

def test_user_create_schema_missing_fields():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

def test_user_out_schema():
    user_data = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "legal_name": "Test User",
        "preferred_name": "Tester",
        "is_active": True,
        "is_superuser": False
    }
    user = UserOut(**user_data)
    assert user.id == 1
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.legal_name == "Test User"
    assert user.preferred_name == "Tester"
    assert user.is_active is True
    assert user.is_superuser is False