# Database Setup Guide

## Quick Start

The MzeeChakula backend uses SQLAlchemy with Supabase PostgreSQL. Database tables are automatically created when the application starts.

## Automatic Table Creation

Tables are created automatically on first run using SQLAlchemy's `create_all()` method. No manual migration needed for initial setup.

### Tables Created:
- **users** - User accounts with authentication
- **conversations** - Chat conversation history
- **messages** - Individual chat messages

## Manual Setup (if needed)

If you need to manually create tables, use Python:

```python
from api.models.database import Base, engine
from api.models.user import UserDB
from api.models.chat import ConversationDB, MessageDB

# Create all tables
Base.metadata.create_all(bind=engine)
```

## Environment Variables

Set your database connection in `.env`:

```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

For Supabase:
```bash
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
```

## Alembic Migrations (Optional)

Alembic is configured but optional. The manual migration script is available at:
`alembic/versions/001_initial_schema.py`

To use Alembic:
```bash
# Check current version
alembic current

# Apply migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

## Troubleshooting

### Tables Not Created
If tables aren't auto-created, check:
1. DATABASE_URL is set correctly
2. Database is accessible
3. User has CREATE TABLE permissions

### Reset Database
To drop and recreate all tables:
```python
from api.models.database import Base, engine

# WARNING: This deletes all data!
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```

## Production Deployment

For production on Cloud Run:
1. Set DATABASE_URL in Cloud Run environment variables
2. Tables will be created on first deployment
3. Use Alembic for schema changes in production
