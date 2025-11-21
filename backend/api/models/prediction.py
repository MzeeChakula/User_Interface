from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field, ConfigDict
from .common import Region, Condition, AgeGroup, Season

class NutritionInput(BaseModel):
    """Input data for nutrition prediction"""
    
    # Nutritional content (per serving)
    Energy_kcal_per_serving: float = Field(..., ge=0, le=3000, description="Energy in kcal")
    Protein_g_per_serving: float = Field(..., ge=0, le=200, description="Protein in grams")
    Fat_g_per_serving: float = Field(..., ge=0, le=200, description="Fat in grams")
    Carbohydrates_g_per_serving: float = Field(..., ge=0, le=500, description="Carbohydrates in grams")
    Fiber_g_per_serving: float = Field(..., ge=0, le=100, description="Fiber in grams")
    
    # Micronutrients (per serving)
    Calcium_mg_per_serving: float = Field(..., ge=0, le=3000, description="Calcium in mg")
    Iron_mg_per_serving: float = Field(..., ge=0, le=100, description="Iron in mg")
    Zinc_mg_per_serving: float = Field(..., ge=0, le=50, description="Zinc in mg")
    VitaminA_ug_per_serving: float = Field(..., ge=0, le=5000, description="Vitamin A in µg")
    VitaminC_mg_per_serving: float = Field(..., ge=0, le=500, description="Vitamin C in mg")
    Potassium_mg_per_serving: float = Field(..., ge=0, le=10000, description="Potassium in mg")
    Magnesium_mg_per_serving: float = Field(..., ge=0, le=1000, description="Magnesium in mg")
    
    # Demographic/contextual (encoded values)
    region_encoded: int = Field(..., ge=0, le=3, description="Region code (0-3)")
    condition_encoded: int = Field(..., ge=0, le=7, description="Health condition code (0-7)")
    age_group_encoded: int = Field(..., ge=0, le=2, description="Age group code (0-2)")
    season_encoded: int = Field(..., ge=0, le=1, description="Season code (0-1)")
    
    # Additional context
    portion_size_g: float = Field(..., ge=0, le=5000, description="Portion size in grams")
    estimated_cost_ugx: float = Field(..., ge=0, le=100000, description="Estimated cost in UGX")

    model_config = ConfigDict(
        json_schema_extra={
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
            }
        }
    )

class PredictionOutput(BaseModel):
    """Prediction response"""
    caloric_needs: float = Field(..., description="Predicted daily caloric needs in kcal/day")
    unit: str = Field(default="kcal/day", description="Unit of measurement")
    model: str = Field(..., description="Model used for prediction")
    accuracy: str = Field(..., description="Model accuracy metrics")

class ModelInfo(BaseModel):
    """Model information"""
    type: str = Field(..., description="Model type")
    size: str = Field(..., description="Model size")
    mode: str = Field(..., description="Deployment mode (online/offline)")
    test_r2: float = Field(..., description="Test R² score")
    test_mae: float = Field(..., description="Test MAE")

class PredictionResponse(BaseModel):
    """Complete prediction response"""
    success: bool = Field(..., description="Whether prediction was successful")
    prediction: Optional[PredictionOutput] = Field(None, description="Prediction results")
    model_info: Optional[ModelInfo] = Field(None, description="Model information")
    status: str = Field(..., description="Status (online/offline)")
    error: Optional[str] = Field(None, description="Error message if failed")

class HealthStatus(BaseModel):
    """Health check response"""
    status: str = Field(..., description="API status")
    version: str = Field(..., description="API version")
    models: Dict[str, bool] = Field(..., description="Available models")
    timestamp: str = Field(..., description="Current timestamp")

class EncodingReference(BaseModel):
    """Reference for feature encoding"""
    regions: Dict[int, str]
    conditions: Dict[int, str]
    age_groups: Dict[int, str]
    seasons: Dict[int, str]

class ModelStatus(BaseModel):
    """Status of available models"""
    offline_model: Dict[str, Any]
    online_model: Dict[str, Any]
    huggingface_model: Optional[Dict[str, Any]] = None

class BatchPredictionInput(BaseModel):
    """Batch prediction input"""
    inputs: List[NutritionInput] = Field(..., description="List of nutrition inputs")
    prefer_online: bool = Field(default=True, description="Prefer online model")

class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    success: bool
    predictions: List[PredictionResponse]
    total: int
    successful: int
    failed: int
