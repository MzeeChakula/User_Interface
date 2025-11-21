# MzeeChakula Backend API

FastAPI backend for the MzeeChakula nutrition assistant, providing AI-powered nutrition recommendations for elderly care in Uganda.

## Production Deployment

**Live API**: <https://mzeechakula-user-interface-backend.onrender.com>

**API Documentation**:

- Swagger UI: <https://mzeechakula-user-interface-backend.onrender.com/docs>
- ReDoc: <https://mzeechakula-user-interface-backend.onrender.com/redoc>
- Health Check: <https://mzeechakula-user-interface-backend.onrender.com/health>

## Features

- **JWT Authentication** - Secure user authentication with Supabase
- **AI Chat System** - LangChain + Groq LLM for conversational AI
- **Multilingual Translation** - Sunbird AI supporting 50+ African languages
- **RAG System** - ChromaDB + Tavily search for intelligent responses
- **Food Recommendations** - HuggingFace embeddings for similarity search
- **Nutrition Predictions** - Ensemble ML model for caloric needs
- **Docker Ready** - Containerized for easy deployment

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **Vector DB**: ChromaDB
- **LLM**: Groq (llama-3.3-70b-versatile)
- **Translation**: Sunbird AI
- **Embeddings**: HuggingFace
- **Search**: Tavily
- **Auth**: JWT with passlib

## Local Development

### Prerequisites

- Python 3.12+
- PostgreSQL (or Supabase account)
- API Keys (Groq, Sunbird, HuggingFace, Tavily)

### Setup

1. **Clone and navigate**:

```bash
cd User_Interface/backend
```

2.**Create virtual environment**:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3.**Install dependencies**:

```bash
pip install -r requirements.txt
```

4.**Configure environment**:

```bash
cp .env.example .env
# Edit .env with your API keys and database credentials
```

5.**Run the server**:

```bash
uvicorn api.main:app --reload
```

### Local API Documentation

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- Health Check: <http://localhost:8000/health>

## API Endpoints

### Authentication

- `POST /auth/register` - User registration
- `POST /auth/token` - Login and get JWT token

### Chat

- `POST /chat/message` - Send message to AI assistant

### AI Services

- `POST /ai/translate` - Translate text (50+ languages)
- `POST /ai/detect-language` - Detect language
- `GET /ai/languages` - List supported languages
- `POST /ai/rag` - RAG query with search

### Predictions

- `POST /predict/` - Predict caloric needs
- `POST /predict/batch` - Batch predictions
- `GET /predict/recommend` - Food recommendations
- `GET /predict/example` - Example input format

### Health & Monitoring

- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics

## Environment Variables

Required variables in `.env`:

```bash
# Database
DATABASE_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_KEY=...

# Security
SECRET_KEY=your-secret-key

# AI Services
GROQ_API_KEY=...
SUNBIRD_API_KEY=...
HUGGINGFACE_TOKEN=...
TAVILY_API_KEY=...

# Vector DB
CHROMA_PERSIST_DIR=./chroma_db
```

## Deployment

### Render (Current)

Deployed at: <https://mzeechakula-user-interface-backend.onrender.com>

Configuration files:

- `Procfile` - Startup command
- `render.yaml` - Infrastructure config
- `runtime.txt` - Python version

### Docker

```bash
# Build
docker build -t mzeechakula-backend .

# Run
docker run -p 8000:8000 --env-file .env mzeechakula-backend
```

### Docker Compose

```bash
docker-compose up
```

## Project Structure

```bash
backend/
├── api/
│   ├── main.py              # FastAPI app
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   └── security.py      # JWT & auth
│   ├── models/
│   │   ├── loader.py        # ML model loader
│   │   ├── user.py          # User models
│   │   └── chat.py          # Chat models
│   ├── routers/
│   │   ├── auth.py          # Authentication
│   │   ├── chat.py          # Chat endpoints
│   │   ├── ai.py            # AI services
│   │   └── predict.py       # Predictions
│   └── services/
│       ├── llm_service.py   # LangChain LLM
│       ├── sunbird.py       # Translation
│       └── rag_service.py   # RAG system
├── docs/                    # Documentation
├── requirements.txt         # Dependencies
├── Dockerfile              # Docker config
└── README.md               # This file
```

## Documentation

- [Database Setup](docs/DATABASE_SETUP.md)
- [HuggingFace Model](docs/HUGGINGFACE_MODEL.md)
- [Embeddings Implementation](docs/EMBEDDINGS_IMPLEMENTATION.md)

## Support

- **Issues**: GitHub Issues
- **API Docs**: <https://mzeechakula-user-interface-backend.onrender.com/docs>
- **Health Status**: <https://mzeechakula-user-interface-backend.onrender.com/health>

## License

MIT License - See LICENSE file for details
