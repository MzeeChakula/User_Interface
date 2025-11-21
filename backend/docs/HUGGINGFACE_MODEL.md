# HuggingFace Model Configuration

## Model Information

**Repository:** `Shakiran/MzeeChakulaNutritionEnsembleModel`  
**Type:** Nutrition Ensemble Model  
**Platform:** HuggingFace Hub

## Configuration

The backend is now configured to use the MzeeChakulaNutritionEnsembleModel from HuggingFace.

### Environment Variables

Set your HuggingFace token in `.env`:

```bash
HUGGINGFACE_TOKEN=your_huggingface_token_here
```

### Model Loading

The model is automatically downloaded from HuggingFace on first use:

```python
from api.models.loader import ModelLoader

loader = ModelLoader()
# Model will be downloaded from Shakiran/MzeeChakulaNutritionEnsembleModel
```

### API Usage

Make predictions using the `/predict` endpoint:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 70,
    "weight": 65,
    "height": 165,
    "gender": "male",
    "activity_level": "moderate",
    "model": "huggingface"
  }'
```

### Model Priority

When using `"model": "auto"`, the system prioritizes:
1. **HuggingFace Ensemble** - Best accuracy (requires internet)
2. **Local Fallback** - Works offline

## Files Updated

- ✅ `api/models/loader.py` - Model loading logic
- ✅ `api/core/config.py` - Configuration settings
- ✅ `api/main.py` - API metadata
- ✅ `api/routers/predict.py` - Prediction endpoint documentation

## Verification

Check model status:
```bash
curl http://localhost:8000/health
```

The response will show:
```json
{
  "huggingface_model": {
    "available": true,
    "type": "NutritionEnsembleModel (HF)",
    "repo_id": "Shakiran/MzeeChakulaNutritionEnsembleModel"
  }
}
```

## Notes

- The model file is cached locally after first download
- Requires `huggingface_hub` package (already in requirements.txt)
- Falls back to local model if HuggingFace is unavailable
