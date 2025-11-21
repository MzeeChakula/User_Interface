from fastapi import APIRouter
from datetime import datetime
from ..models import HealthStatus, ModelStatus, EncodingReference

router = APIRouter(
    prefix="/health",
    tags=["Health & Status"],
    responses={404: {"description": "Not found"}}
)

# Model loader will be injected by main app
model_loader = None


def set_model_loader(loader):
    """Set the model loader instance"""
    global model_loader
    model_loader = loader


@router.get(
    "/",
    response_model=HealthStatus,
    summary="Health Check",
    description="Check API health and availability"
)
async def health_check():
    """
    Check if API is running and which models are available.
    """
    models_status = {}
    
    if model_loader:
        available = model_loader.get_available_models()
        models_status = {
            key: info['available']
            for key, info in available.items()
        }
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "models": models_status,
        "timestamp": datetime.now().isoformat()
    }


@router.get(
    "/models",
    response_model=ModelStatus,
    summary="Model Status",
    description="Get detailed status of all available models"
)
async def get_model_status():
    """
    Get detailed information about all available models.
    
    **Returns:**
    - Offline model: HistGradient Boosting (75 KB, always available)
    - Local XGBoost: Better accuracy (297 KB, offline)
    - Hugging Face: Best accuracy (requires internet)
    """
    if not model_loader:
        return {
            "offline_model": {"available": False},
            "online_model": {"available": False}
        }
    
    available = model_loader.get_available_models()
    
    return {
        "offline_model": available.get('offline', {"available": False}),
        "online_model": available.get('local_xgboost', {"available": False}),
        "huggingface_model": available.get('huggingface', {"available": False})
    }


@router.get(
    "/encoding",
    response_model=EncodingReference,
    summary="Encoding Reference",
    description="Get encoding mappings for categorical features"
)
async def get_encoding_reference():
    """
    Get the encoding mappings for categorical features.
    
    Use these mappings to convert categorical values to encoded integers.
    """
    return {
        "regions": {
            0: "Central Uganda (Buganda)",
            1: "Western Uganda (Ankole, Tooro, Kigezi, Bunyoro)",
            2: "Eastern Uganda (Busoga, Bugisu, Teso)",
            3: "Northern Uganda (Acholi, Lango, Karamoja, West Nile)"
        },
        "conditions": {
            0: "Hypertension",
            1: "Undernutrition",
            2: "Anemia",
            3: "Frailty",
            4: "Digestive issues",
            5: "Arthritis",
            6: "Osteoporosis",
            7: "Diabetes"
        },
        "age_groups": {
            0: "80+",
            1: "60-70",
            2: "70-80"
        },
        "seasons": {
            0: "Dry",
            1: "Wet"
        }
    }


@router.get(
    "/metrics",
    summary="Model Metrics",
    description="Get performance metrics for all models"
)
async def get_model_metrics():
    """
    Get performance metrics for all available models.
    
    **Metrics:**
    - R² Score: Coefficient of determination (higher is better)
    - MAE: Mean Absolute Error in kcal/day (lower is better)
    - Size: Model file size
    """
    if not model_loader:
        return {"error": "Model loader not initialized"}
    
    available = model_loader.get_available_models()
    
    metrics = {}
    for key, info in available.items():
        if info['available']:
            metrics[key] = {
                "type": info['type'],
                "accuracy": info['accuracy'],
                "size": info['size'],
                "available": True
            }
        else:
            metrics[key] = {"available": False}
    
    return {
        "models": metrics,
        "recommendation": "Use 'huggingface' for best accuracy (online), 'local_xgboost' for offline best, or 'offline' for smallest size"
    }
