Uploading local model files

Drop any local model artifacts here if you want the backend to load them.

Recommended filenames (used by `ModelLoader` if present):

- `xgboost_feature_names_20251103.pkl`  -- pickle containing ordered feature names list
- `xgboost_nutrition_model_20251103.pkl` -- pickled XGBoost model
- `baseline_nutrition_model_v2_20251103.pkl` -- optional fallback model

If you have precomputed embeddings for the ensemble, place them here as well with names like:

- `embeddings.json` (dict id -> vector, or list of {"id":..., "vector":[...]})
- `embeddings.npy` (numpy 2D array)
- `metadata.json` (optional, mapping id -> metadata for recommended items)

Notes:
- The loader now prefers Hugging Face snapshot embeddings, but will fall back to any local files 
placed here.
- If you plan to build Docker images that include local models, update the Docker build step to COPY this directory.
