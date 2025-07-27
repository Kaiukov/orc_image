#!/usr/bin/env python3
import sys
import os
import argparse
import re
from PIL import Image
import pytesseract

def correct_currency_symbols(text):
    """
    Correct common OCR misreadings of Ukrainian currency symbols and patterns
    """
    # Common corrections for Ukrainian hryvnia symbol
    corrections = [
        # Fix hryvnia symbol misread as 2
        (r'(\d+\.\d+)\s*2\s*$', r'\1 ₴'),  # 300.00 2 -> 300.00 ₴
        (r'(\d+\.\d+)2\s*$', r'\1₴'),      # 300.002 -> 300.00₴
        (r'(\d+)\s*2\s*$', r'\1 ₴'),        # 300 2 -> 300 ₴
        (r'(\d+)2\s*$', r'\1₴'),            # 3002 -> 300₴
        
        # Fix hryvnia at the end of lines containing numbers
        (r'(-?\d+\.?\d*)\s*2(\s*$)', r'\1 ₴\2'),
        
        # Fix other common misreadings
        (r'(\d+\.\d+)\s*z\s*$', r'\1 ₴'),  # sometimes ₴ is read as 'z'
        (r'(\d+\.\d+)z\s*$', r'\1₴'),
        (r'(\d+\.\d+)\s*е\s*$', r'\1 ₴'),  # sometimes ₴ is read as 'е'
        (r'(\d+\.\d+)е\s*$', r'\1₴'),
        
        # Common Ukrainian text corrections
        (r'Розваги та спорт', 'Розваги та спорт'),
        (r'Залишок', 'Залишок'),
        (r'Oплата в інтернеті', 'Оплата в інтернеті'),
        (r'Роздiлити витрату', 'Розділити витрату'),
        (r'Переглянути квитанцiю', 'Переглянути квитанцію'),
        (r'Налаштування платежiв', 'Налаштування платежів'),
        (r'Поставити запитання', 'Поставити запитання'),
        
        # Fix О (Latin O) vs О (Cyrillic O) confusion
        (r'Oпис', 'Опис'),
    ]
    
    corrected_text = text
    for pattern, replacement in corrections:
        corrected_text = re.sub(pattern, replacement, corrected_text, flags=re.MULTILINE)
    
    return corrected_text

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='OCR from binary image data')
    parser.add_argument('file_path', nargs='?', help='Temporary file path for cleanup')
    parser.add_argument('--lang', '-l', default='eng+ukr+rus', 
                       help='Language(s) for OCR (default: eng+ukr+rus)')
    parser.add_argument('--list-langs', action='store_true',
                       help='List available languages and exit')
    parser.add_argument('--no-correction', action='store_true',
                       help='Skip post-processing corrections')
    
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
        
        # Apply corrections unless disabled
        if not args.no_correction:
            text = correct_currency_symbols(text)
        
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
