import pytest
from sqlalchemy.exc import IntegrityError
from app.db.models.user_model import User
from app.db.models.role_model import Role

def test_create_user(db_session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hasedhpassword",
        legal_name="Test User",
        preferred_name="Tester",
        is_active=True,
        is_superuser=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.legal_name == "Test User"
    assert user.preferred_name == "Tester"
    assert user.is_active is True

def test_user_unique_username(db_session):
    user1 = User(
        username="uniqueuser",
        email="user1@example.com",
        hashed_password="hashedpassword",
        legal_name="Test User"
    )
    user2 = User(
        username="uniqueuser",
        email="user1@example.com",
        hashed_password="hashedpassword",
        legal_name="Test User 2"
    )

    db_session.add(user1)
    db_session.commit()

    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

def test_user_roles_relationship(db_session):
    role_admin = Role(name="admin", description="Administrator")
    role_user = Role(name="user", description="Regular User")
    db_session.add_all([role_admin, role_user])
    db_session.commit()

    user = User(
        username="testuserroles",
        email="testuserroles@example.com",
        hashed_password="hashedpassword",
        legal_name="Test User"
    )
    user.roles.extend([role_admin, role_user])
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert len(user.roles) == 2
    role_names = [role.name for role in user.roles]
    assert "admin" in role_names
    assert "user" in role_names