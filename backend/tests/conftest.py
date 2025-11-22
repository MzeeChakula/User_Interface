"""
Pytest configuration and fixtures for backend tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import sys
import os

# Set test environment variables before importing app
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["GROQ_API_KEY"] = "test-groq-key"
os.environ["SUNBIRD_API_KEY"] = "test-sunbird-key"
os.environ["HUGGINGFACE_TOKEN"] = "test-hf-token"
os.environ["TAVILY_API_KEY"] = "test-tavily-key"
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_KEY"] = "test-supabase-key"

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app
from api.models.database import Base, get_db


# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    """Get test database session"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def override_get_db():
    """Override database dependency"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    """Create test client"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for tests"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "name": "Test User"
    }


@pytest.fixture
def sample_prediction_input():
    """Sample prediction input data"""
    return {
        "Energy_kcal_per_serving": 350,
        "Protein_g_per_serving": 15,
        "Fat_g_per_serving": 10,
        "Carbohydrates_g_per_serving": 45,
        "Fiber_g_per_serving": 5,
        "Calcium_mg_per_serving": 200,
        "Iron_mg_per_serving": 3,
        "Zinc_mg_per_serving": 2,
        "VitaminA_ug_per_serving": 500,
        "VitaminC_mg_per_serving": 20,
        "Potassium_mg_per_serving": 400,
        "Magnesium_mg_per_serving": 50,
        "region_encoded": 0,
        "condition_encoded": 0,
        "age_group_encoded": 1,
        "season_encoded": 0,
        "portion_size_g": 250,
        "estimated_cost_ugx": 5000
    }


@pytest.fixture
def auth_token(client, test_db, sample_user_data):
    """Get auth token for authenticated tests"""
    # Register user
    client.post("/auth/register", json=sample_user_data)

    # Login to get token
    response = client.post(
        "/auth/token",
        data={
            "username": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    return None


@pytest.fixture
def auth_headers(auth_token):
    """Get auth headers for authenticated requests"""
    if auth_token:
        return {"Authorization": f"Bearer {auth_token}"}
    return {}
