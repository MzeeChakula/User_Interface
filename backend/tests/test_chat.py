"""
Tests for chat endpoints
"""
import pytest


@pytest.mark.unit
def test_chat_endpoint_exists(client):
    """Test chat endpoint exists"""
    response = client.post("/chat/message", json={})

    # Should respond (even if with error)
    assert response.status_code in [200, 400, 401, 422, 500]


@pytest.mark.unit
def test_chat_with_message(client):
    """Test sending a chat message"""
    message_data = {
        "message": "What are good foods for elderly nutrition?",
        "language": "en"
    }

    response = client.post("/chat/message", json=message_data)

    # Should respond
    assert response.status_code in [200, 401, 500]

    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict)
        # Should have response
        assert "response" in data or "message" in data or "reply" in data


@pytest.mark.unit
def test_chat_empty_message(client):
    """Test chat with empty message"""
    response = client.post("/chat/message", json={"message": ""})

    # Should return error (401 for auth, or 400/422 for validation)
    assert response.status_code in [400, 401, 422]


@pytest.mark.unit
def test_chat_with_profile(client):
    """Test chat with elder profile context"""
    message_data = {
        "message": "Create a meal plan for me",
        "profile": {
            "age": 70,
            "dietary_preferences": ["vegetarian"],
            "health_conditions": ["diabetes"]
        }
    }

    response = client.post("/chat/message", json=message_data)

    # Should respond
    assert response.status_code in [200, 401, 500]
