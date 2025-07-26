#!/usr/bin/env python3
import sys
import json
import os
from PIL import Image
import pytesseract

def main():
    try:
        # Read binary data from stdin
        image_data = sys.stdin.buffer.read()
        
        if not image_data:
            print(json.dumps({"error": "No binary data provided"}), file=sys.stderr)
            sys.exit(1)
        
        # Get file path from environment variable or command line arg
        file_path = os.environ.get('FILE_PATH') or (sys.argv[1] if len(sys.argv) > 1 else 'stdin')
        
        # Open image directly from binary data
        from io import BytesIO
        image = Image.open(BytesIO(image_data))
        
        # Extract text
        text = pytesseract.image_to_string(image).strip()
        
        # Clean up temp file if it exists and is in /tmp/
        if file_path.startswith('/tmp/') and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Ignore cleanup errors
        
        # Return JSON response
        result = {
            "ocr_text": text,
            "path_to_file": file_path
        }
        
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            "error": str(e),
            "path_to_file": os.environ.get('FILE_PATH', 'stdin')
        }
        print(json.dumps(error_result), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
