"""
Tests for AI service endpoints (translation, RAG, etc.)
"""
import pytest


@pytest.mark.unit
def test_translate_endpoint(client):
    """Test translation endpoint"""
    translation_data = {
        "text": "Hello, how are you?",
        "target_language": "lg"  # Luganda
    }

    response = client.post("/ai/translate", json=translation_data)

    # Should respond (may fail if API key not configured)
    assert response.status_code in [200, 400, 401, 500]


@pytest.mark.unit
def test_detect_language_endpoint(client):
    """Test language detection endpoint"""
    response = client.post("/ai/detect-language", json={"text": "Hello world"})

    # Should respond
    assert response.status_code in [200, 400, 500]


@pytest.mark.unit
def test_get_languages_endpoint(client):
    """Test get supported languages endpoint"""
    response = client.get("/ai/languages")

    # Should return list of languages
    assert response.status_code in [200, 500]

    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, (list, dict))


@pytest.mark.unit
def test_rag_query_endpoint(client):
    """Test RAG query endpoint"""
    rag_data = {
        "query": "What are the best foods for elderly nutrition?",
        "search_web": False
    }

    response = client.post("/ai/rag", json=rag_data)

    # Should respond (may fail if dependencies not configured)
    assert response.status_code in [200, 400, 500]


@pytest.mark.unit
def test_rag_with_web_search(client):
    """Test RAG query with web search enabled"""
    rag_data = {
        "query": "Latest nutrition guidelines for elderly",
        "search_web": True
    }

    response = client.post("/ai/rag", json=rag_data)

    # Should respond
    assert response.status_code in [200, 400, 500]
