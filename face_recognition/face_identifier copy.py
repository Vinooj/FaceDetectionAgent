"""Face identification module using multimodal AI."""
print("Executing face_identifier.py")

import base64
from pathlib import Path
from typing import Any, Dict
import ollama
from fastmcp import FastMCP
from .camera import capture_image


def encode_image_to_base64(image_path: str) -> str:
    """Encode an image file to base64 string."""
    print(f"Encoding image to base64: {image_path}")
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

    
def identify_face(base_image_path: str, image_to_search_path: str) -> Dict[str, Any]:
    """
    Identify if the same person appears in two images using multimodal AI.
    
    Args:
        base_image_path: Path to the reference face image (cropped)
        image_to_search_path: Path to the image to search in (webcam capture)
        
    Returns:
        Dictionary with identification result (True if same person, False otherwise)
    """
    print(f"Attempting to identify face from {base_image_path} in {image_to_search_path}")
    try:
        # Verify both image files exist
        base_path = Path(base_image_path)
        search_path = Path(image_to_search_path)
        
        if not base_path.exists():
            print(f"Base image not found: {base_image_path}")
            return {
                "success": False,
                "error": f"Base image not found: {base_image_path}",
                "is_match": False
            }
        
        if not search_path.exists():
            # If we don't find the search image path, the use the came ra tool to capture the second image
            # capture_image(image_to_search_path, 0)
            print(f"Search image not found: {image_to_search_path}")
            return {
                "success": False,
                "error": f"Search image not found: {image_to_search_path}",
                "is_match": False
            }
        
        # Create prompt for multimodal model
        prompt = (
            "You are a face recognition expert. Compare the person in the first image "
            "with the person in the second image. Determine if they are the same person. "
            "Answer with ONLY 'yes' or 'no', nothing else."
        )
        
        # Call Ollama with multimodal model
        print("Calling Ollama for face identification")
        response = ollama.generate(
            model="qwen3-vl:235b-cloud",
            prompt=prompt,
            images=[base_image_path, image_to_search_path],
            stream=False
        )
        
        print("Returned from Ollama call for face identification")
        
        # Parse the response
        answer = response.get("response", "").strip().lower()
        is_match = answer == "yes"
        print(f"Ollama response: {answer}, Match: {is_match}")
        
        return {
            "success": True,
            "error": None,
            "is_match": is_match,
            "response": answer
        }
    
    except Exception as e:
        print(f"An error occurred during face identification: {e}")
        return {
            "success": False,
            "error": str(e),
            "is_match": False
        }
