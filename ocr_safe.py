#!/usr/bin/env python3
import sys
import os
import base64
from io import BytesIO
from PIL import Image
import pytesseract

def main():
    # Try environment variable first, then stdin
    base64_input = os.environ.get('IMAGE_B64') or sys.stdin.read().strip()
    
    if not base64_input:
        print("Error: No input provided", file=sys.stderr)
        sys.exit(1)
    
    try:
        image_bytes = base64.b64decode(base64_input)
        image = Image.open(BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        print(text.strip())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
