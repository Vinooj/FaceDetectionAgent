import asyncio
from fastmcp import Client
from typing import Any, Dict

client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)
        
        
async def call_capture_image(file_path: str, camera_index: int = 0) -> Dict[str, Any]:
    async with client:
        result = await client.call_tool("call_capture_image", {"file_path": file_path, "camera_index":camera_index})
        print(result)

async def call_detect_faces(image_path: str) -> Dict[str, Any]:
    async with client:
        result = await client.call_tool("call_detect_faces", {"image_path": image_path})
        print(result)
        
async def call_identify_face(base_image_path: str, image_to_search_path: str) -> str:
    async with client:
        result = await client.call_tool("call_identify_face", {"base_image_path": base_image_path, "image_to_search_path": image_to_search_path })
        print(result)      
        
async def call_face_matcher(source_image_path: str, target_image_path: str) -> Dict[str, Any]:
    async with client:
        result = await client.call_tool("call_face_matcher",{"source_image_path": source_image_path, "target_image_path": target_image_path})
        print(result)  

# Test the MCP serer greet tool
# asyncio.run(call_tool("Ford"))

# Test the MCP serer capture_image
# asyncio.run(call_capture_image("./test.jpg"))

# Test the MCP serer detect faces. 
# Note: this will fail if we do not pass the detected face image
# asyncio.run(call_detect_faces("./input.jpg"))

# Test the MCP serer face identifier.
# asyncio.run(call_identify_face("./face_0.jpg", "./captured_image.jpg" ))

# Test the MCP serer face identifier.
asyncio.run(call_face_matcher("source.jpg", "target.jpg" ))