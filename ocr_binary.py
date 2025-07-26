#!/usr/bin/env python3
import sys
import os
from PIL import Image
import pytesseract

def main():
    try:
        # Read binary data from stdin
        image_data = sys.stdin.buffer.read()
        
        if not image_data:
            print("Error: No binary data provided", file=sys.stderr)
            sys.exit(1)
        
        # Get file path from command line arg if provided
        file_path = sys.argv[1] if len(sys.argv) > 1 else None
        
        # Open image directly from binary data
        from io import BytesIO
        image = Image.open(BytesIO(image_data))
        
        # Extract text
        text = pytesseract.image_to_string(image)
        print(text.strip())
        
        # Clean up temp file if it exists and is in /tmp/
        if file_path and file_path.startswith('/tmp/') and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Ignore cleanup errors
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
