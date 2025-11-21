# Backend Tests

Comprehensive test suite for the MzeeChakula backend API.

## Test Structure

```
tests/
├── conftest.py           # Pytest configuration and fixtures
├── test_health.py        # Health check and metrics tests
├── test_auth.py          # Authentication tests
├── test_predict.py       # Prediction endpoint tests
├── test_chat.py          # Chat endpoint tests
├── test_ai.py            # AI service tests (translation, RAG)
└── test_model_loader.py  # ML model loader tests
```

## Running Tests

### Quick Start

```bash
# Run all tests
./run_tests.sh

# Or with pytest directly
pytest tests/ -v
```

### Run Specific Test Files

```bash
pytest tests/test_health.py -v
pytest tests/test_auth.py -v
pytest tests/test_predict.py -v
```

### Run by Markers

```bash
# Run only unit tests
pytest -m unit

# Run only auth tests
pytest -m auth

# Run model tests
pytest -m models
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Fast, isolated tests
- No external dependencies
- Test individual functions/endpoints

### Integration Tests (`@pytest.mark.integration`)
- Test multiple components together
- May require external services
- Slower than unit tests

### Slow Tests (`@pytest.mark.slow`)
- Tests that take longer to run
- Often involve ML model operations
- Can be skipped for quick testing: `pytest -m "not slow"`

## Test Fixtures

Available fixtures in `conftest.py`:

- `client` - FastAPI test client
- `test_db` - Test database session
- `sample_user_data` - Sample user registration data
- `sample_prediction_input` - Sample prediction input
- `auth_token` - JWT token for authenticated tests
- `auth_headers` - Authorization headers with Bearer token

## Environment Setup

Tests use a separate test environment with SQLite database.

Environment variables are set automatically in `conftest.py`:
- `DATABASE_URL=sqlite:///./test.db`
- `SECRET_KEY=test-secret-key`
- Dummy API keys for external services

## Expected Behavior

### Tests That Should Pass
- ✅ Health endpoint tests
- ✅ Metrics endpoint tests
- ✅ Model loader initialization
- ✅ Authentication flow (if database is configured)
- ✅ Prediction endpoint structure (even without models)

### Tests That May Fail (Expected)
- ⚠️ Chat tests (if GROQ_API_KEY not configured)
- ⚠️ Translation tests (if SUNBIRD_API_KEY not configured)
- ⚠️ RAG tests (if TAVILY_API_KEY not configured)
- ⚠️ Model predictions (if model files not in backend/models/)

**These failures are normal** and won't affect deployment as long as:
- The endpoints exist
- They handle errors gracefully
- They return appropriate status codes

## CI/CD Integration

Add to your CI/CD pipeline:

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest tests/ -m "unit" -v
```

## Coverage

Generate coverage report:

```bash
pytest tests/ --cov=api --cov-report=html
# Open htmlcov/index.html
```

## Writing New Tests

Example test structure:

```python
import pytest

@pytest.mark.unit
def test_my_feature(client):
    """Test description"""
    response = client.get("/my-endpoint")

    assert response.status_code == 200
    data = response.json()
    assert "expected_key" in data
```

## Troubleshooting

### Import Errors
If you see import errors, make sure you're in the backend directory and the virtual environment is activated:

```bash
cd backend
source .venv/bin/activate
```

### Database Errors
Tests use SQLite. If you see database errors:

```bash
rm test.db  # Remove old test database
pytest tests/ -v
```

### Module Not Found
Install test dependencies:

```bash
pip install pytest pytest-asyncio pytest-cov
```

## Test Coverage Goals

Current coverage targets:
- **Core endpoints**: >80% coverage
- **Auth logic**: >90% coverage
- **Model loader**: >70% coverage
- **Error handling**: >60% coverage

## Documentation

See individual test files for specific test documentation and examples.
