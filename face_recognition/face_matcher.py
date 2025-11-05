
"""Face matching module."""
import cv2
import os
from typing import Any, Dict, List
from .face_detector import detect_faces
from .face_identifier import identify_face

def face_matcher(source_image_path: str, target_image_path: str) -> Dict[str, Any]:
    """
    Detect all faces in the source image and match them against the target image.

    Args:
        source_image_path: Path to the source image with faces to be detected.
        target_image_path: Path to the target image to match against.

    Returns:
        A dictionary containing the matching results for each detected face.
    """
    print(f"Starting face matching process for {source_image_path} and {target_image_path}")

    # Detect faces in the source image
    detection_result = detect_faces(source_image_path)
    if not detection_result.get("success"):
        return {
            "success": False,
            "error": "Face detection failed.",
            "details": detection_result.get("error"),
            "results": []
        }

    faces = detection_result.get("faces", [])
    if not faces:
        return {
            "success": True,
            "error": None,
            "message": "No faces detected in the source image.",
            "results": []
        }

    # Create a directory for temporary cropped face images
    temp_dir = "temp_cropped_faces"
    os.makedirs(temp_dir, exist_ok=True)

    # Read the source image
    source_image = cv2.imread(source_image_path)
    if source_image is None:
        return {
            "success": False,
            "error": f"Failed to read source image: {source_image_path}",
            "results": []
        }

    match_results = []
    for i, face in enumerate(faces):
        print((f"Inside the face detection loop - {i}"))
        bbox = face.get("bbox")
        if not bbox or len(bbox) != 4:
            print(f"Skipping face {i} due to invalid bounding box.")
            continue

        # Crop the face from the source image
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        cropped_face = source_image[y1:y2, x1:x2]

        # Save the cropped face to a temporary file
        cropped_face_path = os.path.join(temp_dir, f"face_{i}.jpg")
        cv2.imwrite(cropped_face_path, cropped_face)

        # Identify the cropped face against the target image
        identification_result = identify_face(cropped_face_path, target_image_path)
        match_results.append({
            "face_id": face.get("face_id"),
            "bbox": bbox,
            "identification_result": identification_result
        })

    # Clean up temporary files
    # for i in range(len(faces)):
    #     cropped_face_path = os.path.join(temp_dir, f"face_{i}.jpg")
    #     if os.path.exists(cropped_face_path):
    #         os.remove(cropped_face_path)
    # os.rmdir(temp_dir)

    return {
        "success": True,
        "error": None,
        "total_faces_detected": len(faces),
        "results": match_results
    }
