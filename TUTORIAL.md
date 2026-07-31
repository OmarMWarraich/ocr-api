# OCR API — Development Tutorial

This document outlines the steps taken to build the OCR API from scratch.

## Step 1: Initialize the project

Create a new directory for the project and initialize a Git repository:

```bash
mkdir ocr-api
cd ocr-api
git init
```

## Step 2: Create the Python virtual environment

Create and activate a Python 3.13 virtual environment to isolate dependencies:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

## Step 3: Install core dependencies

Install FastAPI, Uvicorn, and the OCR libraries:

```bash
pip install fastapi uvicorn pytesseract pillow
```

After installing, freeze the dependencies to a `requirements.txt` file:

```bash
pip freeze > requirements.txt
```

## Step 4: Create the basic FastAPI app

Create `main.py` with a minimal FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Visit the endpoint: /api/v1/extract_text to perform OCR."}
```

This provides a root endpoint that confirms the server is running and points users to the planned OCR endpoint.

## Step 5: Add an async OCR helper

Create `ocr.py` with an asynchronous helper function that wraps Tesseract OCR and simulates non-blocking I/O with `asyncio.sleep`:

```python
import pytesseract
import asyncio

async def read_image(img_path, lang='eng'):
    try:
        text = pytesseract.image_to_string(img_path, lang=lang)
        await asyncio.sleep(2)
        return text
    except:
        return "[ERROR] Unable to process file: {0}".format(img_path)
```

This helper performs the OCR work asynchronously and returns either the extracted text or a friendly error message.

## Step 6: Add a file-save utility

Create `utils.py` to persist uploaded files to disk with safe filename handling:

```python
from fastapi import UploadFile
import shutil
import os

def _save_file_to_server(uploaded_file: UploadFile, path: str = "./", save_as: str | None = None) -> str:
    filename = uploaded_file.filename or "upload"
    extension = os.path.splitext(filename)[-1]
    if save_as is None:
        save_as = os.path.splitext(filename)[0] or "upload"

    save_as_stem, save_as_ext = os.path.splitext(save_as)
    if not save_as_ext:
        save_as_ext = extension

    temp_file = os.path.join(path, save_as_stem + save_as_ext)

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    return temp_file
```

This utility handles missing filenames and avoids duplicating file extensions when `save_as` already includes one (e.g., passing `img.filename` directly).

## Step 7: Add the OCR endpoint

Update `main.py` to import the helper modules and expose the POST endpoint that accepts one or more image uploads:

```python
from typing import List
import time
import ocr
import utils
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Visit the endpoint: /api/v1/extract_text to perform OCR."}

@app.post("/api/v1/extract_text")
async def extract_text(Images: List[UploadFile] = File(...)):
    response = {}
    s = time.time()
    for img in Images:
        if not img.filename:
            raise HTTPException(status_code=400, detail="Uploaded file is missing a filename")

        print("Images Uploaded: ", img.filename)
        temp_file = utils._save_file_to_server(img, path="./", save_as=img.filename)
        text = await ocr.read_image(temp_file)
        response[img.filename] = text
    response["Time Taken"] = round((time.time() - s), 2)

    return response
```

The endpoint saves each image, runs OCR on it, and returns a dictionary mapping filenames to extracted text plus the total time taken.

## Step 8: Run the development server

Start Uvicorn with auto-reload enabled:

```bash
uvicorn main:app --reload
```

Verify the root endpoint responds correctly:

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{"message":"Visit the endpoint: /api/v1/extract_text to perform OCR."}
```

Test the OCR endpoint with a sample image:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/extract_text" \
     -F "Images=@sample_image.png"
```

## Next Steps

1. Add input validation and file-type checks for uploads.
2. Improve error handling for unreadable images or missing Tesseract.
3. Add unit and integration tests.
4. Containerize the application with Docker.
