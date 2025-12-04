"""
Food Database Management Router
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import csv
import io

from api.models.food import (
    FoodDB, Food, FoodCreate, FoodSearch, BulkFoodImport
)
from api.models.database import get_db
from api.models.user import UserDB
from api.core.deps import get_current_user

router = APIRouter(
    prefix="/foods",
    tags=["Food Database"],
)


@router.post("/", response_model=Food)
async def create_food(
    food: FoodCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Create a new food entry"""
    # Check if food already exists
    existing = db.query(FoodDB).filter(FoodDB.name == food.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Food already exists")

    db_food = FoodDB(**food.model_dump())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


@router.post("/bulk", response_model=dict)
async def bulk_import_foods(
    import_data: BulkFoodImport,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Bulk import foods from JSON"""
    created = 0
    skipped = 0
    errors = []

    for food_data in import_data.foods:
        try:
            # Check if exists
            existing = db.query(FoodDB).filter(FoodDB.name == food_data.name).first()
            if existing:
                skipped += 1
                continue

            db_food = FoodDB(**food_data.model_dump())
            db.add(db_food)
            created += 1
        except Exception as e:
            errors.append(f"Error importing {food_data.name}: {str(e)}")

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Bulk import failed: {str(e)}")

    return {
        "success": True,
        "created": created,
        "skipped": skipped,
        "errors": errors
    }


@router.post("/import-csv")
async def import_from_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Import foods from CSV file

    CSV format: name,local_name,category,calories,protein,carbs,fats,fiber,vitamin_a,vitamin_c,calcium,iron,potassium,sodium,glycemic_index,is_diabetic_friendly,is_hypertension_friendly,description,preparation_tips,availability
    """
    try:
        content = await file.read()
        csv_data = io.StringIO(content.decode('utf-8'))
        reader = csv.DictReader(csv_data)

        created = 0
        skipped = 0
        errors = []

        for row in reader:
            try:
                # Check if exists
                existing = db.query(FoodDB).filter(FoodDB.name == row['name']).first()
                if existing:
                    skipped += 1
                    continue

                # Convert boolean strings
                is_diabetic = row.get('is_diabetic_friendly', 'false').lower() in ['true', '1', 'yes']
                is_hypertension = row.get('is_hypertension_friendly', 'false').lower() in ['true', '1', 'yes']

                # Create food entry
                db_food = FoodDB(
                    name=row['name'],
                    local_name=row.get('local_name') or None,
                    category=row['category'],
                    calories=float(row['calories']),
                    protein=float(row.get('protein', 0)),
                    carbs=float(row.get('carbs', 0)),
                    fats=float(row.get('fats', 0)),
                    fiber=float(row['fiber']) if row.get('fiber') else None,
                    vitamin_a=float(row['vitamin_a']) if row.get('vitamin_a') else None,
                    vitamin_c=float(row['vitamin_c']) if row.get('vitamin_c') else None,
                    calcium=float(row['calcium']) if row.get('calcium') else None,
                    iron=float(row['iron']) if row.get('iron') else None,
                    potassium=float(row['potassium']) if row.get('potassium') else None,
                    sodium=float(row['sodium']) if row.get('sodium') else None,
                    glycemic_index=int(row['glycemic_index']) if row.get('glycemic_index') else None,
                    is_diabetic_friendly=is_diabetic,
                    is_hypertension_friendly=is_hypertension,
                    description=row.get('description') or None,
                    preparation_tips=row.get('preparation_tips') or None,
                    availability=row.get('availability') or None,
                )
                db.add(db_food)
                created += 1

            except Exception as e:
                errors.append(f"Row error: {str(e)}")

        db.commit()

        return {
            "success": True,
            "created": created,
            "skipped": skipped,
            "total_rows": created + skipped,
            "errors": errors[:10]  # Limit error output
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"CSV import failed: {str(e)}")


@router.get("/search", response_model=List[Food])
async def search_foods(
    query: Optional[str] = None,
    category: Optional[str] = None,
    diabetic_friendly: Optional[bool] = None,
    hypertension_friendly: Optional[bool] = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Search foods in database"""
    query_obj = db.query(FoodDB)

    if query:
        query_obj = query_obj.filter(
            (FoodDB.name.ilike(f"%{query}%")) |
            (FoodDB.local_name.ilike(f"%{query}%"))
        )

    if category:
        query_obj = query_obj.filter(FoodDB.category == category)

    if diabetic_friendly is not None:
        query_obj = query_obj.filter(FoodDB.is_diabetic_friendly == diabetic_friendly)

    if hypertension_friendly is not None:
        query_obj = query_obj.filter(FoodDB.is_hypertension_friendly == hypertension_friendly)

    results = query_obj.limit(limit).all()
    return results


@router.get("/categories")
async def get_categories(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Get all food categories"""
    categories = db.query(FoodDB.category).distinct().all()
    return {"categories": [c[0] for c in categories]}


@router.get("/{food_id}", response_model=Food)
async def get_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Get food by ID"""
    food = db.query(FoodDB).filter(FoodDB.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@router.delete("/{food_id}")
async def delete_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Delete a food entry"""
    food = db.query(FoodDB).filter(FoodDB.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    db.delete(food)
    db.commit()
    return {"success": True, "message": "Food deleted"}


@router.get("/", response_model=List[Food])
async def list_foods(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """List all foods"""
    foods = db.query(FoodDB).offset(skip).limit(limit).all()
    return foods


@router.get("/recommend")
async def recommend_foods(
    food_id: Optional[str] = None,
    top_k: int = 10,
    model_name: Optional[str] = None,
    current_user: UserDB = Depends(get_current_user)
):
    """
    Get food recommendations using ensemble ML models
    
    Args:
        food_id: Optional food ID to get similar foods (if not provided, returns top recommendations)
        top_k: Number of recommendations to return (default: 10)
        model_name: Optional specific model to use (crgn_embeddings, gat_embeddings, hetgnn_embeddings)
    
    Returns:
        List of recommended foods with similarity scores and contributing models
    """
    from api.main import model_loader
    
    try:
        # Get recommendations from ensemble models
        if food_id:
            result = model_loader.recommend_foods(
                by_id=food_id,
                top_k=top_k,
                model_name=model_name
            )
        else:
            # Get top recommendations (you could use a default query vector here)
            result = model_loader.recommend_foods(
                top_k=top_k,
                model_name=model_name
            )
        
        if not result.get('success'):
            raise HTTPException(
                status_code=503,
                detail=result.get('error', 'Recommendation service unavailable')
            )
        
        return {
            "success": True,
            "recommendations": result.get('items', []),
            "models_used": result.get('models_used', []),
            "total": len(result.get('items', []))
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(e)}"
        )

