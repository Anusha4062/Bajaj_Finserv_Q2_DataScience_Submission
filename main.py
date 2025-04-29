from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io
from utils import extract_text_from_image, parse_lab_report, is_test_out_of_range

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI OCR Service is running."}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Read the uploaded file contents
    contents = await file.read()

    try:
        # Load image from the file
        image = Image.open(io.BytesIO(contents))

        # Run OCR using pytesseract to extract text
        extracted_text = pytesseract.image_to_string(image)

        # Parse lab test data from the extracted text
        lab_tests = parse_lab_report(extracted_text)

        # Check for tests out of range
        for test in lab_tests:
            test_value = float(test['test_value'])
            reference_range = test['bio_reference_range']
            if is_test_out_of_range(test_value, reference_range):
                test['status'] = 'Out of range'
            else:
                test['status'] = 'Normal'

        # Return the parsed lab tests with status
        return JSONResponse(content={
            "filename": file.filename,
            "lab_tests": lab_tests
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
