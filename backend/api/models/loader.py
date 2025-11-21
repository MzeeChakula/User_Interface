import pickle
import logging
from pathlib import Path
from typing import Optional, Dict
import pandas as pd
import numpy as np

try:
    from huggingface_hub import hf_hub_download
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    logging.warning("huggingface_hub not installed. Online model features disabled.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Handles loading and management of different model types:
    1. Hugging Face model (XGBoost) - Best accuracy, requires internet
    2. Local XGBoost model - Good accuracy, offline
    3. HistGradient model - Lightweight, offline fallback
    """
    
    def __init__(self, local_model_dir: Optional[str] = None):
        # Use absolute path from project root
        if local_model_dir is None:
            project_root = Path(__file__).parent.parent.parent.parent
            local_model_dir = project_root / "src" / "results" / "models"
        self.local_model_dir = Path(local_model_dir)
        self.models = {}
        self.feature_names = None
        
        logger.info(f"Looking for models in: {self.local_model_dir}")
        
        # Load feature names (shared across models)
        self._load_feature_names()
        
        # Try to load all available models
        self._load_offline_model()
        self._load_local_xgboost()
        if HF_AVAILABLE:
            self._load_hf_model()
    
    def _load_feature_names(self):
        """Load feature names"""
        try:
            # Try v2 first
            feature_path = self.local_model_dir / 'feature_names_v2_20251103.pkl'
            if not feature_path.exists():
                feature_path = self.local_model_dir / 'xgboost_feature_names_20251103.pkl'

            with open(feature_path, 'rb') as f:
                self.feature_names = pickle.load(f)

            # Fix VitaminA field name (µ/μ -> ug for ASCII compatibility)
            self.feature_names = [
                'VitaminA_ug_per_serving' if 'VitaminA_' in name and 'g_per_serving' in name
                else name
                for name in self.feature_names
            ]

            logger.info(f"Loaded {len(self.feature_names)} feature names")
        except Exception as e:
            logger.error(f"Failed to load feature names: {e}")
            raise
    
    def _load_offline_model(self):
        """Load lightweight HistGradient model"""
        try:
            model_path = self.local_model_dir / 'baseline_nutrition_model_v2_20251103.pkl'
            if not model_path.exists():
                logger.warning("Offline model not found")
                return
            
            with open(model_path, 'rb') as f:
                import joblib
                try:
                    model = joblib.load(model_path)
                except:
                    model = pickle.load(f)
            
            self.models['offline'] = {
                'model': model,
                'type': 'HistGradientBoostingRegressor',
                'size': '75 KB',
                'accuracy': 'R² = 0.5116, MAE = 3.42 kcal/day',
                'test_r2': 0.5116,
                'test_mae': 3.42,
                'available': True
            }
            logger.info("Loaded offline model (HistGradient)")
        except Exception as e:
            logger.warning(f"Could not load offline model: {e}")
            self.models['offline'] = {'available': False}
    
    def _load_local_xgboost(self):
        """Load local XGBoost model"""
        try:
            model_path = self.local_model_dir / 'xgboost_nutrition_model_20251103.pkl'
            if not model_path.exists():
                logger.warning("Local XGBoost model not found")
                return
            
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            self.models['local_xgboost'] = {
                'model': model,
                'type': 'XGBoostRegressor',
                'size': '297 KB',
                'accuracy': 'R² = 0.6710, MAE = 2.84 kcal/day',
                'test_r2': 0.6710,
                'test_mae': 2.84,
                'available': True
            }
            logger.info("✅ Loaded local XGBoost model")
        except Exception as e:
            logger.warning(f"Could not load local XGBoost: {e}")
            self.models['local_xgboost'] = {'available': False}
    
    def _load_hf_model(self):
        """Load model from Hugging Face"""
        try:
            logger.info("Attempting to download from Hugging Face...")
            model_path = hf_hub_download(
                repo_id='Shakiran/MzeeChakula_Model',
                filename='xgboost_nutrition_model_20251103.pkl'
            )
            
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            self.models['huggingface'] = {
                'model': model,
                'type': 'XGBoostRegressor (HF)',
                'size': '297 KB',
                'accuracy': 'R² = 0.6710, MAE = 2.84 kcal/day',
                'test_r2': 0.6710,
                'test_mae': 2.84,
                'available': True,
                'repo_id': 'Shakiran/MzeeChakula_Model'
            }
            logger.info("Loaded Hugging Face model")
        except Exception as e:
            logger.warning(f"Could not load Hugging Face model: {e}")
            self.models['huggingface'] = {'available': False}
    
    def predict(
        self,
        input_data: Dict,
        model_preference: str = 'auto'
    ) -> Dict:
        """
        Make prediction with specified model preference.
        """
        # Determine which model to use
        if model_preference == 'auto':
            # Priority: HuggingFace > Local XGBoost > Offline
            if self.models.get('huggingface', {}).get('available'):
                model_key = 'huggingface'
            elif self.models.get('local_xgboost', {}).get('available'):
                model_key = 'local_xgboost'
            elif self.models.get('offline', {}).get('available'):
                model_key = 'offline'
            else:
                return {
                    'success': False,
                    'error': 'No models available',
                    'status': 'error'
                }
        else:
            model_key = model_preference
            if not self.models.get(model_key, {}).get('available'):
                return {
                    'success': False,
                    'error': f'Model {model_key} not available',
                    'status': 'error'
                }
        
        # Get model
        model_info = self.models[model_key]
        model = model_info['model']
        
        try:
            # Prepare input
            df = pd.DataFrame([input_data])
            df = df[self.feature_names]
            
            # Make prediction
            prediction = model.predict(df)[0]
            
            # Determine status
            if model_key == 'huggingface':
                status = 'online'
            elif model_key == 'local_xgboost':
                status = 'local'
            else:
                status = 'offline'
            
            return {
                'success': True,
                'prediction': {
                    'caloric_needs': float(prediction),
                    'unit': 'kcal/day',
                    'model': f"{model_info['type']} ({status.upper()})",
                    'accuracy': model_info['accuracy']
                },
                'model_info': {
                    'type': model_info['type'],
                    'size': model_info['size'],
                    'mode': status,
                    'test_r2': model_info['test_r2'],
                    'test_mae': model_info['test_mae']
                },
                'status': status
            }
            
        except Exception as e:
            logger.error(f"Prediction failed with {model_key}: {e}")
            return {
                'success': False,
                'error': str(e),
                'status': 'error'
            }
    
    def get_available_models(self) -> Dict:
        """Get status of all models"""
        return {
            key: {
                'available': info.get('available', False),
                'type': info.get('type'),
                'size': info.get('size'),
                'accuracy': info.get('accuracy')
            }
            for key, info in self.models.items()
        }
