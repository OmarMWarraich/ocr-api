from typing import Annotated
import time
import asyncio
import ocr
import utils
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.openapi.utils import get_openapi

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="OCR API",
        version="0.1.0",
        description="Extract text from images using Tesseract OCR.",
        routes=app.routes,
    )
    # Swagger UI renders array file uploads more reliably when each item
    # is described with OpenAPI 3.0's `format: binary` instead of OpenAPI 3.1's
    # `contentMediaType`. Patch the generated request-body schema accordingly.
    body_schema = openapi_schema["components"]["schemas"].get(
        "Body_extract_text_api_v1_extract_text_post"
    )
    if body_schema:
        body_schema["properties"]["Images"]["items"] = {
            "type": "string",
            "format": "binary",
        }

    app.openapi_schema = openapi_schema
    return openapi_schema


app.openapi = custom_openapi


@app.get("/")
def home():
    return {"message": "Visit the endpoint: /api/v1/extract_text to perform OCR."}

@app.post("/api/v1/extract_text")
async def extract_text(Images: Annotated[list[UploadFile], File(...)]):
    """Accept one or more image uploads and return the extracted text for each."""
    response = {}
    s = time.time()
    tasks = []
    for img in Images:
        if not img.filename:
            raise HTTPException(status_code=400, detail="Uploaded file is missing a filename")

        print("Images Uploaded: ", img.filename)
        temp_file = utils._save_file_to_server(img, path="./", save_as=img.filename)
        tasks.append(asyncio.create_task(ocr.read_image(temp_file)))
    text = await asyncio.gather(*tasks)
    for i in range(len(text)):
        response[Images[i].filename] = text[i]
    response["Time Taken"] = round((time.time() - s), 2)

    return response