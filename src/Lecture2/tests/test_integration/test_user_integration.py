import pytest
from httpx import AsyncClient
from app.main import app
from app.dependencies import get_db
from app.db.models.user_model import User

from tests.conftest import override_get_db, override_get_current_user

@pytest.mark.anyio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "name": "New User",
            "password": "securepassword"
        }
        response = await ac.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data

    # Verify user is in the database
    db = next(override_get_db())
    user_in_db = db.query(User).filter(User.username == "newuser").first()
    assert user_in_db is not None
    assert user_in_db.email == "newuser@example.com"

@pytest.mark.anyio
async def test_reigster_user_existing_username():
    # Create initial user
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        user_data = {
            "username": "duplicateuser",
            "email": "duplicateuser1@example.com",
            "legal_name": "Duplicate User 1",
            "password": "securepassword"
        }
        response = await ac.post("/users/", json=user_data)
    assert response.status_code == 400  # Bad Request
    data = response.json()
    assert "Username already exists" in data["detail"]

@pytest.mark.anyio
async def test_user_login():
    # First create a test user directly in the database
    db = next(override_get_db())
    user = User(
        username="loginuser",
        email="loginuser@example.com",
        hashed_password="$2b$12$KIXR/3qJiQvsF2BMEY.n0e7Ib4lV0Vl3N9jXBbBxF0uB5wL7pItaG",  # Hashed 'securepassword'
        legal_name="Login User",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Attempt to log in
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        login_data = {
            "username": "loginuser",
            "password": "securepassword"
        }
        response = await ac.post("/login/access-token", data=login_data)
        assert response.status_code == 200, response.text
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

@pytest.mark.anyio
async def test_get_current_user():
    # Authenticate user and get access token
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        login_data = {
            "username": "testuser",
            "password": "securepassword"
        }
        response = await ac.post("/login/access-token", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]

        # Access protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

@pytest.mark.anyio
async def test_update_user():
    # Authenticate user and get access token
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        login_data = {
            "username": "testuser",
            "password": "securepassword"
        }
        response = await ac.post("/login/access-token", data=login_data)
        token = response.json()["access_token"]

        # Update user data
        headers = {"Authorization": f"Bearer {token}"}
        update_data = {
            "email": "updateduser@example.com",
            "legal_name": "Updated User"
        }
        response = await ac.put("/user/me", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updateduser@example.com"
    assert data["legal_name"] == "Updated User"

    # Verify update in database
    db = next(override_get_db())
    user_in_db = db.query(User).filter(User.username == "testuser").first()
    assert user_in_db.email == "updateduser@example.com"
    assert user_in_db.legal_name == "Updated User"

@pytest.mark.anyio
async def test_delete_user():
    # Authenticate user and get access token
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        login_data = {
            "username": "testuser",
            "password": "securepassword"
        }
        response = await ac.post("/login/access-token", data=login_data)
        token = response.json()["access_token"]

        # Delete user
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.delete("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "User deleted"

    # Verify deletion in database
    db = next(override_get_db())
    user_in_db = db.query(User).filter(User.username == 'testuser').first()
    assert user_in_db is None

@pytest.mark.anyio
async def test_get_user_by_id():
    # Create test user directly in database
    db = next(override_get_db())
    user = User(
        username="retrieveuser",
        email="retrieveuser@example.com",
        hashed_password="hashedpassword",
        name="Retrieve User",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Retriee use via API
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get(f"/users/{user.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "retrieveuser"
        assert data["email"] == "retrieveuser@example.com"

async def test_get_users_list():
    # Ensure there are users in the database
    db = next(override_get_db())
    users = [
        User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            hashed_password="hashedpassword",
        )
        for i in range(1, 4)
    ]
    db.add_all(users)
    db.commit()

    # Retrieve users via API
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3  # There may be more users depending on other tests