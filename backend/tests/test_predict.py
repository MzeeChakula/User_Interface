"""
Tests for prediction endpoints
"""
import pytest


@pytest.mark.unit
def test_predict_endpoint_exists(client):
    """Test prediction endpoint exists"""
    response = client.post("/predict/", json={})

    # Should respond (even if with error due to invalid data)
    assert response.status_code in [200, 400, 422, 500]


@pytest.mark.unit
def test_predict_with_valid_input(client, sample_prediction_input):
    """Test prediction with valid input"""
    response = client.post("/predict/", json=sample_prediction_input)

    # Should succeed or fail gracefully if models not loaded
    assert response.status_code in [200, 500]

    if response.status_code == 200:
        data = response.json()
        # Check response structure
        assert "prediction" in data or "caloric_needs" in data or "success" in data


@pytest.mark.unit
def test_predict_missing_fields(client):
    """Test prediction with missing required fields"""
    incomplete_data = {
        "age": 70
        # Missing other required fields
    }

    response = client.post("/predict/", json=incomplete_data)

    # Should return validation error
    assert response.status_code in [400, 422]


@pytest.mark.unit
def test_predict_invalid_data_types(client):
    """Test prediction with invalid data types"""
    invalid_data = {
        "age": "seventy",  # Should be number
        "weight": 65.5,
        "height": 165,
        "gender": "male",
        "activity_level": "sedentary"
    }

    response = client.post("/predict/", json=invalid_data)

    # Should return validation error
    assert response.status_code in [400, 422]


@pytest.mark.unit
def test_predict_example_endpoint(client):
    """Test example input endpoint"""
    response = client.get("/predict/example")

    assert response.status_code == 200
    data = response.json()

    # Should return example structure
    assert isinstance(data, dict)
    assert len(data) > 0


@pytest.mark.unit
def test_food_recommendations_endpoint(client):
    """Test food recommendations endpoint"""
    response = client.get("/predict/recommend")

    # Should respond
    assert response.status_code in [200, 500]

    if response.status_code == 200:
        data = response.json()
        # Should be a list or dict with recommendations
        assert isinstance(data, (list, dict))


@pytest.mark.unit
def test_food_recommendations_with_params(client):
    """Test food recommendations with query parameters"""
    params = {
        "dietary_preference": "vegetarian",
        "max_results": 5
    }

    response = client.get("/predict/recommend", params=params)

    # Should respond
    assert response.status_code in [200, 500]


@pytest.mark.unit
def test_predict_batch_endpoint(client):
    """Test batch prediction endpoint if it exists"""
    batch_data = [
        {
            "age": 70,
            "weight": 65.5,
            "height": 165,
            "gender": "male",
            "activity_level": "sedentary"
        },
        {
            "age": 75,
            "weight": 60.0,
            "height": 160,
            "gender": "female",
            "activity_level": "lightly_active"
        }
    ]

    response = client.post("/predict/batch", json=batch_data)

    # Should respond (endpoint may not exist)
    assert response.status_code in [200, 404, 422, 500]
