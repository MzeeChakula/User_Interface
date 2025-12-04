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
        # Use absolute path - models are in backend/models/
        if local_model_dir is None:
            # From api/models/loader.py -> go up to backend/ then into models/
            backend_root = Path(__file__).parent.parent.parent
            local_model_dir = backend_root / "models"
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
            # Try newest date first (20251120), then older versions
            feature_path = self.local_model_dir / 'xgboost_feature_names_20251120.pkl'
            if not feature_path.exists():
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
            # Try newest date first
            model_path = self.local_model_dir / 'xgboost_nutrition_model_20251120.pkl'
            if not model_path.exists():
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
            embedding_candidates = []
            metadata_path = None
            
            # Find all potential embedding files
            # Prioritize JSON files as they often contain ID mappings
            embedding_candidates.extend(sorted(list(repo_path.rglob('*embedd*.json'))))
            embedding_candidates.extend(sorted(list(repo_path.rglob('*embedd*.npy'))))
            
            # Find metadata file
            for p in repo_path.rglob('*.json'):
                name = p.name.lower()
                if 'meta' in name or 'items' in name or 'foods' in name:
                    metadata_path = p
                    break

            if not embedding_candidates:
                logger.warning("No embeddings file found in HF repo snapshot")
            
            # Load ALL embedding files and combine them
            all_embeddings = []
            all_ids = []
            loaded_files = []
            
            # Try loading from ALL candidates
            for embeddings_path in embedding_candidates:
                try:
                    logger.info(f"Attempting to load embeddings from: {embeddings_path.name}")
                    
                    if embeddings_path.suffix == '.npy':
                        # NPY loading
                        data = np.load(embeddings_path, allow_pickle=True)
                        raw_embeddings = data
                        # For NPY, we might not have IDs unless they are in a separate file or part of the array
                        # If data is object array, it might contain IDs? Assuming simple array for now
                        raw_ids = [f"{embeddings_path.stem}_{i}" for i in range(len(data))]
                    else:
                        # JSON loading
                        import json
                        with open(embeddings_path, 'r', encoding='utf-8') as ef:
                            data = json.load(ef)
                        
                        raw_embeddings = []
                        raw_ids = []
                        
                        # Normalize data structure
                        if isinstance(data, dict):
                            raw_ids = list(data.keys())
                            raw_embeddings = list(data.values())
                        elif isinstance(data, list):
                            if len(data) > 0 and isinstance(data[0], dict):
                                # List of dicts
                                for idx, item in enumerate(data):
                                    raw_ids.append(str(item.get('id') or item.get('food_id') or f"{embeddings_path.stem}_{idx}"))
                                    raw_embeddings.append(item.get('vector') or item.get('embedding'))
                            else:
                                # List of lists/arrays
                                raw_embeddings = data
                                raw_ids = [f"{embeddings_path.stem}_{i}" for i in range(len(data))]
                    
                    # Validate and filter embeddings
                    valid_embeddings = []
                    valid_ids = []
                    
                    if len(raw_embeddings) > 0:
                        # Determine expected dimension from the first valid non-empty vector
                        expected_dim = 0
                        for vec in raw_embeddings:
                            if hasattr(vec, '__len__') and len(vec) > 0:
                                expected_dim = len(vec)
                                break
                        
                        if expected_dim > 0:
                            for i, vec in enumerate(raw_embeddings):
                                if hasattr(vec, '__len__') and len(vec) == expected_dim:
                                    valid_embeddings.append(vec)
                                    valid_ids.append(raw_ids[i])
                        
                        if valid_embeddings:
                            # Add to combined list
                            all_embeddings.extend(valid_embeddings)
                            all_ids.extend(valid_ids)
                            loaded_files.append(embeddings_path.name)
                            logger.info(f"Successfully loaded {len(valid_embeddings)} valid embeddings from {embeddings_path.name}")
                        else:
                            logger.warning(f"No valid embeddings found in {embeddings_path.name}")
                    else:
                        logger.warning(f"Empty embeddings data in {embeddings_path.name}")
                        
                except Exception as e:
                    logger.warning(f"Failed to load embeddings from {embeddings_path.name}: {e}")
                    continue
            
            # Convert combined embeddings to numpy array
            # Handle different embedding dimensions by storing them as separate models
            emb = None
            ids = None
            if all_embeddings:
                # Group embeddings by dimension
                dim_groups = {}
                for i, embedding in enumerate(all_embeddings):
                    dim = len(embedding)
                    if dim not in dim_groups:
                        dim_groups[dim] = {'embeddings': [], 'ids': [], 'files': set()}
                    dim_groups[dim]['embeddings'].append(embedding)
                    dim_groups[dim]['ids'].append(all_ids[i])
                    # Extract filename from ID (format: filename_index)
                    file_prefix = all_ids[i].rsplit('_', 1)[0] if '_' in all_ids[i] else 'unknown'
                    dim_groups[dim]['files'].add(file_prefix)
                
                # Log dimension groups
                for dim, group in dim_groups.items():
                    files_str = ', '.join(sorted(group['files']))
                    logger.info(f"Found {len(group['embeddings'])} embeddings with dimension {dim} from: {files_str}")
                
                # Store ALL dimension groups as separate sub-models
                if dim_groups:
                    # Create a multi-model ensemble structure
                    ensemble_models = {}
                    total_embeddings = 0
                    
                    for dim, group in dim_groups.items():
                        emb_array = np.array(group['embeddings'], dtype=float)
                        # Normalize embeddings for cosine similarity
                        norms = np.linalg.norm(emb_array, axis=1, keepdims=True)
                        norms[norms == 0] = 1.0
                        emb_norm = emb_array / norms
                        
                        # Determine model name from files
                        files = sorted(group['files'])
                        model_name = files[0] if len(files) == 1 else f"{dim}D_combined"
                        
                        ensemble_models[model_name] = {
                            'embeddings': emb_norm,
                            'ids': group['ids'],
                            'dimension': dim,
                            'count': len(emb_norm)
                        }
                        total_embeddings += len(emb_norm)
                        
                        files_str = ', '.join(files)
                        logger.info(f"Created sub-ensemble '{model_name}': {len(emb_norm)} items × {dim}D from {files_str}")
                    
                    # Store the multi-model ensemble
                    self.models['ensemble'] = {
                        'models': ensemble_models,
                        'available': True,
                        'repo_id': repo_id,
                        'type': 'MultiModelEnsemble',
                        'size': f'{total_embeddings} items across {len(ensemble_models)} models',
                        'accuracy': f'Food recommendation via {len(ensemble_models)} embedding models'
                    }
                    logger.info(f"Finalized multi-model ensemble with {total_embeddings} total embeddings across {len(ensemble_models)} models")
                    
                    # For backward compatibility, also set emb to the largest group
                    best_dim = max(dim_groups.keys(), key=lambda d: len(dim_groups[d]['embeddings']))
                    best_group = dim_groups[best_dim]
                    emb = np.array(best_group['embeddings'], dtype=float)
                    ids = best_group['ids']

            # Load metadata if present (shared across attempts)
            metadata = {}
            try:
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
                logger.warning(f"Failed to load metadata: {e}")

            # Ensemble model already created above with multi-model structure
            # Only set to unavailable if no embeddings were loaded at all
            if 'ensemble' not in self.models:
                self.models['ensemble'] = {'available': False}
                logger.warning("Ensemble embeddings not available after trying all candidates")

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
            # If we didn't load a huggingface model file but have embeddings, mark as available
            if 'huggingface' not in self.models:
                if emb is not None:
                    # Embeddings loaded successfully, mark HF as available
                    self.models['huggingface'] = {
                        'available': True,
                        'type': 'HuggingFace Embeddings',
                        'size': f'{emb_norm.shape[0]} embeddings',
                        'accuracy': 'Food recommendation model',
                        'repo_id': repo_id
                    }
                else:
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
    
    def recommend_foods(self, query_vector=None, top_k: int = 5, by_id: str = None, model_name: str = None):
        """Return top-k similar food items from the ensemble embeddings.

        Provide either `query_vector` (iterable) or `by_id` to look up an item in the loaded ids.
        If model_name is specified, use only that model; otherwise combine results from all models.
        """
        ensemble = self.models.get('ensemble', {})
        if not ensemble.get('available'):
            return {'success': False, 'error': 'Ensemble embeddings not available', 'items': []}

        # Check if this is a multi-model ensemble
        if 'models' in ensemble:
            # Multi-model ensemble - combine results from all models
            ensemble_models = ensemble['models']
            
            if model_name and model_name in ensemble_models:
                # Use specific model only
                models_to_use = {model_name: ensemble_models[model_name]}
            else:
                # Use all models
                models_to_use = ensemble_models
            
            try:
                all_results = {}  # {item_id: {'score': max_score, 'meta': meta, 'models': [model_names]}}
                
                for m_name, m_data in models_to_use.items():
                    emb = m_data['embeddings']
                    ids = m_data['ids']
                    
                    # Prepare query vector
                    if by_id is not None:
                        if ids is None:
                            continue
                        try:
                            idx = ids.index(str(by_id))
                        except ValueError:
                            continue
                        q = emb[idx]
                    else:
                        if query_vector is None:
                            continue
                        q = np.array(query_vector, dtype=float)
                        # Pad or truncate query vector to match embedding dimension
                        if len(q) != m_data['dimension']:
                            if len(q) < m_data['dimension']:
                                q = np.pad(q, (0, m_data['dimension'] - len(q)))
                            else:
                                q = q[:m_data['dimension']]
                        q = q / (np.linalg.norm(q) or 1.0)
                    
                    # Cosine similarity with normalized embeddings -> dot product
                    sims = emb.dot(q)
                    top_idx = np.argsort(-sims)[:top_k * 2]  # Get more candidates for merging
                    
                    for i in top_idx:
                        item_id = ids[i] if ids is not None else str(i)
                        score = float(sims[i])
                        
                        if item_id in all_results:
                            # Combine scores (take maximum or average)
                            all_results[item_id]['score'] = max(all_results[item_id]['score'], score)
                            all_results[item_id]['models'].append(m_name)
                        else:
                            all_results[item_id] = {
                                'score': score,
                                'meta': {},
                                'models': [m_name]
                            }
                
                # Sort by score and take top_k
                sorted_items = sorted(all_results.items(), key=lambda x: x[1]['score'], reverse=True)[:top_k]
                
                items = []
                for item_id, data in sorted_items:
                    items.append({
                        'id': item_id,
                        'score': data['score'],
                        'meta': data['meta'],
                        'models': data['models']  # Which models contributed to this recommendation
                    })
                
                return {
                    'success': True,
                    'items': items,
                    'models_used': list(models_to_use.keys())
                }
                
            except Exception as e:
                logger.error(f"Multi-model recommendation failed: {e}")
                return {'success': False, 'error': str(e), 'items': []}
        
        else:
            # Legacy single-model ensemble
            emb = ensemble.get('embeddings')
            ids = ensemble.get('ids')
            metadata = ensemble.get('metadata', {})
            
            if emb is None:
                return {'success': False, 'error': 'No embeddings in ensemble', 'items': []}

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
