# OCR API

A lightweight REST API built with FastAPI that extracts text from images using Optical Character Recognition (OCR).

## Description

OCR API provides a simple HTTP interface for performing OCR on uploaded images. The service is built with [FastAPI](https://fastapi.tiangolo.com/) and runs on [Uvicorn](https://www.uvicorn.org/). It exposes a root health/check endpoint and a `/api/v1/extract_text` endpoint that accepts one or more image uploads and returns the extracted text using Tesseract OCR.

## Prerequisites

- Python 3.13+
- `pip` or a compatible package installer
- Tesseract OCR installed on your system (e.g., `brew install tesseract` on macOS)
- OCR engine dependencies: `pytesseract`, `Pillow`

## Setup

1. Clone the repository:

   ```bash
   git clone git@github-b:OmarMWarraich/ocr-api.git
   cd ocr-api
   ```

2. (Recommended) Create and activate a virtual environment:

   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Tesseract OCR:

   - macOS: `brew install tesseract`
   - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
   - Windows: download the installer from [github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes `fastapi`, `uvicorn`, `pytesseract`, and `Pillow`.

## Running the App

Start the development server with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Endpoints

| Method | Endpoint              | Description                               |
|--------|-----------------------|-------------------------------------------|
| GET    | `/`                   | Returns a welcome message and API hint    |
| POST   | `/api/v1/extract_text`| Upload one or more images and extract text|

## Testing Endpoints with curl

### Root endpoint

```bash
curl -X GET http://127.0.0.1:8000/
```

Expected response:

```json
{"message":"Visit the endpoint: /api/v1/extract_text to perform OCR."}
```

### Extract text from one or more images

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/extract_text" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "Images=@/path/to/your/image.png"
```

Expected response:

```json
{
  "image.png": "extracted text from image",
  "Time Taken": 2.15
}
```

To upload multiple images, repeat the `-F` flag:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/extract_text" \
     -F "Images=@image1.png" \
     -F "Images=@image2.png"
```

### Interactive API documentation

FastAPI automatically generates interactive docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
