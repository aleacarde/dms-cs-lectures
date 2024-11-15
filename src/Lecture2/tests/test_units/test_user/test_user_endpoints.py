import pytest
from app.db.models.user_model import User

@pytest.mark.anyio
async def test_create_user_endpoint(test_client):
    response = test_client.post(
        "/users/",
        json={
            "username": "endpointuser",
            "email": "endpointuser@example.com",
            "legal_name": "Endpoint User",
            "password": "securepassword"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "endpointuser"
    assert data["email"] == "endpointuser@example.com"
    assert data["legal_name"] == "Endpoint User"
    assert "id" in data

@pytest.mark.anyio
async def test_create_user_endpoint_missing_fields(test_client):
    response = test_client.post(
        "/users/",
        json={
            "username": "incompleteuser",
            "password": "password",
        }
    )
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "email"]

@pytest.mark.anyio
async def test_get_user_endpoint(test_client, db_session):
    # First, create a test user directly in the database
    user = User(
        username="getuser",
        email="getuser@example.com",
        hashed_password="hashedpassword",
        name="Get User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Now, retrieve the user via the endpoint
    response = test_client.get(f"/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["username"] == "getuser"
    assert data["email"] == "getuser@example.com"
    assert data["name"] == "Get User"

@pytest.mark.anyio
async def test_authenticate_user_endpoint(test_client):
    # Create user
    response = test_client.post(
        "/users/",
        json={
            "usrname": "authuser",
            "email": "authuser@example.com",
            "legal_name": "Auth User",
            "password": "securepassword"
        }
    )
    assert response.status_code == 200

    # Authenticate user
    response = test_client.post(
        "/login/access-token",
        data={
            "username": "authuser",
            "password": "securepassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.anyio
async def test_get_current_user_endpoint(test_client):
    # Create and authenticate user
    response = test_client.post(
        "/users/",
        json={
            "username": "currentuser",
            "email": "currentuser@example.com",
            "name": "Current User",
            "password": "securepassword"
        }
    )
    assert response.status_code == 200

    # Authenticate user
    response = test_client.post(
        "/login/access-token",
        data={
            "username": "currentuser",
            "password": "securepassword"
        }
    )
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]

    # Get current user
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "currentuser"
    assert data["email"] == "currentuser@example.com"
    assert data["legal_name"] == "Current User"

@pytest.mark.anyio
async def test_update_user_endpoint(test_client, db_session):
    # Create user
    user = User(
        username="updateuser",
        email="updateuser@example.com",
        hashed_password="hashedpassword",
        legal_name="Update User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Update user
    response = test_client.put(
        f"/users/{user.id}",
        json={
            "email": "updated@example.com",
            "legal_name": "Updated User",
            "preferred_name": "Updater"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"
    assert data["legal_name"] == "Updated User"
    assert data["preferred_name"] == "Updater"
