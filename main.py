import cv2
import numpy as np
import pytesseract
from PIL import Image
import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import io

# Ensure pytesseract is in your PATH or specify the path:
# pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'

app = FastAPI()

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshold

def extract_text(image):
    # Preprocess the image
    preprocessed = preprocess_image(image)
    # Extract text using pytesseract
    text = pytesseract.image_to_string(preprocessed)
    return text.strip()

def extract_tabular_data(image):
    # Preprocess the image
    preprocessed = preprocess_image(image)
    # Extract table data using pytesseract
    data = pytesseract.image_to_data(preprocessed, output_type=pytesseract.Output.DATAFRAME)
    # Filter out empty text
    data = data[data.text.notnull()]
    # Group by line number
    lines = data.groupby('line_num')['text'].apply(' '.join).reset_index()
    return lines.to_dict('records')

@app.post("/extract_text")
async def extract_text_api(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    text = extract_text(image)
    tabular_data = extract_tabular_data(image)
    
    return JSONResponse({
        "non_tabular_text": text,
        "tabular_data": tabular_data
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1000)
