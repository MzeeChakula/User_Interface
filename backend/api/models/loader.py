import pickle
import logging
from pathlib import Path
from typing import Optional, Dict
import pandas as pd
import numpy as np

try:
    # prefer snapshot_download (downloads full repo snapshot)
    from huggingface_hub import snapshot_download, hf_hub_download
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    logging.warning("huggingface_hub not installed. Online model features disabled.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Handles loading and management of different model types:
    1. Hugging Face Ensemble Model - Best accuracy, requires internet
    2. Local fallback model - Lightweight, offline
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
            logger.info("Loaded local XGBoost model")
        except Exception as e:
            logger.warning(f"Could not load local XGBoost: {e}")
            self.models['local_xgboost'] = {'available': False}
    
    def _load_hf_model(self):
        """Load Nutrition Ensemble Model from Hugging Face with embeddings"""
        try:
            logger.info("Attempting to download ensemble from Hugging Face (snapshot)...")

            # Prefer the ensemble repo which contains precomputed JSON embeddings
            repo_id = 'Shakiran/MzeeChakulaNutritionEnsembleModel'
            try:
                repo_dir = snapshot_download(repo_id)
            except Exception as e:
                logger.warning(f"snapshot_download failed: {e}, falling back to single file download")
                # fallback to single file download if snapshot unavailable
                model_path = hf_hub_download(
                    repo_id=repo_id,
                    filename='model.pkl'
                )
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)

                self.models['huggingface'] = {
                    'model': model,
                    'type': 'NutritionEnsembleModel (HF)',
                    'size': 'Ensemble Model',
                    'accuracy': 'Ensemble of multiple models',
                    'available': True,
                    'repo_id': repo_id
                }
                self.models['ensemble'] = {'available': False}
                logger.info("Loaded Hugging Face model (fallback)")
                return

            # If snapshot_download succeeded, look for embeddings and metadata
            from pathlib import Path as _P
            repo_path = _P(repo_dir)

            # Search for JSON embeddings or numpy arrays
            embeddings_path = None
            metadata_path = None
            for p in repo_path.rglob('*.json'):
                name = p.name.lower()
                if 'embedd' in name:
                    embeddings_path = p
                if 'meta' in name or 'items' in name or 'foods' in name:
                    metadata_path = p

            # Also accept .npy files
            if embeddings_path is None:
                for p in repo_path.rglob('*.npy'):
                    if 'embedd' in p.name.lower():
                        embeddings_path = p
                        break

            if embeddings_path is None:
                logger.warning("No embeddings file found in HF repo snapshot")
            else:
                # Load embeddings
                try:
                    if embeddings_path.suffix == '.npy':
                        emb = np.load(embeddings_path)
                        ids = None
                    else:
                        import json
                        with open(embeddings_path, 'r', encoding='utf-8') as ef:
                            data = json.load(ef)
                        # data could be dict id->vector or list of {id:..., vector:...}
                        if isinstance(data, dict):
                            ids = list(data.keys())
                            emb = np.array(list(data.values()), dtype=float)
                        elif isinstance(data, list) and len(data) and isinstance(data[0], dict):
                            ids = [str(item.get('id') or item.get('food_id') or idx) for idx, item in enumerate(data)]
                            emb = np.array([item.get('vector') or item.get('embedding') for item in data], dtype=float)
                        else:
                            emb = np.array(data, dtype=float)
                            ids = None

                    # Load metadata if present
                    metadata = {}
                    if metadata_path and metadata_path.exists():
                        import json
                        with open(metadata_path, 'r', encoding='utf-8') as mf:
                            md = json.load(mf)
                        # Expect dict id->info or list
                        if isinstance(md, dict):
                            metadata = md
                        elif isinstance(md, list):
                            # try to create mapping using id key
                            for item in md:
                                key = item.get('id') or item.get('food_id')
                                if key is not None:
                                    metadata[str(key)] = item
                except Exception as e:
                    logger.warning(f"Failed to load embeddings/metadata: {e}")
                    emb = None
                    ids = None
                    metadata = {}

                if emb is not None:
                    # normalize embeddings for cosine similarity
                    norms = np.linalg.norm(emb, axis=1, keepdims=True)
                    norms[norms == 0] = 1.0
                    emb_norm = emb / norms

                    self.models['ensemble'] = {
                        'embeddings': emb_norm,
                        'ids': ids,
                        'metadata': metadata,
                        'available': True,
                        'repo_id': repo_id
                    }
                    logger.info(f"Loaded ensemble embeddings ({emb_norm.shape[0]} items)")
                else:
                    self.models['ensemble'] = {'available': False}
                    logger.warning("Ensemble embeddings not available after download")

            # Also try to load a model file inside the snapshot if present (xgboost pickle)
            try:
                for p in repo_path.rglob('*.pkl'):
                    if 'xgboost' in p.name.lower() or 'nutrition_model' in p.name.lower() or 'model' in p.name.lower():
                        with open(p, 'rb') as f:
                            model = pickle.load(f)
                        self.models['huggingface'] = {
                            'model': model,
                            'type': 'NutritionEnsembleModel (HF-snapshot)',
                            'size': f"{p.stat().st_size//1024} KB",
                            'accuracy': 'Ensemble model',
                            'available': True,
                            'repo_id': repo_id
                        }
                        logger.info("Loaded model from HF snapshot")
                        break
            except Exception:
                pass
            # If we didn't load a huggingface model file, ensure a key exists
            if 'huggingface' not in self.models:
                self.models['huggingface'] = {'available': False}
        except Exception as e:
            logger.warning(f"Could not load Hugging Face model: {e}")
            self.models['huggingface'] = {'available': False}
            self.models['ensemble'] = {'available': False}
    
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
    
    def recommend_foods(self, query_vector=None, top_k: int = 5, by_id: str = None):
        """Return top-k similar food items from the ensemble embeddings.

        Provide either `query_vector` (iterable) or `by_id` to look up an item in the loaded ids.
        """
        ensemble = self.models.get('ensemble', {})
        if not ensemble.get('available'):
            return {'success': False, 'error': 'Ensemble embeddings not available', 'items': []}

        emb = ensemble['embeddings']
        ids = ensemble.get('ids')
        metadata = ensemble.get('metadata', {})

        try:
            if by_id is not None:
                if ids is None:
                    return {'success': False, 'error': 'No ids available to look up by_id', 'items': []}
                try:
                    idx = ids.index(str(by_id))
                except ValueError:
                    return {'success': False, 'error': 'by_id not found', 'items': []}
                q = emb[idx]
            else:
                q = np.array(query_vector, dtype=float)
                q = q / (np.linalg.norm(q) or 1.0)

            # cosine similarity with normalized embeddings -> dot product
            sims = emb.dot(q)
            top_idx = np.argsort(-sims)[:top_k]

            items = []
            for i in top_idx:
                item_id = ids[i] if ids is not None else i
                info = metadata.get(str(item_id), {})
                items.append({'id': item_id, 'score': float(sims[i]), 'meta': info})

            return {'success': True, 'items': items}
        except Exception as e:
            logger.error(f"Recommendation failed: {e}")
            return {'success': False, 'error': str(e), 'items': []}
    
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
