import cv2
from typing import Any, Dict, List
from google.genai import types
from google.adk.tools import ToolContext
from pathlib import Path
from .utils import load_image_bytes, get_filename


async  def draw_object_rectangle(
    image_path: str, bounding_box: List[int], tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Draws a bounding box on an image and saves it to a new file.

    Args:
        image_path (str): The path to the input image file.
        bounding_box (List[int]): A list of 4 integers representing the bounding box
                                  in [x1, y1, x2, y2] format.
        output_path (str): The path to save the output image with the bounding box.
        tool_context(ToolContext): 

    Returns:
        A dictionary with the result of the operation.
        {
            'status': 'success',
            'detail': 'Image generated successfully and stored in artifacts.',
            'filename': file_name,
        }
    """
    print(f"Tool called to draw object rectangle: '{image_path}'")
    try:
        color = (255, 0, 0)
        thickness = 2
         
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            return {"success": False, "output_path": None, "error": f"Could not read image from {image_path}"}
        
        # Draw the bounding box
        x, y, w, h = [int(c) for c in bounding_box]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)

        output_path = "./result_with_bbox.jpg"
        # Save rewriet the image 
        cv2.imwrite(output_path, image)
        
        # load bytes from the desired path
        image_bytes = load_image_bytes(output_path)
    
        file_name = get_filename(output_path)
        await tool_context.save_artifact(
            file_name,
            types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
        )
        
        return {
            'status': 'success',
            'detail': 'Image showing detected face is generated successfully and stored in artifacts.',
            'filename': file_name,
        }

    except Exception as e:
        return {'status': 'failed', 'detail': 'Was not able to create the image with bounded rect', "error": str(e)}
