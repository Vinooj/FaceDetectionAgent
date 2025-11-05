
import argparse
import json
from face_recognition import face_matcher

def main():
    """Main function to run the face matcher test."""
    parser = argparse.ArgumentParser(description="Test the face_matcher function with real images.")
    parser.add_argument("--source", default="./input.jpg", help="Path to the source image.")
    parser.add_argument("--target", default="./captured_image.jpg", help="Path to the target image.")
    args = parser.parse_args()

    print(f"Running face_matcher with source: {args.source} and target: {args.target}")
    results = face_matcher(args.source, args.target)

    print("\n--- Results ---")
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
