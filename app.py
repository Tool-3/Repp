import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import pytesseract
from PIL import Image
import pdf2image
import os

# Set up Tesseract OCR engine path (adjust if necessary)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' 

# --- Helper Functions ---
@st.cache_data  # Cache the OCR process for efficiency
def perform_ocr(file_path):
    """Performs OCR on the given image or PDF file."""
    if file_path.endswith(".pdf"):
        images = pdf2image.convert_from_path(file_path)
        text = "".join(pytesseract.image_to_string(image) for image in images)
    else:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
    return text

# --- Main Streamlit App ---
def main():
    st.title("Invoice OCR Application")

    uploaded_file = st.file_uploader(
        "Upload an invoice image (JPG, PNG, or PDF)", type=["jpg", "png", "pdf"]
    )

    if uploaded_file is not None:
        with st.spinner("Processing..."):
            try:
                # Create a temporary file
                with open("temp_file", "wb") as temp_file:
                    temp_file.write(uploaded_file.read())

                extracted_text = perform_ocr("temp_file")
                os.remove("temp_file")  # Clean up the temporary file

                st.write("### Extracted Text")
                st.text_area(" ", value=extracted_text, height=400)

            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

