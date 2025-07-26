# OCR Binary Script

Extract text from images using OCR. Reads binary image data from stdin and outputs extracted text.

## Prerequisites

Install Tesseract OCR:
- **macOS**: `brew install tesseract`
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`

## Usage

```bash
cat /path/to/image.png | uv run ocr_binary.py [file_path]
```

- Reads binary image data from stdin
- Optional file path argument for cleanup (removes `/tmp/` files after processing)
- Outputs extracted text to stdout

## Example

```bash
# Basic usage
cat image.png | uv run ocr_binary.py

# With temp file cleanup
cat /tmp/temp_image.jpg | uv run ocr_binary.py "/tmp/temp_image.jpg"
```

## Dependencies

Managed by `uv` via `pyproject.toml`:
- Pillow (image processing)
- pytesseract (OCR interface)
