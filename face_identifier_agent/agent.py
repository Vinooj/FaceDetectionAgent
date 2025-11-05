import json
from fastmcp import Client
from typing import Any, Dict
from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool, ToolContext
from pathlib import Path
from .prompt import FACE_MATCHER_PROMPT
from face_recognition.fetch_image import fetch_image
from face_recognition.draw_bounding_box_on_image import draw_object_rectangle

client = Client("http://localhost:8000/mcp")

# Define a custom tool for drawing bounding rectangle over the target image
# Use FunctionTool() to create the tool
# The imagePath is the target image and bounding_box is returned by the face_matcher.
draw_object_rectangle_tool = FunctionTool(func=draw_object_rectangle)

# Define a custom tool for image generation
# Use FunctionTool() to create the tool
# The name and description are automatically inferred from the function's definition and docstring.
fetch_image_tool = FunctionTool(func=fetch_image)
    
async def capture_image(output_path: str) -> str:
    """
    Captures an image from the primary camera and saves it to the specified path.

    Args:
        output_path (str): The file path where the captured image should be saved.

    Returns:
        str: A JSON-encoded string representing a dictionary with the capture result,
             for example:
             {
               "success": true,             # bool indicating whether capture succeeded
               "file_path": "/path/to.jpg", # path to the saved image (if successful)
               "error": null                # error message (if any)
             }.
    """
    try:
        async with client:
            print(f"Inside the capture_image tool - {output_path}")
            result = await client.call_tool("call_capture_image", {"output_path": output_path})
            return str(result)
    except Exception as e:
        return json.dumps({"success": False, "file_path": None, "error": str(e)})
    

async def detect_faces(image_path: str) -> str:
    """
    Detect faces in an image using RetinaFace.
    
    Args:
        image_path: Path to the image file

    Returns:
        str: A JSON-encoded string representing a dictionary with the capture result,
             for example:
             {
                "success": True,
                "error": None,
                "faces": processed_faces,
                "total_faces": len(processed_faces)
            }
    """
    try:
        async with client:
            print(f"Inside the detect_faces tool - {image_path}")
            result = await client.call_tool("call_detect_faces", {"image_path": image_path})
            return str(result)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

async def identify_face(base_image_path: str, image_to_search_path: str) -> str:
    """
    Compares two images to determine if they contain the same person.

    Args:
        base_image_path (str): The file path to the reference (base) image.
        image_to_search_path (str): The file path to the image to search within.

    Returns:
        str: A JSON-encoded string representing a dictionary with the identification result,
             for example:
             {
               "is_match": true,              # bool indicating whether the faces match
               "confidence": 0.95,            # optional float confidence score
               "base_image": "/path/to.jpg",  # original base image path
               "query_image": "/path/to2.jpg",# image searched against
               "error": null                  # error message (if any)
             }
    """
    try:
        async with client:
            print(f"Inside the identify_face tool - {base_image_path} {image_to_search_path}")
            result = await client.call_tool(
                "call_identify_face",
                {
                    "base_image_path": base_image_path,
                    "image_to_search_path": image_to_search_path,
                },
            )
            return str(result)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    
async def face_matcher(source_image_path: str, target_image_path: str) -> Dict[str, Any]:
    """
    Detect all faces in the source image and match them against the target image.

    Args:
        source_image_path: Path to the source image with faces to be detected.
        target_image_path: Path to the target image to match against.

    Returns:
        A dictionary containing the matching results for each detected face.
    """
    try:
        async with client:
            print(f"Inside the identify_face tool - {source_image_path} {target_image_path}")
            result = await client.call_tool(
                "call_face_matcher",
                {
                    "source_image_path": source_image_path,
                    "target_image_path": target_image_path,
                },
            )
            
            print(f"Face matcher returend {str(result)}")
            return str(result)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="An agent that helps identify faces.",
    instruction=FACE_MATCHER_PROMPT,
    tools=[fetch_image_tool, capture_image, face_matcher, draw_object_rectangle_tool],
)
