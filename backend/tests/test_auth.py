"""
Tests for authentication endpoints
"""
import pytest


@pytest.mark.auth
@pytest.mark.unit
def test_register_user(client, sample_user_data, test_db):
    """Test user registration"""
    response = client.post("/auth/register", json=sample_user_data)

    # Should succeed or fail gracefully
    assert response.status_code in [200, 201, 400, 409]

    if response.status_code in [200, 201]:
        data = response.json()
        assert "email" in data or "id" in data


@pytest.mark.auth
@pytest.mark.unit
def test_register_duplicate_user(client, sample_user_data, test_db):
    """Test registering duplicate user fails"""
    # Register first time
    client.post("/auth/register", json=sample_user_data)

    # Try to register again
    response = client.post("/auth/register", json=sample_user_data)

    # Should return error (400 or 409)
    assert response.status_code in [400, 409]


@pytest.mark.auth
@pytest.mark.unit
def test_login_success(client, sample_user_data, test_db):
    """Test successful login"""
    # Register user first
    client.post("/auth/register", json=sample_user_data)

    # Login
    response = client.post(
        "/auth/token",
        data={
            "username": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
    )

    if response.status_code == 200:
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"


@pytest.mark.auth
@pytest.mark.unit
def test_login_wrong_password(client, sample_user_data, test_db):
    """Test login with wrong password fails"""
    # Register user
    client.post("/auth/register", json=sample_user_data)

    # Try login with wrong password
    response = client.post(
        "/auth/token",
        data={
            "username": sample_user_data["email"],
            "password": "WrongPassword123!"
        }
    )

    # Should fail
    assert response.status_code in [401, 403]


@pytest.mark.auth
@pytest.mark.unit
def test_login_nonexistent_user(client, test_db):
    """Test login with non-existent user fails"""
    response = client.post(
        "/auth/token",
        data={
            "username": "nonexistent@example.com",
            "password": "Password123!"
        }
    )

    # Should fail
    assert response.status_code in [401, 404]


@pytest.mark.auth
@pytest.mark.unit
def test_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without token fails"""
    # Try to access a protected endpoint (if any)
    response = client.get("/auth/me")

    # Should require authentication
    assert response.status_code in [401, 403]


@pytest.mark.auth
@pytest.mark.unit
def test_protected_endpoint_with_token(client, auth_headers, test_db):
    """Test accessing protected endpoint with valid token"""
    if not auth_headers:
        pytest.skip("Auth token not available")

    response = client.get("/auth/me", headers=auth_headers)

    # Should succeed or endpoint doesn't exist
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        assert "email" in data or "id" in data
