"""
Meal Plan Generation Router
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from api.services.meal_plan_service import get_meal_plan_service
from api.services.pdf_service import get_pdf_service
from api.models.user import UserDB
from api.core.deps import get_current_user
from api.main import model_loader

router = APIRouter(
    prefix="/meal-plan",
    tags=["Meal Planning"],
)


class MealPlanRequest(BaseModel):
    """Request for meal plan generation"""
    name: str = Field(..., description="Patient name")
    age: int = Field(..., ge=0, le=120, description="Patient age")
    health_conditions: List[str] = Field(
        default=[],
        description="Health conditions (e.g., diabetes, hypertension)"
    )
    preferred_foods: List[str] = Field(
        default=[],
        description="Preferred local foods"
    )


class MealPlanResponse(BaseModel):
    """Meal plan response"""
    success: bool
    patient_name: str
    caloric_needs: int
    meal_plan: dict
    shopping_list: List[str]
    tips: List[str]
    generated_at: str
    model_used: Optional[str] = None


@router.post("/generate", response_model=MealPlanResponse)
async def generate_meal_plan(
    request: MealPlanRequest,
    current_user: UserDB = Depends(get_current_user)
):
    """
    Generate a personalized 7-day meal plan using ML models

    This endpoint:
    1. Uses HuggingFace ensemble model (when online) or XGBoost (offline)
    2. Calculates caloric needs based on age and health conditions
    3. Recommends culturally appropriate Ugandan foods
    4. Generates a structured 7-day meal plan
    """
    try:
        service = get_meal_plan_service(model_loader)

        result = service.generate_meal_plan(
            age=request.age,
            health_conditions=request.health_conditions,
            preferred_foods=request.preferred_foods,
            name=request.name
        )

        if not result['success']:
            raise HTTPException(status_code=500, detail=result.get('error', 'Generation failed'))

        # Add model info
        models = model_loader.get_available_models()
        if models.get('huggingface', {}).get('available'):
            result['model_used'] = 'HuggingFace Ensemble (Online)'
        elif models.get('local_xgboost', {}).get('available'):
            result['model_used'] = 'XGBoost (Local)'
        else:
            result['model_used'] = 'Fallback Model'

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate meal plan: {str(e)}")


@router.post("/generate/quick")
async def quick_meal_plan(
    age: int,
    conditions: str = "",  # Comma-separated
    foods: str = "",  # Comma-separated
    name: str = "Patient",
    current_user: UserDB = Depends(get_current_user)
):
    """
    Quick meal plan generation with simple parameters

    Example: POST /meal-plan/generate/quick?age=80&conditions=diabetes&foods=matooke,beans&name=Grandpa
    """
    # Parse comma-separated strings
    health_conditions = [c.strip() for c in conditions.split(',') if c.strip()]
    preferred_foods = [f.strip() for f in foods.split(',') if f.strip()]

    # Create request
    request = MealPlanRequest(
        name=name,
        age=age,
        health_conditions=health_conditions,
        preferred_foods=preferred_foods
    )

    return await generate_meal_plan(request, current_user)


@router.post("/generate/pdf")
async def generate_meal_plan_pdf(
    request: MealPlanRequest,
    current_user: UserDB = Depends(get_current_user)
):
    """
    Generate a meal plan and return as downloadable PDF

    This endpoint:
    1. Generates the meal plan using ML models
    2. Creates a professionally formatted PDF
    3. Returns the PDF for download
    """
    try:
        # Generate meal plan
        service = get_meal_plan_service(model_loader)
        result = service.generate_meal_plan(
            age=request.age,
            health_conditions=request.health_conditions,
            preferred_foods=request.preferred_foods,
            name=request.name
        )

        if not result['success']:
            raise HTTPException(status_code=500, detail=result.get('error', 'Generation failed'))

        # Add model info
        models = model_loader.get_available_models()
        if models.get('huggingface', {}).get('available'):
            result['model_used'] = 'HuggingFace Ensemble (Online)'
        elif models.get('local_xgboost', {}).get('available'):
            result['model_used'] = 'XGBoost (Local)'
        else:
            result['model_used'] = 'Fallback Model'

        # Generate PDF
        pdf_service = get_pdf_service()
        pdf_buffer = pdf_service.generate_meal_plan_pdf(result)

        # Create filename
        filename = f"meal_plan_{request.name.replace(' ', '_')}_{result['generated_at'][:10]}.pdf"

        # Return as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
