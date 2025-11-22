from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .models.loader import ModelLoader
from .routers import predict_router, health_router
from .routers import predict, health
from .routers.metrics import router as metrics_router
from .models import database, user, chat, food

# Create database tables
# Order matters for foreign keys: User -> Conversation -> Message, Food (independent)
try:
    user.Base.metadata.create_all(bind=database.engine)
    chat.Base.metadata.create_all(bind=database.engine)
    food.Base.metadata.create_all(bind=database.engine)
    logger = logging.getLogger(__name__)
    logger.info("Database tables created successfully")
except Exception as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"Could not create database tables: {e}")
    logger.warning("App will continue without database. Auth endpoints may not work.")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("MzeeChakula Nutrition API Started")
    logger.info("Documentation: http://localhost:8000/docs")
    logger.info("Health Check: http://localhost:8000/health")
    logger.info("Prediction: http://localhost:8000/predict")
    yield
    # Shutdown
    logger.info("MzeeChakula API shutting down...")

# Creating FastAPI app
app = FastAPI(
    lifespan=lifespan,
    title="MzeeChakula Nutrition API",
    description="",
    version="1.0.0",
    contact={
        "name": "MzeeChakula Team",
        "url": "https://huggingface.co/Shakiran/MzeeChakulaNutritionEnsembleModel",
        "backend": "https://mzeechakula-backend.onrender.com",
        "email": "support@mzeechakula.com"
    },
    license_info={
        "name": "MIT",
    }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mzeechakula.vercel.app",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model loader
logger.info("Initializing MzeeChakula API...")
try:
    model_loader = ModelLoader()
    
    # Inject model loader into routers
    predict.set_model_loader(model_loader)
    health.set_model_loader(model_loader)
    
    available_models = model_loader.get_available_models()
    logger.info("Available models:")
    for name, info in available_models.items():
        if info['available']:
            logger.info(f"{name}: {info['type']} ({info['size']})")
        else:
            logger.info(f"{name}: Not available")

except Exception as e:
    logger.error(f"Failed to initialize models: {e}")
    raise

from .routers.auth import router as auth_router
from .routers.chat import router as chat_router
from .routers.ai import router as ai_router
from .routers.meal_plan import router as meal_plan_router
from .routers.food import router as food_router
from .routers.voice import router as voice_router

# Include routers
app.include_router(health_router)
app.include_router(predict_router)
app.include_router(metrics_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(ai_router)
app.include_router(meal_plan_router)
app.include_router(food_router)
app.include_router(voice_router)


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API docs"""
    return RedirectResponse(url="/docs")


@app.get("/api/info", tags=["Info"])
async def api_info():
    """
    Get API information and available endpoints.
    """
    return {
        "name": "MzeeChakula Nutrition API",
        "version": "1.0.0",
        "description": "Predict daily caloric needs for elderly individuals in Uganda",
        "models": model_loader.get_available_models() if model_loader else {},
        "endpoints": {
            "health": "/health - Check API health",
            "models": "/health/models - Get model status",
            "encoding": "/health/encoding - Get encoding reference",
            "metrics": "/health/metrics - Get model metrics",
            "predict": "/predict - Make single prediction",
            "batch": "/predict/batch - Make batch predictions",
            "example": "/predict/example - Get example input",
            "docs": "/docs - Interactive API documentation",
            "redoc": "/redoc - Alternative API documentation"
        },
        "repository": "https://huggingface.co/Shakiran/MzeeChakulaNutritionEnsembleModel"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
