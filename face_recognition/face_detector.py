"""Face detection module using RetinaFace."""
from typing import Any, Dict
from pathlib import Path
import numpy as np
from retinaface import RetinaFace

def convert_to_native_types(obj: Any) -> Any:
    """Convert numpy types to native Python types for JSON serialization."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_to_native_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_native_types(item) for item in obj]
    return obj


def detect_faces(image_path: str) -> Dict[str, Any]:
    """
    Detect faces in an image using RetinaFace.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary containing detected faces with bounding boxes and landmarks
    """
    print(f"Attempting to detect faces in image: {image_path}")
    try:
        # Verify the image file exists
        path = Path(image_path)
        if not path.exists():
            print(f"Image file not found: {image_path}")
            return {
                "success": False,
                "error": f"Image file not found: {image_path}",
                "faces": []
            }
        
        # Detect faces using RetinaFace
        print("Calling RetinaFace.detect_faces")
        faces = RetinaFace.detect_faces(image_path)
        
        if not faces or isinstance(faces, dict) and "error" in faces:
            print("No faces detected or an error occurred")
            return {
                "success": True,
                "error": None,
                "faces": [],
                "total_faces": 0
            }
        
        # Process detected faces
        print(f"Detected {len(faces)} faces")
        processed_faces = []
        for face_id, face_data in faces.items():
            if isinstance(face_data, dict):
                # Extract facial area (bounding box)
                facial_area = face_data.get("facial_area", [])
                
                face_info = {
                    "face_id": face_id,
                    "bbox": convert_to_native_types(facial_area),
                    "landmarks": convert_to_native_types(face_data.get("landmarks", {})),
                    "confidence": float(face_data.get("score", 0))
                }
                processed_faces.append(face_info)
        
        print("Face detection successful")
        return {
            "success": True,
            "error": None,
            "faces": processed_faces,
            "total_faces": len(processed_faces)
        }
    
    except Exception as e:
        print(f"An error occurred during face detection: {e}")
        return {
            "success": False,
            "error": str(e),
            "faces": [],
            "total_faces": 0
        }
