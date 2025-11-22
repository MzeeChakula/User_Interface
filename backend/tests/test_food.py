"""
Tests for Food Database Router
"""
import pytest
import io
from fastapi import status


@pytest.mark.unit
def test_create_food(client, auth_headers, test_db):
    """Test creating a new food entry"""
    food_data = {
        "name": "Matooke",
        "local_name": "Matooke",
        "category": "Staples",
        "calories": 122.0,
        "protein": 1.3,
        "carbs": 31.2,
        "fats": 0.4,
        "fiber": 2.6,
        "is_diabetic_friendly": True,
        "is_hypertension_friendly": True,
        "description": "Green cooking bananas, a staple food in Uganda"
    }
    
    response = client.post("/foods/", json=food_data, headers=auth_headers)
    
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["name"] == "Matooke"
    assert data["category"] == "Staples"
    assert "id" in data


@pytest.mark.unit
def test_create_duplicate_food(client, auth_headers, test_db):
    """Test creating duplicate food returns error"""
    food_data = {
        "name": "Beans",
        "category": "Legumes",
        "calories": 127.0,
        "protein": 8.7,
        "carbs": 22.8,
        "fats": 0.5
    }
    
    # Create first time
    client.post("/foods/", json=food_data, headers=auth_headers)
    
    # Try to create duplicate
    response = client.post("/foods/", json=food_data, headers=auth_headers)
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.unit
def test_create_food_without_auth(client, test_db):
    """Test creating food without authentication fails"""
    food_data = {
        "name": "Test Food",
        "category": "Test",
        "calories": 100.0,
        "protein": 5.0,
        "carbs": 10.0,
        "fats": 2.0
    }
    
    response = client.post("/foods/", json=food_data)
    
    assert response.status_code == 401


@pytest.mark.unit
def test_bulk_import_foods(client, test_db, auth_headers):
    """Test bulk importing foods from JSON"""
    bulk_data = {
        "foods": [
            {
                "name": "Rice",
                "category": "Staples",
                "calories": 130.0,
                "protein": 2.7,
                "carbs": 28.2,
                "fats": 0.3
            },
            {
                "name": "Chicken",
                "category": "Protein",
                "calories": 165.0,
                "protein": 31.0,
                "carbs": 0.0,
                "fats": 3.6
            }
        ]
    }
    
    response = client.post("/foods/bulk", json=bulk_data, headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["created"] == 2
    assert data["skipped"] == 0


@pytest.mark.unit
def test_bulk_import_with_duplicates(client, test_db, auth_headers):
    """Test bulk import handles duplicates correctly"""
    # First import
    bulk_data = {
        "foods": [
            {
                "name": "Cassava",
                "category": "Staples",
                "calories": 160.0,
                "protein": 1.4,
                "carbs": 38.1,
                "fats": 0.3
            }
        ]
    }
    client.post("/foods/bulk", json=bulk_data, headers=auth_headers)
    
    # Second import with same food
    bulk_data["foods"].append({
        "name": "Sweet Potato",
        "category": "Staples",
        "calories": 86.0,
        "protein": 1.6,
        "carbs": 20.1,
        "fats": 0.1
    })
    
    response = client.post("/foods/bulk", json=bulk_data, headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["created"] == 1  # Only Sweet Potato
    assert data["skipped"] == 1  # Cassava skipped


@pytest.mark.unit
def test_search_foods_by_name(client, test_db, auth_headers):
    """Test searching foods by name"""
    # Create test foods
    foods = [
        {"name": "Green Beans", "category": "Vegetables", "calories": 31.0, "protein": 1.8, "carbs": 7.0, "fats": 0.2},
        {"name": "Green Peas", "category": "Vegetables", "calories": 81.0, "protein": 5.4, "carbs": 14.5, "fats": 0.4}
    ]
    for food in foods:
        client.post("/foods/", json=food, headers=auth_headers)
    
    # Search for "green"
    response = client.get("/foods/search?query=green", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all("green" in item["name"].lower() for item in data)


@pytest.mark.unit
def test_search_foods_by_category(client, test_db, auth_headers):
    """Test searching foods by category"""
    # Create test foods
    foods = [
        {"name": "Spinach", "category": "Vegetables", "calories": 23.0, "protein": 2.9, "carbs": 3.6, "fats": 0.4},
        {"name": "Beef", "category": "Protein", "calories": 250.0, "protein": 26.0, "carbs": 0.0, "fats": 15.0}
    ]
    for food in foods:
        client.post("/foods/", json=food, headers=auth_headers)
    
    # Search by category
    response = client.get("/foods/search?category=Vegetables", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(item["category"] == "Vegetables" for item in data)


@pytest.mark.unit
def test_search_foods_diabetic_friendly(client, test_db, auth_headers):
    """Test searching for diabetic-friendly foods"""
    # Create test foods
    foods = [
        {
            "name": "Oats",
            "category": "Staples",
            "calories": 68.0,
            "protein": 2.4,
            "carbs": 12.0,
            "fats": 1.4,
            "is_diabetic_friendly": True
        },
        {
            "name": "White Bread",
            "category": "Staples",
            "calories": 265.0,
            "protein": 9.0,
            "carbs": 49.0,
            "fats": 3.2,
            "is_diabetic_friendly": False
        }
    ]
    for food in foods:
        client.post("/foods/", json=food, headers=auth_headers)
    
    # Search for diabetic-friendly
    response = client.get("/foods/search?diabetic_friendly=true", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(item["is_diabetic_friendly"] is True for item in data)


@pytest.mark.unit
def test_get_categories(client, test_db, auth_headers):
    """Test getting all food categories"""
    # Create foods in different categories
    foods = [
        {"name": "Food1", "category": "Fruits", "calories": 50.0, "protein": 1.0, "carbs": 12.0, "fats": 0.2},
        {"name": "Food2", "category": "Vegetables", "calories": 25.0, "protein": 2.0, "carbs": 5.0, "fats": 0.1},
        {"name": "Food3", "category": "Fruits", "calories": 60.0, "protein": 0.5, "carbs": 15.0, "fats": 0.1}
    ]
    for food in foods:
        client.post("/foods/", json=food, headers=auth_headers)
    
    response = client.get("/foods/categories", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert "Fruits" in data["categories"]
    assert "Vegetables" in data["categories"]


@pytest.mark.unit
def test_get_food_by_id(client, test_db, auth_headers):
    """Test getting a specific food by ID"""
    # Create a food
    food_data = {
        "name": "Mango",
        "category": "Fruits",
        "calories": 60.0,
        "protein": 0.8,
        "carbs": 15.0,
        "fats": 0.4
    }
    create_response = client.post("/foods/", json=food_data, headers=auth_headers)
    food_id = create_response.json()["id"]
    
    # Get by ID
    response = client.get(f"/foods/{food_id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mango"
    assert data["id"] == food_id


@pytest.mark.unit
def test_get_food_not_found(client, test_db, auth_headers):
    """Test getting non-existent food returns 404"""
    response = client.get("/foods/99999", headers=auth_headers)
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.unit
def test_delete_food(client, test_db, auth_headers):
    """Test deleting a food entry"""
    # Create a food
    food_data = {
        "name": "Test Delete Food",
        "category": "Test",
        "calories": 100.0,
        "protein": 5.0,
        "carbs": 10.0,
        "fats": 2.0
    }
    create_response = client.post("/foods/", json=food_data, headers=auth_headers)
    food_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/foods/{food_id}", headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["success"] is True
    
    # Verify it's deleted
    get_response = client.get(f"/foods/{food_id}", headers=auth_headers)
    assert get_response.status_code == 404


@pytest.mark.unit
def test_delete_food_not_found(client, test_db, auth_headers):
    """Test deleting non-existent food returns 404"""
    response = client.delete("/foods/99999", headers=auth_headers)
    
    assert response.status_code == 404


@pytest.mark.unit
def test_list_foods(client, test_db, auth_headers):
    """Test listing all foods with pagination"""
    # Create multiple foods
    for i in range(5):
        food_data = {
            "name": f"Food {i}",
            "category": "Test",
            "calories": 100.0 + i,
            "protein": 5.0,
            "carbs": 10.0,
            "fats": 2.0
        }
        client.post("/foods/", json=food_data, headers=auth_headers)
    
    # List all
    response = client.get("/foods/", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5


@pytest.mark.unit
def test_list_foods_pagination(client, test_db, auth_headers):
    """Test food listing pagination"""
    # Create multiple foods
    for i in range(10):
        food_data = {
            "name": f"Paginated Food {i}",
            "category": "Test",
            "calories": 100.0,
            "protein": 5.0,
            "carbs": 10.0,
            "fats": 2.0
        }
        client.post("/foods/", json=food_data, headers=auth_headers)
    
    # Get first page
    response = client.get("/foods/?skip=0&limit=5", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5
    
    # Get second page
    response2 = client.get("/foods/?skip=5&limit=5", headers=auth_headers)
    assert response2.status_code == 200
