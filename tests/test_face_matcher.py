
import pytest
import cv2
import numpy as np
import os
from unittest.mock import patch, MagicMock
from face_recognition.face_matcher import face_matcher

@pytest.fixture
def create_dummy_images(tmpdir):
    """Create dummy images for testing."""
    source_image_path = os.path.join(tmpdir, "source.jpg")
    target_image_path = os.path.join(tmpdir, "target.jpg")

    # Create black images
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite(source_image_path, dummy_image)
    cv2.imwrite(target_image_path, dummy_image)

    return source_image_path, target_image_path

@patch('face_recognition.face_matcher.detect_faces')
@patch('face_recognition.face_matcher.identify_face')
def test_face_matcher_success(mock_identify_face, mock_detect_faces, create_dummy_images):
    """Test face_matcher successfully identifies faces."""
    source_image_path, target_image_path = create_dummy_images

    # Mock detect_faces to return two faces
    mock_detect_faces.return_value = {
        "success": True,
        
        "faces": [
            {"face_id": "face_1", "bbox": [10, 10, 50, 50]},
            {"face_id": "face_2", "bbox": [60, 60, 90, 90]}
        ]
    }

    # Mock identify_face to return a match for the first face and no match for the second
    mock_identify_face.side_effect = [
        {"success": True, "is_match": True},
        {"success": True, "is_match": False}
    ]

    result = face_matcher(source_image_path, target_image_path)

    assert result["success"] is True
    assert result["total_faces_detected"] == 2
    assert len(result["results"]) == 2
    assert result["results"][0]["identification_result"]["is_match"] is True
    assert result["results"][1]["identification_result"]["is_match"] is False

@patch('face_recognition.face_matcher.detect_faces')
def test_face_matcher_no_faces(mock_detect_faces, create_dummy_images):
    """Test face_matcher when no faces are detected."""
    source_image_path, target_image_path = create_dummy_images

    # Mock detect_faces to return no faces
    mock_detect_faces.return_value = {
        "success": True,
        "faces": []
    }

    result = face_matcher(source_image_path, target_image_path)

    assert result["success"] is True
    assert "No faces detected" in result["message"]
    assert len(result["results"]) == 0

def test_face_matcher_source_not_found():
    """Test face_matcher when the source image is not found."""
    result = face_matcher("non_existent_source.jpg", "non_existent_target.jpg")

    assert result["success"] is False
    assert "Face detection failed" in result["error"]
