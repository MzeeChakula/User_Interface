from fastapi import APIRouter, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from api.models.prediction import ModelInfo
from api.models.loader import ModelLoader
import time

router = APIRouter(tags=["Metrics"])

# Metrics
prediction_counter = Counter('predictions_total', 'Total number of predictions', ['model', 'status'])
prediction_duration = Histogram('prediction_duration_seconds', 'Time spent processing prediction')
model_accuracy = Gauge('model_accuracy', 'Model accuracy', ['model'])

@router.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
