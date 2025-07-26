#!/usr/bin/env python3
import sys
from PIL import Image
import pytesseract

def main():
    try:
        # Read binary data from stdin
        image_data = sys.stdin.buffer.read()
        
        if not image_data:
            print("Error: No binary data provided", file=sys.stderr)
            sys.exit(1)
        
        # Open image directly from binary data
        from io import BytesIO
        image = Image.open(BytesIO(image_data))
        
        # Extract text
        text = pytesseract.image_to_string(image)
        print(text.strip())
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
