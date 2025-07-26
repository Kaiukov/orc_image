#!/usr/bin/env python3
import sys
import base64
from io import BytesIO
from PIL import Image
import pytesseract

def main():
    if len(sys.argv) == 2:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            base64_input = f.read().strip()
    else:
        # Read from stdin
        base64_input = sys.stdin.read().strip()
    
    if not base64_input:
        print("Error: No input provided", file=sys.stderr)
        sys.exit(1)
    
    try:
        image_bytes = base64.b64decode(base64_input)
        image = Image.open(BytesIO(image_bytes))
        extracted_text = pytesseract.image_to_string(image)
        print(extracted_text.strip())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
