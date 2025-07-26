# OCR Image Script

Python script for extracting text from images using OCR.

## Prerequisites

Install Tesseract OCR on your system:
- **macOS**: `brew install tesseract`
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

```bash
echo "BASE64_ENCODED_IMAGE" | uv run ocr_image.py
```

The script reads base64 encoded image data from stdin and outputs extracted text.

## Dependencies

Dependencies are managed automatically by `uv` via `pyproject.toml`:
- Pillow (image processing)
- pytesseract (OCR interface)
