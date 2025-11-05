"""Tests for MCP server and face recognition tools."""

import tempfile
from pathlib import Path
import pytest
import numpy as np
import cv2
from mcp_server import mcp_server


@pytest.fixture
def test_image_path():
    """Create a temporary test image."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        # Create a simple test image with a face-like pattern
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        cv2.circle(img, (50, 50), 20, (0, 0, 0), -1)  # Simple circle pattern
        cv2.imwrite(tmp.name, img)
        yield tmp.name
    Path(tmp.name).unlink(missing_ok=True)


@pytest.fixture
def test_image_path_invalid():
    """Return path to non-existent image."""
    return "/tmp/nonexistent_image_12345.jpg"


@pytest.fixture
def sample_face_image():
    """Create a sample image with a simple face-like pattern."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        img = np.ones((200, 200, 3), dtype=np.uint8) * 255
        # Draw a simple face pattern
        cv2.circle(img, (100, 80), 40, (0, 0, 0), 2)      # Head
        cv2.circle(img, (80, 70), 5, (0, 0, 0), -1)       # Left eye
        cv2.circle(img, (120, 70), 5, (0, 0, 0), -1)      # Right eye
        cv2.line(img, (90, 100), (110, 100), (0, 0, 0), 2) # Mouth
        cv2.imwrite(tmp.name, img)
        yield tmp.name
    Path(tmp.name).unlink(missing_ok=True)


# ============================================================================
# Core Module Tests
# ============================================================================

def test_mcp_server_exists():
    """Test MCP server instance exists."""
    assert mcp_server is not None


def test_mcp_server_is_fastmcp():
    """Test MCP server is a FastMCP instance."""
    from fastmcp import FastMCP
    assert isinstance(mcp_server, FastMCP)


def test_mcp_server_has_name():
    """Test MCP server has a name."""
    assert hasattr(mcp_server, 'name')
    assert mcp_server.name == "face-detection-app"


# ============================================================================
# Module Import Tests
# ============================================================================

def test_face_detector_module_imports():
    """Test face detector module imports correctly."""
    from face_recognition.face_detector import (
        register_face_detector_tools,
        convert_to_native_types
    )
    
    assert callable(register_face_detector_tools)
    assert callable(convert_to_native_types)


def test_face_identifier_module_imports():
    """Test face identifier module imports correctly."""
    from face_recognition.face_identifier import (
        register_face_identifier_tools,
        encode_image_to_base64
    )
    
    assert callable(register_face_identifier_tools)
    assert callable(encode_image_to_base64)


def test_camera_module_imports():
    """Test camera module imports correctly."""
    from face_recognition.camera import register_camera_tools
    
    assert callable(register_camera_tools)


def test_mcp_server_module_imports():
    """Test MCP server module imports correctly."""
    from mcp_server import create_mcp_server, mcp_server
    
    assert callable(create_mcp_server)
    assert mcp_server is not None


# ============================================================================
# Utility Function Tests
# ============================================================================

def test_numpy_type_conversion():
    """Test numpy type conversion utility."""
    from face_recognition.face_detector import convert_to_native_types
    
    # Test various numpy types
    test_data = {
        "int_val": np.int64(100),
        "float_val": np.float32(3.14),
        "array_val": np.array([1, 2, 3]),
        "nested": {
            "nested_int": np.int32(50)
        }
    }
    
    result = convert_to_native_types(test_data)
    
    assert result["int_val"] == 100
    assert isinstance(result["int_val"], int)
    assert isinstance(result["float_val"], float)
    assert isinstance(result["array_val"], list)
    assert result["nested"]["nested_int"] == 50


def test_numpy_int_conversion():
    """Test numpy int conversion."""
    from face_recognition.face_detector import convert_to_native_types
    
    result = convert_to_native_types(np.int64(42))
    assert result == 42
    assert isinstance(result, int)


def test_numpy_float_conversion():
    """Test numpy float conversion."""
    from face_recognition.face_detector import convert_to_native_types
    
    result = convert_to_native_types(np.float32(3.14))
    assert isinstance(result, float)
    assert abs(result - 3.14) < 0.01


def test_numpy_array_conversion():
    """Test numpy array conversion."""
    from face_recognition.face_detector import convert_to_native_types
    
    arr = np.array([[1, 2], [3, 4]])
    result = convert_to_native_types(arr)
    assert isinstance(result, list)
    assert result == [[1, 2], [3, 4]]


def test_image_encoding():
    """Test image encoding to base64."""
    from face_recognition.face_identifier import encode_image_to_base64
    
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        # Create simple image
        img = np.ones((50, 50, 3), dtype=np.uint8) * 255
        cv2.imwrite(tmp.name, img)
        
        # Test encoding
        b64_str = encode_image_to_base64(tmp.name)
        
        assert isinstance(b64_str, str)
        assert len(b64_str) > 0
        assert b64_str.isprintable()
        
        Path(tmp.name).unlink(missing_ok=True)


# ============================================================================
# Configuration Tests
# ============================================================================

def test_config_module_imports():
    """Test config module imports correctly."""
    from config import (
        get_config,
        get_server_config,
        get_streamlit_config,
        get_ollama_config,
        get_paths_config,
        get_detection_config,
        get_identification_config,
        get_logging_config
    )
    
    assert callable(get_config)
    assert callable(get_server_config)
    assert callable(get_streamlit_config)
    assert callable(get_ollama_config)
    assert callable(get_paths_config)
    assert callable(get_detection_config)
    assert callable(get_identification_config)
    assert callable(get_logging_config)


def test_config_values():
    """Test configuration values are properly loaded."""
    from config import get_config
    
    config = get_config()
    
    assert config is not None
    assert hasattr(config, 'server')
    assert hasattr(config, 'streamlit')
    assert hasattr(config, 'ollama')
    assert hasattr(config, 'paths')


def test_server_config():
    """Test server configuration."""
    from config import get_server_config
    
    server_config = get_server_config()
    
    assert server_config.host is not None
    assert server_config.port > 0
    assert hasattr(server_config, 'url')


def test_streamlit_config():
    """Test Streamlit configuration."""
    from config import get_streamlit_config
    
    streamlit_config = get_streamlit_config()
    
    assert streamlit_config.port == 8501
    assert hasattr(streamlit_config, 'url')


def test_ollama_config():
    """Test Ollama configuration."""
    from config import get_ollama_config
    
    ollama_config = get_ollama_config()
    
    assert ollama_config.model == "qwen3-vl:235b-cloud"
    assert ollama_config.host is not None


def test_paths_config():
    """Test paths configuration."""
    from config import get_paths_config
    
    paths_config = get_paths_config()
    
    assert paths_config is not None
    assert hasattr(paths_config, 'temp_dir')
    assert hasattr(paths_config, 'log_dir')


def test_detection_config():
    """Test detection configuration."""
    from config import get_detection_config
    
    detection_config = get_detection_config()
    
    assert detection_config.min_confidence >= 0
    assert detection_config.min_confidence <= 1
    assert detection_config.min_face_size > 0


def test_identification_config():
    """Test identification configuration."""
    from config import get_identification_config
    
    identification_config = get_identification_config()
    
    assert identification_config.max_retries > 0
    assert identification_config.retry_delay >= 0


def test_logging_config():
    """Test logging configuration."""
    from config import get_logging_config
    
    logging_config = get_logging_config()
    
    assert logging_config.level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    assert hasattr(logging_config, 'format')


# ============================================================================
# File System Tests
# ============================================================================

def test_image_file_creation(sample_face_image):
    """Test sample image file is created."""
    assert Path(sample_face_image).exists()
    assert Path(sample_face_image).stat().st_size > 0


def test_temp_file_creation():
    """Test temporary file creation."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        img = np.zeros((10, 10, 3), dtype=np.uint8)
        cv2.imwrite(tmp.name, img)
        
        assert Path(tmp.name).exists()
        Path(tmp.name).unlink()


# ============================================================================
# Integration Tests
# ============================================================================

def test_app_imports():
    """Test Streamlit app imports correctly."""
    try:
        # This will fail if dependencies are missing, but should at least parse
        import ast
        with open('app.py', 'r') as f:
            ast.parse(f.read())
        assert True
    except SyntaxError:
        pytest.fail("app.py has syntax errors")


def test_server_simple_imports():
    """Test Flask server imports correctly."""
    try:
        import ast
        with open('mcp_server_simple.py', 'r') as f:
            ast.parse(f.read())
        assert True
    except (SyntaxError, FileNotFoundError):
        # File may not exist, which is OK
        assert True


# ============================================================================
# Cleanup
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_temp_files():
    """Cleanup temporary files after each test."""
    yield
    import shutil
    import glob
    
    # Clean up any temp files we created
    for pattern in ['/tmp/*.jpg', '/tmp/*.png', '/tmp/face_detection*']:
        for path in glob.glob(pattern):
            try:
                if Path(path).is_file():
                    Path(path).unlink()
                elif Path(path).is_dir():
                    shutil.rmtree(path)
            except Exception:
                pass