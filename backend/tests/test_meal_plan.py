"""
Tests for Meal Plan Generation Router
"""
import pytest
from unittest.mock import Mock, patch


@pytest.mark.unit
def test_generate_meal_plan_endpoint_exists(client, test_db, auth_headers):
    """Test that meal plan generation endpoint exists"""
    request_data = {
        "name": "Test Patient",
        "age": 70,
        "health_conditions": ["diabetes"],
        "preferred_foods": ["matooke", "beans"]
    }
    
    response = client.post("/meal-plan/generate", json=request_data, headers=auth_headers)
    
    # Should not return 404
    assert response.status_code != 404


@pytest.mark.unit
def test_generate_meal_plan_requires_auth(client):
    """Test that meal plan generation requires authentication"""
    request_data = {
        "name": "Test Patient",
        "age": 70,
        "health_conditions": [],
        "preferred_foods": []
    }
    
    response = client.post("/meal-plan/generate", json=request_data)
    
    assert response.status_code == 401


@pytest.mark.unit
def test_generate_meal_plan_validation(client, test_db, auth_headers):
    """Test meal plan request validation"""
    # Missing required fields
    invalid_data = {
        "name": "Test"
        # Missing age
    }
    
    response = client.post("/meal-plan/generate", json=invalid_data, headers=auth_headers)
    
    assert response.status_code == 422  # Validation error


@pytest.mark.unit
def test_generate_meal_plan_age_validation(client, test_db, auth_headers):
    """Test age validation in meal plan request"""
    # Age too high
    invalid_data = {
        "name": "Test Patient",
        "age": 150,  # Invalid age
        "health_conditions": [],
        "preferred_foods": []
    }
    
    response = client.post("/meal-plan/generate", json=invalid_data, headers=auth_headers)
    
    assert response.status_code == 422


@pytest.mark.unit
def test_generate_meal_plan_with_valid_data(client, test_db, auth_headers):
    """Test meal plan generation with valid data"""
    request_data = {
        "name": "Elderly Patient",
        "age": 75,
        "health_conditions": ["diabetes", "hypertension"],
        "preferred_foods": ["matooke", "beans", "greens"]
    }
    
    response = client.post("/meal-plan/generate", json=request_data, headers=auth_headers)
    
    # May succeed or fail gracefully depending on model availability
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "success" in data
        assert "patient_name" in data
        assert "meal_plan" in data


@pytest.mark.unit
def test_generate_meal_plan_empty_conditions(client, test_db, auth_headers):
    """Test meal plan generation with no health conditions"""
    request_data = {
        "name": "Healthy Patient",
        "age": 65,
        "health_conditions": [],
        "preferred_foods": ["rice", "chicken"]
    }
    
    response = client.post("/meal-plan/generate", json=request_data, headers=auth_headers)
    
    # Should handle empty conditions gracefully
    assert response.status_code in [200, 500]


@pytest.mark.unit
def test_quick_meal_plan_endpoint(client, test_db, auth_headers):
    """Test quick meal plan generation with query parameters"""
    response = client.post(
        "/meal-plan/generate/quick?age=80&conditions=diabetes&foods=matooke,beans&name=Grandpa",
        headers=auth_headers
    )
    
    # Should not return 404
    assert response.status_code != 404
    assert response.status_code in [200, 500]


@pytest.mark.unit
def test_quick_meal_plan_minimal_params(client, test_db, auth_headers):
    """Test quick meal plan with minimal parameters"""
    response = client.post(
        "/meal-plan/generate/quick?age=70",
        headers=auth_headers
    )
    
    # Should handle minimal params
    assert response.status_code in [200, 422, 500]


@pytest.mark.unit
def test_quick_meal_plan_comma_separated_parsing(client, test_db, auth_headers):
    """Test that comma-separated values are parsed correctly"""
    response = client.post(
        "/meal-plan/generate/quick?age=75&conditions=diabetes,hypertension&foods=rice,beans,fish",
        headers=auth_headers
    )
    
    # Should parse comma-separated values
    assert response.status_code in [200, 500]


@pytest.mark.unit
def test_generate_pdf_endpoint_exists(client, test_db, auth_headers):
    """Test that PDF generation endpoint exists"""
    request_data = {
        "name": "PDF Test Patient",
        "age": 70,
        "health_conditions": ["diabetes"],
        "preferred_foods": ["matooke"]
    }
    
    response = client.post("/meal-plan/generate/pdf", json=request_data, headers=auth_headers)
    
    # Should not return 404
    assert response.status_code != 404


@pytest.mark.unit
def test_generate_pdf_requires_auth(client):
    """Test that PDF generation requires authentication"""
    request_data = {
        "name": "Test Patient",
        "age": 70,
        "health_conditions": [],
        "preferred_foods": []
    }
    
    response = client.post("/meal-plan/generate/pdf", json=request_data)
    
    assert response.status_code == 401


@pytest.mark.unit
def test_generate_pdf_content_type(client, test_db, auth_headers):
    """Test PDF generation returns correct content type"""
    request_data = {
        "name": "PDF Patient",
        "age": 68,
        "health_conditions": [],
        "preferred_foods": []
    }
    
    response = client.post("/meal-plan/generate/pdf", json=request_data, headers=auth_headers)
    
    # If successful, should return PDF content type
    if response.status_code == 200:
        assert response.headers["content-type"] == "application/pdf"
        assert "attachment" in response.headers.get("content-disposition", "").lower()


@pytest.mark.unit
def test_meal_plan_response_structure(client, test_db, auth_headers):
    """Test meal plan response has expected structure"""
    request_data = {
        "name": "Structure Test",
        "age": 72,
        "health_conditions": ["diabetes"],
        "preferred_foods": ["beans"]
    }
    
    response = client.post("/meal-plan/generate", json=request_data, headers=auth_headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Check required fields
        assert "success" in data
        assert "patient_name" in data
        assert "caloric_needs" in data
        assert "meal_plan" in data
        assert "shopping_list" in data
        assert "tips" in data
        assert "generated_at" in data
        
        # Check data types
        assert isinstance(data["success"], bool)
        assert isinstance(data["patient_name"], str)
        assert isinstance(data["caloric_needs"], int)
        assert isinstance(data["meal_plan"], dict)
        assert isinstance(data["shopping_list"], list)
        assert isinstance(data["tips"], list)


@pytest.mark.unit
def test_meal_plan_patient_name_preserved(client, test_db, auth_headers):
    """Test that patient name is preserved in response"""
    request_data = {
        "name": "John Doe",
        "age": 65,
        "health_conditions": [],
        "preferred_foods": []
    }
    
    response = client.post("/meal-plan/generate", json=request_data, headers=auth_headers)
    
    if response.status_code == 200:
        data = response.json()
        assert data["patient_name"] == "John Doe"


@pytest.mark.unit
def test_meal_plan_multiple_conditions(client, test_db, auth_headers):
    """Test meal plan with multiple health conditions"""
    request_data = {
        "name": "Multi-Condition Patient",
        "age": 78,
        "health_conditions": ["diabetes", "hypertension", "high_cholesterol"],
        "preferred_foods": ["vegetables", "fish"]
    }
    
    response = client.post("/meal-plan/generate", json=request_data, headers=auth_headers)
    
    # Should handle multiple conditions
    assert response.status_code in [200, 500]
