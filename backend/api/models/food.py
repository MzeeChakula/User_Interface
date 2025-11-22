"""
Food Database Models
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from .database import Base


# --- Pydantic Schemas ---

class FoodBase(BaseModel):
    """Base food schema"""
    name: str = Field(..., description="Food name")
    local_name: Optional[str] = Field(None, description="Local/Ugandan name")
    category: str = Field(..., description="Food category (staple, protein, vegetable, fruit, etc.)")

    # Nutritional information per 100g
    calories: float = Field(..., ge=0, description="Calories per 100g")
    protein: float = Field(default=0, ge=0, description="Protein (g) per 100g")
    carbs: float = Field(default=0, ge=0, description="Carbohydrates (g) per 100g")
    fats: float = Field(default=0, ge=0, description="Fats (g) per 100g")
    fiber: Optional[float] = Field(None, ge=0, description="Fiber (g) per 100g")

    # Micronutrients
    vitamin_a: Optional[float] = Field(None, ge=0, description="Vitamin A (μg) per 100g")
    vitamin_c: Optional[float] = Field(None, ge=0, description="Vitamin C (mg) per 100g")
    calcium: Optional[float] = Field(None, ge=0, description="Calcium (mg) per 100g")
    iron: Optional[float] = Field(None, ge=0, description="Iron (mg) per 100g")
    potassium: Optional[float] = Field(None, ge=0, description="Potassium (mg) per 100g")
    sodium: Optional[float] = Field(None, ge=0, description="Sodium (mg) per 100g")

    # Health information
    glycemic_index: Optional[int] = Field(None, ge=0, le=100, description="Glycemic index")
    is_diabetic_friendly: bool = Field(default=False, description="Suitable for diabetics")
    is_hypertension_friendly: bool = Field(default=False, description="Suitable for hypertension")

    # Additional info
    description: Optional[str] = Field(None, description="Food description")
    preparation_tips: Optional[str] = Field(None, description="How to prepare")
    availability: Optional[str] = Field(None, description="Seasonal availability")


class FoodCreate(FoodBase):
    """Food creation schema"""
    pass


class Food(FoodBase):
    """Food response schema"""
    id: int = Field(..., description="Food ID")
    model_config = ConfigDict(from_attributes=True)


class FoodSearch(BaseModel):
    """Food search parameters"""
    query: Optional[str] = Field(None, description="Search query")
    category: Optional[str] = Field(None, description="Filter by category")
    diabetic_friendly: Optional[bool] = Field(None, description="Filter diabetic-friendly foods")
    hypertension_friendly: Optional[bool] = Field(None, description="Filter hypertension-friendly foods")
    limit: int = Field(default=20, ge=1, le=100, description="Number of results")


class BulkFoodImport(BaseModel):
    """Bulk food import schema"""
    foods: list[FoodCreate] = Field(..., description="List of foods to import")


# --- SQLAlchemy Models ---

class FoodDB(Base):
    """Food database model"""
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    local_name = Column(String, nullable=True)
    category = Column(String, index=True, nullable=False)

    # Nutritional information
    calories = Column(Float, nullable=False)
    protein = Column(Float, default=0)
    carbs = Column(Float, default=0)
    fats = Column(Float, default=0)
    fiber = Column(Float, nullable=True)

    # Micronutrients
    vitamin_a = Column(Float, nullable=True)
    vitamin_c = Column(Float, nullable=True)
    calcium = Column(Float, nullable=True)
    iron = Column(Float, nullable=True)
    potassium = Column(Float, nullable=True)
    sodium = Column(Float, nullable=True)

    # Health information
    glycemic_index = Column(Integer, nullable=True)
    is_diabetic_friendly = Column(Boolean, default=False)
    is_hypertension_friendly = Column(Boolean, default=False)

    # Additional info
    description = Column(Text, nullable=True)
    preparation_tips = Column(Text, nullable=True)
    availability = Column(String, nullable=True)
