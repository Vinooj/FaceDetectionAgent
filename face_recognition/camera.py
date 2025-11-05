"""Camera capture module using OpenCV."""
print("Executing camera.py")

from typing import Any, Dict
import cv2
import time

def list_cameras() -> list[int]:
    """
    Attempts to list available camera indices.
    Note: This is a heuristic and might not list all devices or work perfectly.
    """
    print("Listing available cameras")
    available_cameras = []
    for i in range(10):  # Check up to 10 possible camera indices
        cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
        if cap.isOpened():
            print(f"Camera index {i} is available.")
            available_cameras.append(i)
            cap.release()
    return available_cameras


def capture_image(file_path: str, camera_index: int = 0) -> Dict[str, Any]:
    """
    Capture an image from the specified webcam.

    Args:
        file_path: Path where the captured image will be saved
        camera_index: The index of the camera to use (default: 0)

    Returns:
        Dictionary with success status and image information
    """
    print(f"Attempting to capture image from camera {camera_index} to {file_path}")
    # Open a connection to the specified camera.
    cap = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        print(f"Error: Could not open camera with index {camera_index}.")
        return {"success": False, "error": f"Could not open camera with index {camera_index}."}

    # Capture a single frame from the camera.
    time.sleep(1)
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame from camera.")
        cap.release()
        return {"success": False, "error": "Could not read frame from camera."}

    # Save the captured frame to the specified file.
    success = cv2.imwrite(file_path, frame)

    # Release the camera resource.
    cap.release()

    if success:
        print(f"Image captured and saved as {file_path}")
        return {"success": True, "file_path": file_path}
    else:
        print(f"Error: Could not save image to {file_path}")
        return {"success": False, "error": f"Could not save image to {file_path}"}
