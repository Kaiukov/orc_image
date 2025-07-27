#!/usr/bin/env python3
import sys
import os
import argparse
from PIL import Image
import pytesseract

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='OCR from binary image data')
    parser.add_argument('file_path', nargs='?', help='Temporary file path for cleanup')
    parser.add_argument('--lang', '-l', default='eng+ukr+rus', 
                       help='Language(s) for OCR (default: eng+ukr+rus)')
    parser.add_argument('--list-langs', action='store_true',
                       help='List available languages and exit')
    
    args = parser.parse_args()
    
    # List available languages if requested
    if args.list_langs:
        try:
            langs = pytesseract.get_languages()
            print("Available languages:")
            for lang in sorted(langs):
                print(f"  {lang}")
            return
        except Exception as e:
            print(f"Error getting languages: {e}", file=sys.stderr)
            sys.exit(1)
    
    try:
        # Read binary data from stdin
        image_data = sys.stdin.buffer.read()
        
        if not image_data:
            print("Error: No binary data provided", file=sys.stderr)
            sys.exit(1)
        
        # Open image directly from binary data
        from io import BytesIO
        image = Image.open(BytesIO(image_data))
        
        # Extract text with specified language(s)
        text = pytesseract.image_to_string(image, lang=args.lang)
        print(text.strip())
        
        # Clean up temp file if it exists and is in /tmp/
        if args.file_path and args.file_path.startswith('/tmp/') and os.path.exists(args.file_path):
            try:
                os.remove(args.file_path)
            except Exception:
                pass  # Ignore cleanup errors
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
