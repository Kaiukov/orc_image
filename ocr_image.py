#!/usr/bin/env python3
"""
OCR Image Script
Reads base64 encoded image from stdin and extracts text using OCR.
Usage: echo "BASE64" | uv run ocr_image.py
"""

import sys
import base64
from io import BytesIO
from PIL import Image
import pytesseract


def main():
    try:
        # Read base64 from stdin
        base64_input = sys.stdin.read().strip()
        
        if not base64_input:
            print("Error: No input provided", file=sys.stderr)
            sys.exit(1)
        
        # Decode base64 to bytes
        try:
            image_bytes = base64.b64decode(base64_input)
        except Exception as e:
            print(f"Error: Invalid base64 input - {e}", file=sys.stderr)
            sys.exit(1)
        
        # Convert bytes to PIL Image
        try:
            image = Image.open(BytesIO(image_bytes))
        except Exception as e:
            print(f"Error: Cannot open image - {e}", file=sys.stderr)
            sys.exit(1)
        
        # Perform OCR
        try:
            extracted_text = pytesseract.image_to_string(image)
            print(extracted_text.strip())
        except Exception as e:
            print(f"Error: OCR failed - {e}", file=sys.stderr)
            sys.exit(1)
            
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
