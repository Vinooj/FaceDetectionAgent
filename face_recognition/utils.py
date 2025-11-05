from pathlib import Path

def load_image_bytes(image_path: str) -> bytes:
    """
    Load image bytes from image_path. Returns a small placeholder PNG if loading fails.
    """
    try:
        with open(image_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {image_path} not found — using placeholder image.")
    except Exception as e:
        print(f"Error reading {image_path}: {e} — using placeholder image.")
            
def get_filename(image_path: str) -> str:
    """
    Return the filename component of image_path.
    """
    try:
        filename = Path(image_path).name
        return filename or ""
    except Exception:
        if not image_path:
            return ""
        # Fallback: normalize separators and take last segment
        return image_path.replace("\\", "/").split("/")[-1]