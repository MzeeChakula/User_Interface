"""
Tests for ML model loader
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.models.loader import ModelLoader


@pytest.mark.models
@pytest.mark.unit
def test_model_loader_initialization():
    """Test ModelLoader initializes without errors"""
    loader = ModelLoader()

    # Should initialize
    assert loader is not None
    assert hasattr(loader, 'models')
    assert hasattr(loader, 'feature_names')
    assert hasattr(loader, 'local_model_dir')


@pytest.mark.models
@pytest.mark.unit
def test_model_loader_path_resolution():
    """Test model directory path is resolved correctly"""
    loader = ModelLoader()

    # Path should exist or at least be defined
    assert loader.local_model_dir is not None
    assert isinstance(loader.local_model_dir, Path)


@pytest.mark.models
@pytest.mark.unit
def test_get_available_models():
    """Test getting available models"""
    loader = ModelLoader()
    available_models = loader.get_available_models()

    assert isinstance(available_models, dict)

    # Check expected model keys
    expected_keys = ['offline', 'local_xgboost', 'huggingface', 'ensemble']
    for key in expected_keys:
        if key in available_models:
            assert 'available' in available_models[key]


@pytest.mark.models
@pytest.mark.unit
def test_feature_names_loaded():
    """Test feature names are loaded if models exist"""
    loader = ModelLoader()

    # Feature names should be None or a list
    assert loader.feature_names is None or isinstance(loader.feature_names, list)

    if loader.feature_names:
        # Should have some features
        assert len(loader.feature_names) > 0


@pytest.mark.models
@pytest.mark.unit
def test_predict_without_models():
    """Test prediction fails gracefully when models not available"""
    loader = ModelLoader()

    # Try prediction
    result = loader.predict(
        input_data={},
        model_preference='auto'
    )

    assert isinstance(result, dict)
    assert 'success' in result or 'error' in result


@pytest.mark.models
@pytest.mark.slow
def test_predict_with_valid_input():
    """Test prediction with valid input if models are loaded"""
    loader = ModelLoader()

    # Check if any model is available
    available = loader.get_available_models()
    has_model = any(m.get('available', False) for m in available.values())

    if not has_model:
        pytest.skip("No models available for testing")

    # Sample valid input (this would need actual feature names)
    sample_input = {
        "age": 70,
        "weight": 65.5,
        "height": 165
    }

    result = loader.predict(sample_input)

    assert isinstance(result, dict)


@pytest.mark.models
@pytest.mark.unit
def test_recommend_foods_no_ensemble():
    """Test food recommendations fail gracefully without ensemble"""
    loader = ModelLoader()

    result = loader.recommend_foods(top_k=5)

    assert isinstance(result, dict)
    assert 'success' in result

    if not result['success']:
        assert 'error' in result


@pytest.mark.models
@pytest.mark.unit
def test_model_loader_handles_missing_directory():
    """Test ModelLoader handles missing model directory"""
    # Try to load from non-existent path
    loader = ModelLoader(local_model_dir="/nonexistent/path/to/models")

    # Should not crash
    assert loader is not None
    available = loader.get_available_models()
    assert isinstance(available, dict)
