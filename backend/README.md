# Mzee Chakula Backend API

AI-powered nutritional assistant backend for elderly care in Uganda.

## Architecture

- **Framework**: FastAPI
- **Database**: PostgreSQL (primary), Neo4j (knowledge graph)
- **AI Services**: Groq (LLM), Sunbird AI (translation), LangChain (RAG)
- **Deployment**: Docker + Google Cloud Run

## Directory Structure

```
backend/
├── api/
│   ├── routers/          # API endpoints
│   ├── models/           # Data models & ML
│   ├── services/         # AI service integrations
│   ├── core/             # Configuration & security
│   └── utils/            # Helper functions
├── docker/               # Container configuration
├── tests/                # Test suite
├── alembic/              # Database migrations
└── requirements.txt      # Python dependencies
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start development server:
```bash
uvicorn api.main:app --reload
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Status

- ✓ Base structure migrated from model testing
- ✓ Docker configuration ready
- ⚙️ Authentication system (in progress)
- ⚙️ Chat system (in progress)
- ⚙️ AI orchestration (in progress)

See `progress.txt` in project root for detailed status.
