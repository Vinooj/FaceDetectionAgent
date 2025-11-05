import google.generativeai as genai
from pathlib import Path
from typing import Dict, Any
import json
from PIL import Image

def identify_face(base_image_path: str, image_to_search_path: str) -> Dict[str, Any]:
    """
    Identify if the same person appears in two images using Gemini 2.5 Flash.
    
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
            print(f"Search image not found: {image_to_search_path}")
            return {
                "success": False,
                "error": f"Search image not found: {image_to_search_path}",
                "is_match": False
            }
        
        # Load images using PIL
        image1 = Image.open(base_image_path)
        image2 = Image.open(image_to_search_path)
        
        prompt = """
            You are a highly specialized face recognition and image analysis expert. Your task is to perform an accurate face comparison and location detection.

            **Input:**
            1.  **Source Image:** Contains the target face for identification.
            2.  **Target Image:** A video conference screenshot containing multiple faces.

            **Target Image Resolution Constraint:**
            All coordinates and dimensions for the bounding box **MUST** be scaled to a fixed resolution of **1920 pixels wide by 1080 pixels tall** (1920x1080).

            **Task:**
            1.  **High-Precision Comparison:** Compare the face in the Source Image against **every** face visible in the Target Image. The comparison must be based on fine-grained facial features, including but not limited to:
                * Mustache shape, density, and trim.
                * Eyeglasses style, frame shape, and color.
                * Overall facial structure, skin texture, and hair pattern/color.
                * *Specifically, note that two different individuals may appear superficially similar (e.g., both wearing glasses and a mustache), requiring a judgment based on subtle, distinct facial markers.*
            2.  **Determine Match:** State `'yes'` if the person is confirmed to be present, or `'no'` otherwise.
            3.  **Generate Output:** Return **ONLY** a single, valid JSON object and nothing else.
            4.  **Bounding Box:** If a match is found (`'yes'`), provide the single, tightest **bounding box** for the matched face. The coordinates **MUST** be scaled to the 1920x1080 resolution. If no match is found (`'no'`), the value for the `bounding_box` field **MUST** be the JSON keyword `null`.
            5.  **Data Type:** All coordinates within the `bounding_box` array **MUST** be integers.

            **Mandatory Output Schema:**
            A single JSON object with the following two fields:
            * `"match"`: A string, either `"yes"` or `"no"`.
            * `"bounding_box"`: An array of four integers `[x, y, width, height]` or the JSON keyword `null`.

            **Example Output (Match Found, coordinates scaled to 1920x1080):**
            ```json
            {
            "match": "yes",
            "bounding_box": [120, 345, 200, 400]
            }
        """
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Generate response with both images
        response = model.generate_content([
            prompt,
            image1,
            image2
        ])
        
        raw = response.text.strip()
        print(f"Gemini raw response: {raw}")
        
        # Try to parse JSON response from the model
        try:
            # Clean up markdown code blocks if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()
            
            parsed = json.loads(raw)
            match_str = parsed.get("match", "").strip().lower()
            is_match = match_str == "yes"
            bounding_box = parsed.get("bounding_box")
        except Exception as parse_err:
            print(f"Failed to parse JSON from model response: {parse_err}")
            # Fallback: try simple yes/no
            is_match = raw.lower().startswith("yes")
            bounding_box = None
        
        return {
            "success": True,
            "error": None,
            "is_match": is_match,
            "response": raw,
            "bounding_box": bounding_box
        }
        
    except Exception as e:
        print(f"An error occurred during face identification: {e}")
        return {
            "success": False,
            "error": str(e),
            "is_match": False
        }