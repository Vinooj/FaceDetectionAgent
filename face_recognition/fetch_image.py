from typing import Any, Dict
from google.adk.tools import ToolContext
from google.genai import types
from fastmcp.utilities.types import Image
from mcp.types import ImageContent
from .utils import load_image_bytes, get_filename

async def fetch_image(imagePath: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Generates an image from a text description and returns an artifact.
    """
    print(f"Tool called to fetch image with prompt: '{imagePath}'")

    # load bytes from the desired path
    image_bytes = load_image_bytes(imagePath)
    
    file_name = get_filename(imagePath)
    
    await tool_context.save_artifact(
      file_name,
      types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
    )
    return {
        'status': 'success',
        'detail': 'Image generated successfully and stored in artifacts.',
        'filename': imagePath,
    }
    
def show_image(image_path) -> ImageContent:
    """
    Generates an image.
    """
    image = Image.open(image_path)
    return _encode_image(image)

def _encode_image(image) -> ImageContent:
    """
    Encodes a PIL Image to a format compatible with ImageContent.
    """
    import io
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    img_obj = Image(data=img_bytes, format="png")
    return img_obj.to_image_content()