# Voice API Testing Guide

## Overview
The voice recognition API has been successfully implemented using Groq's Whisper API.

## Available Endpoints

### 1. Basic Transcription
**Endpoint:** `POST /voice/transcribe`

Transcribe audio to text using Groq Whisper API.

**Parameters:**
- `audio` (file, required): Audio file (mp3, wav, m4a, ogg, webm, etc.)
- `language` (optional): ISO-639-1 language code (e.g., 'en', 'lg', 'sw')
- `temperature` (optional, default: 0.0): Sampling temperature (0-1)

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/voice/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "audio=@/path/to/your/audio.mp3" \
  -F "language=en" \
  -F "temperature=0.0"
```

**Response:**
```json
{
  "text": "Transcribed text here",
  "language": "en",
  "duration": 5.2
}
```

---

### 2. Transcribe and Translate
**Endpoint:** `POST /voice/transcribe-and-translate`

Transcribe audio and optionally translate to target language.

**Parameters:**
- `audio` (file, required): Audio file
- `translate_to` (optional): Target language code (e.g., 'eng', 'lug')
- `detect_language` (optional, default: true): Detect the source language

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/voice/transcribe-and-translate" \
  -H "Content-Type: multipart/form-data" \
  -F "audio=@/path/to/your/audio.mp3" \
  -F "translate_to=lug" \
  -F "detect_language=true"
```

**Response:**
```json
{
  "transcribed_text": "Original transcribed text",
  "detected_language": "en",
  "detected_language_name": "English",
  "translated_text": "Translated text in Luganda",
  "translation_target": "lug"
}
```

---

### 3. Get Supported Formats
**Endpoint:** `GET /voice/supported-formats`

Get list of supported audio formats.

**Example using cURL:**
```bash
curl -X GET "http://localhost:8000/voice/supported-formats"
```

**Response:**
```json
{
  "formats": ["mp3", "wav", "m4a", "ogg", "webm", "mp4", "mpeg", "mpga"],
  "recommended": ["mp3", "wav", "m4a", "ogg"]
}
```

---

## Testing with Python

```python
import requests

# Test basic transcription
with open("audio.mp3", "rb") as f:
    files = {"audio": f}
    data = {"language": "en", "temperature": 0.0}
    response = requests.post(
        "http://localhost:8000/voice/transcribe",
        files=files,
        data=data
    )
    print(response.json())

# Test transcribe and translate
with open("audio.mp3", "rb") as f:
    files = {"audio": f}
    data = {"translate_to": "lug", "detect_language": True}
    response = requests.post(
        "http://localhost:8000/voice/transcribe-and-translate",
        files=files,
        data=data
    )
    print(response.json())
```

---

## Testing with JavaScript/Fetch

```javascript
// Test basic transcription
const formData = new FormData();
formData.append('audio', audioFile);
formData.append('language', 'en');
formData.append('temperature', '0.0');

const response = await fetch('http://localhost:8000/voice/transcribe', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

---

## Features

✅ **Speech-to-Text**: Convert audio to text using Whisper
✅ **Multi-language Support**: Supports English, Luganda, Swahili, and other languages
✅ **Language Detection**: Automatically detect spoken language
✅ **Translation Integration**: Combine transcription with Sunbird translation
✅ **Multiple Audio Formats**: mp3, wav, m4a, ogg, webm, mp4, mpeg, mpga

---

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Look for the "Voice Services" section in the documentation.
