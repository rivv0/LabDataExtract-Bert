# Core FastAPI framework
from fastapi import FastAPI, UploadFile, File, HTTPException

from typing import List
from PIL import Image
import pytesseract
import io
from aiolimiter import AsyncLimiter
import logging

from validators.composite_validator import CompositeValidator
from validators.extention_validator import ExtensionValidator
from validators.mime_validator import MimeValidator
from validators.size_validator import SizeValidator
from processors.pdf_processor import PDFProcessor
from models.openai_models import OpenAIModel
from known_tests import KNOWN_TESTS
from utils import filter_known_tests

# Initialize the FastAPI application
app = FastAPI()

# Set a limit of 10 requests per minute
limiter = AsyncLimiter(max_rate=10, time_period=60)

@app.get("/")
async def root():
    """
    Root endpoint, redirect to /extract
    """
    return {"message": "Welcome to the Lab Results extraction API for the Medsender Challenge. Visit /docs for an interface to use the extract endpoint."}



@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    """
    Accepts a single PDF or image file, extracts lab test names and values.
    """
    try:
        filename = file.filename.lower()
        if filename.endswith(".pdf"):
            pdf_processor = PDFProcessor(file)
            text = await pdf_processor.extract_text()
        elif filename.endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff")):
            content = await file.read()
            image = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(image)
        else:
            raise HTTPException(status_code=400, detail="Only PDF or image files are supported.")

        model = OpenAIModel("gpt-4o-mini")
        result = model.get_fields(text)
        if "lab_results" in result:
            result["lab_results"] = filter_known_tests(result["lab_results"], KNOWN_TESTS)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
