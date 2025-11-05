"""FastMCP server for face detection and identification tools."""
print("Executing mcp_server.py")
import json
from fastmcp import FastMCP
from typing import Any, Dict, List
from google.adk.tools import ToolContext
from face_recognition.face_identifier import identify_face
from face_recognition.face_detector import detect_faces
from face_recognition.face_matcher import face_matcher
from face_recognition.camera import capture_image
from face_recognition.draw_bounding_box_on_image import draw_object_rectangle

mcp = FastMCP("Face Identification Tools")

def serializeDict(response: Dict[str, Any]) -> str:
    try:
        # Standard JSON serialization
        return json.dumps(response, ensure_ascii=False)
    except TypeError:
        print("Inside serializeDict Exception")
        # Fallback for non-serializable objects (e.g., custom classes, numpy arrays)
        return json.dumps(response, default=lambda o: getattr(o, "__dict__", str(o)), ensure_ascii=False)

@mcp.tool()
def call_capture_image(output_path: str) -> str:
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
             }
    """
    print(f"Inside MCP Server the capture_image tool - {output_path}")

    response = capture_image(file_path=output_path)
    print(f"Inside MCP Server After image capture - response: {response} json: {serializeDict(response)}")
    return serializeDict(response)


@mcp.tool()
def call_detect_faces(image_path: str) -> str:
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
    print(f"Inside MCP Server the detect_faces tool - {image_path}")
    response = detect_faces(image_path=image_path)
    return serializeDict(response)


@mcp.tool()
def call_identify_face(base_image_path: str, image_to_search_path: str) -> str:
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
    print(f"Inside the MCP Server identify_face tool - {base_image_path} {image_to_search_path}")
    response = identify_face(base_image_path, image_to_search_path)
    return serializeDict(response)


@mcp.tool()
def call_face_matcher(source_image_path: str, target_image_path: str) -> str:
    """
    Compares two images to determine if they contain the same person.

    Args:
        source_image_path (str): The file path to the reference (base) image.
        target_image_path (str): The file path to the image to search within.

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
    print(f"Inside the MCP Server face_matcher tool - {source_image_path} {target_image_path}")
    response = face_matcher(source_image_path, target_image_path)
    return serializeDict(response)


@mcp.tool()
def call_draw_object_rectangle(
    image_path: str, bounding_box: List[int], color: tuple, thickness: int, tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Draws a bounding box on an image and saves it to a new file.

    Args:
        image_path (str): The path to the input image file.
        bounding_box (List[int]): A list of 4 integers representing the bounding box
                                  in [x1, y1, x2, y2] format.
        output_path (str): The path to save the output image with the bounding box.
        color (tuple): The color of the bounding box in BGR format (default is green).
        thickness (int): The thickness of the bounding box lines.

    Returns:
        A dictionary with the result of the operation.
        {
            "success": bool,
            "output_path": str | None,
            "error": str | None
        }
    """
    print(f"Inside the MCP Server draw_object_rectangle tool - {image_path} {bounding_box}")

    response = draw_object_rectangle(image_path, bounding_box)
    return serializeDict(response)

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)