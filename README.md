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

> **Tip:** The `@` before the path is required so curl uploads the file rather than sending the path as plain text. If the path starts with `~`, use `$HOME` or an absolute path so the shell expands it:
>
> ```bash
> -F "Images=@$HOME/Downloads/test.png"
> ```

### Interactive API documentation

FastAPI automatically generates interactive docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

In Swagger UI, expand the `/api/v1/extract_text` endpoint, click **Try it out**, and use the **Choose File** buttons under the `Images` array to select one or more images. Then click **Execute** to run the OCR.

> **Note:** The app overrides the generated OpenAPI schema so that Swagger UI renders each `Images` array item as a file picker (`format: binary`) rather than a plain text field. If you see an **Add string item** button, do not use it; use the existing **Choose File** rows instead.
>
> **Background:** FastAPI defaults to emitting OpenAPI 3.1, where binary file arrays are described with `contentMediaType: application/octet-stream`. Swagger UI v5 sometimes renders that as an **Add string item** text box, which submits the value as a string and causes FastAPI to respond with:
>
> ```json
> {"detail":[{"type":"value_error","loc":["body","Images",0],"msg":"Value error, Expected UploadFile, received: <class 'str'>",...}]}
> ```
>
> The fix applied in `main.py` is to override `app.openapi()` and patch the request-body schema so that `Images.items` uses the OpenAPI 3.0 `format: binary` style, which Swagger UI reliably renders as **Choose File** buttons.
