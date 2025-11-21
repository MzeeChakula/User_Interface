from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import List, Optional
import logging
from api.models.prediction import (
    NutritionInput,
    PredictionResponse,
    BatchPredictionInput,
    BatchPredictionResponse
)
from api.models.loader import ModelLoader

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/predict",
    tags=["Predictions"],
    responses={404: {"description": "Not found"}}
)

# Model loader will be injected by main app
model_loader = None


def set_model_loader(loader):
    """Set the model loader instance"""
    global model_loader
    model_loader = loader


@router.post(
    "/",
    response_model=PredictionResponse,
    summary="Predict Daily Caloric Needs",
    description="Predict daily caloric needs based on nutritional and demographic features"
)
async def predict_caloric_needs(
    input_data: NutritionInput,
    model: Optional[str] = Query(
        'auto',
        description="Model to use: 'auto', 'huggingface', 'local_xgboost', or 'offline'"
    )
):

    if model_loader is None:
        raise HTTPException(status_code=500, detail="Model loader not initialized")
    
    try:
        # Convert Pydantic model to dict
        input_dict = input_data.dict()
        
        # Make prediction
        result = model_loader.predict(input_dict, model_preference=model)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result.get('error', 'Prediction failed'))
        
        return result
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/batch",
    response_model=BatchPredictionResponse,
    summary="Batch Predictions",
    description="Make predictions for multiple inputs at once"
)
async def batch_predict(
    batch_input: BatchPredictionInput
):
    """
    Make predictions for multiple inputs.
    
    **Benefits:**
    - More efficient for multiple predictions
    - Returns summary statistics
    - Continues on individual errors
    """
    if model_loader is None:
        raise HTTPException(status_code=500, detail="Model loader not initialized")
    
    results = []
    successful = 0
    failed = 0
    
    model_pref = 'auto' if batch_input.prefer_online else 'offline'
    
    for input_data in batch_input.inputs:
        try:
            input_dict = input_data.dict()
            result = model_loader.predict(input_dict, model_preference=model_pref)
            results.append(result)
            
            if result['success']:
                successful += 1
            else:
                failed += 1
        except Exception as e:
            results.append({
                'success': False,
                'error': str(e),
                'status': 'error'
            })
            failed += 1
    
    return {
        'success': True,
        'predictions': results,
        'total': len(batch_input.inputs),
        'successful': successful,
        'failed': failed
    }


@router.get(
    "/example",
    summary="Get Example Input",
    description="Get an example input format for testing"
)
async def get_example_input():
    """
    Returns an example input that can be used for testing the prediction endpoint.
    """
    return {
        "example": {
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
        },
        "description": {
            "region": "0 = Central Uganda",
            "condition": "0 = Hypertension",
            "age_group": "1 = 70-80 years",
            "season": "0 = Dry"
        }
    }


@router.get(
    "/recommend",
    summary="Recommend similar foods",
    description="Return top-k similar foods from HF ensemble embeddings. Provide `by_id` or `vector` (comma-separated) and optional `top_k`."
)
async def recommend(
    by_id: Optional[str] = Query(None, description="Lookup recommendations by item id from ensemble"),
    vector: Optional[str] = Query(None, description="Comma-separated vector to query embeddings"),
    top_k: Optional[int] = Query(5, description="Number of top similar items to return")
):
    """
    Get food recommendations based on similarity search using HuggingFace embeddings.
    
    **Usage:**
    - Provide `by_id` to find similar foods to a specific food item
    - Provide `vector` as comma-separated numbers to search by custom embedding
    - Adjust `top_k` to control number of results (default: 5)
    
    **Example:**
    ```
    GET /predict/recommend?by_id=12345&top_k=10
    GET /predict/recommend?vector=0.1,0.2,0.3,...&top_k=5
    ```
    """
    if model_loader is None:
        raise HTTPException(status_code=500, detail="Model loader not initialized")

    if by_id is None and vector is None:
        raise HTTPException(status_code=400, detail="Provide either by_id or vector")

    qvec = None
    if vector is not None:
        try:
            qvec = [float(x) for x in vector.split(',') if x.strip()]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid vector: {e}")

    try:
        result = model_loader.recommend_foods(query_vector=qvec, top_k=top_k, by_id=by_id)
        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error', 'Recommendation failed'))
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
