#!/bin/bash
# Read base64 from environment variable and pipe to OCR script
echo "$OCR_BASE64" | uv run ocr_safe.py
