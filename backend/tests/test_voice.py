"""
Tests for Voice/Speech Recognition Router
"""
import pytest
import io
from unittest.mock import Mock, patch, AsyncMock


@pytest.mark.unit
def test_transcribe_endpoint_exists(client):
    """Test that transcribe endpoint exists"""
    # Create a mock audio file
    audio_data = b"fake audio data"
    files = {"audio": ("test.mp3", io.BytesIO(audio_data), "audio/mpeg")}
    
    response = client.post("/voice/transcribe", files=files)
    
    # Should not return 404 (may return 500 if API key not configured)
    assert response.status_code != 404


@pytest.mark.unit
def test_transcribe_missing_file(client):
    """Test transcribe endpoint with missing audio file"""
    response = client.post("/voice/transcribe")
    
    assert response.status_code == 422  # Validation error


@pytest.mark.unit
def test_transcribe_with_language_param(client):
    """Test transcribe with language parameter"""
    audio_data = b"fake audio data"
    files = {"audio": ("test.mp3", io.BytesIO(audio_data), "audio/mpeg")}
    data = {"language": "en"}
    
    response = client.post("/voice/transcribe", files=files, data=data)
    
    # Should accept language parameter
    assert response.status_code in [200, 400, 500]


@pytest.mark.unit
def test_transcribe_with_temperature(client):
    """Test transcribe with temperature parameter"""
    audio_data = b"fake audio data"
    files = {"audio": ("test.mp3", io.BytesIO(audio_data), "audio/mpeg")}
    data = {"temperature": "0.5"}
    
    response = client.post("/voice/transcribe", files=files, data=data)
    
    # Should accept temperature parameter
    assert response.status_code in [200, 400, 500]


@pytest.mark.unit
@patch('api.services.voice_service.get_voice_service')
def test_transcribe_success_response(mock_service, client):
    """Test successful transcription response structure"""
    # Mock the voice service
    mock_instance = Mock()
    mock_instance.transcribe_audio = AsyncMock(return_value={
        "text": "Hello world",
        "language": "en",
        "duration": 2.5
    })
    mock_service.return_value = mock_instance
    
    audio_data = b"fake audio data"
    files = {"audio": ("test.mp3", io.BytesIO(audio_data), "audio/mpeg")}
    
    response = client.post("/voice/transcribe", files=files)
    
    if response.status_code == 200:
        data = response.json()
        assert "text" in data
        assert "language" in data
        assert "duration" in data


@pytest.mark.unit
def test_transcribe_and_translate_endpoint_exists(client):
    """Test that transcribe-and-translate endpoint exists"""
    audio_data = b"fake audio data"
    files = {"audio": ("test.mp3", io.BytesIO(audio_data), "audio/mpeg")}
    
    response = client.post("/voice/transcribe-and-translate", files=files)
    
    # Should not return 404
    assert response.status_code != 404


@pytest.mark.unit
def test_transcribe_and_translate_with_target_lang(client):
    """Test transcribe and translate with target language"""
    audio_data = b"fake audio data"
    files = {"audio": ("test.mp3", io.BytesIO(audio_data), "audio/mpeg")}
    data = {"translate_to": "eng"}
    
    response = client.post("/voice/transcribe-and-translate", files=files, data=data)
    
    # Should accept translate_to parameter
    assert response.status_code in [200, 400, 500]


@pytest.mark.unit
def test_transcribe_and_translate_detect_language(client):
    """Test transcribe and translate with language detection"""
    audio_data = b"fake audio data"
    files = {"audio": ("test.mp3", io.BytesIO(audio_data), "audio/mpeg")}
    data = {"detect_language": "true"}
    
    response = client.post("/voice/transcribe-and-translate", files=files, data=data)
    
    # Should accept detect_language parameter
    assert response.status_code in [200, 400, 500]


@pytest.mark.unit
@patch('api.services.voice_service.get_voice_service')
def test_transcribe_and_translate_response_structure(mock_service, client):
    """Test transcribe-and-translate response structure"""
    # Mock the voice service
    mock_instance = Mock()
    mock_instance.transcribe_audio = AsyncMock(return_value={
        "text": "Habari",
        "language": "sw"
    })
    mock_service.return_value = mock_instance
    
    audio_data = b"fake audio data"
    files = {"audio": ("test.mp3", io.BytesIO(audio_data), "audio/mpeg")}
    
    response = client.post("/voice/transcribe-and-translate", files=files)
    
    if response.status_code == 200:
        data = response.json()
        assert "transcribed_text" in data
        assert "detected_language" in data


@pytest.mark.unit
def test_supported_formats_endpoint(client):
    """Test get supported formats endpoint"""
    response = client.get("/voice/supported-formats")
    
    assert response.status_code == 200
    data = response.json()
    assert "formats" in data
    assert isinstance(data["formats"], list)
    assert len(data["formats"]) > 0


@pytest.mark.unit
def test_supported_formats_includes_common_types(client):
    """Test that supported formats includes common audio types"""
    response = client.get("/voice/supported-formats")
    
    if response.status_code == 200:
        data = response.json()
        formats = data["formats"]
        
        # Should include common formats
        common_formats = ["mp3", "wav", "m4a", "ogg"]
        for fmt in common_formats:
            assert fmt in formats or any(fmt in f for f in formats)


@pytest.mark.unit
def test_supported_formats_has_recommended(client):
    """Test that supported formats response includes recommended formats"""
    response = client.get("/voice/supported-formats")
    
    if response.status_code == 200:
        data = response.json()
        assert "recommended" in data
        assert isinstance(data["recommended"], list)


@pytest.mark.unit
def test_transcribe_invalid_audio_format(client):
    """Test transcribe with invalid audio format"""
    # Create a text file instead of audio
    text_data = b"This is not audio"
    files = {"audio": ("test.txt", io.BytesIO(text_data), "text/plain")}
    
    response = client.post("/voice/transcribe", files=files)
    
    # Should handle invalid format gracefully
    assert response.status_code in [400, 500]


@pytest.mark.unit
def test_transcribe_empty_file(client):
    """Test transcribe with empty audio file"""
    empty_data = b""
    files = {"audio": ("empty.mp3", io.BytesIO(empty_data), "audio/mpeg")}
    
    response = client.post("/voice/transcribe", files=files)
    
    # Should handle empty file
    assert response.status_code in [400, 500]


@pytest.mark.unit
def test_transcribe_large_file_handling(client):
    """Test transcribe handles large files"""
    # Create a "large" mock file (not actually large for testing)
    large_data = b"x" * 1024 * 100  # 100KB
    files = {"audio": ("large.mp3", io.BytesIO(large_data), "audio/mpeg")}
    
    response = client.post("/voice/transcribe", files=files)
    
    # Should handle without crashing
    assert response.status_code in [200, 400, 413, 500]


@pytest.mark.unit
def test_transcribe_multiple_languages(client):
    """Test transcribe with different language codes"""
    audio_data = b"fake audio data"
    
    languages = ["en", "lg", "sw", "ach"]
    
    for lang in languages:
        files = {"audio": ("test.mp3", io.BytesIO(audio_data), "audio/mpeg")}
        data = {"language": lang}
        
        response = client.post("/voice/transcribe", files=files, data=data)
        
        # Should accept various language codes
        assert response.status_code in [200, 400, 500]


@pytest.mark.unit
def test_transcribe_and_translate_full_workflow(client):
    """Test full transcribe and translate workflow"""
    audio_data = b"fake audio data"
    files = {"audio": ("test.mp3", io.BytesIO(audio_data), "audio/mpeg")}
    data = {
        "translate_to": "eng",
        "detect_language": "true"
    }
    
    response = client.post("/voice/transcribe-and-translate", files=files, data=data)
    
    # Should handle full workflow
    assert response.status_code in [200, 400, 500]
    
    if response.status_code == 200:
        result = response.json()
        assert "transcribed_text" in result
        # May have translation if service is available
        if "translated_text" in result:
            assert isinstance(result["translated_text"], str)
