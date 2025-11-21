"""Init file for models package"""
# Note: schemas.py doesn't exist, models are in separate files
# from .schemas import (
#     NutritionInput,
#     PredictionResponse,
#     PredictionOutput,
#     ModelInfo,
#     HealthStatus,
#     EncodingReference,
#     ModelStatus,
#     BatchPredictionInput,
#     BatchPredictionResponse
# )
from .loader import ModelLoader

__all__ = [
    'ModelLoader'
]
