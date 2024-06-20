import streamlit as st
# Use st.cache_data for caching to avoid deprecation warning

import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

def load_data():
    # Sample data generation
    np.random.seed(0)
    dates = pd.date_range('20230101', periods=6)
   df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
    return df


def main():
    st.title("Invoice OCR Application")
    uploaded_file = st.file_uploader("Upload an invoice image (JPG, PNG, or PDF)", type=["jpg", "png", "pdf"])
    if uploaded_file is not None:
        with st.spinner('Processing...'):
            try:
                # Save the uploaded file temporarily
                with open("temp_file", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                extracted_text = perform_ocr("temp_file")

                st.write("### Extracted Text")
                st.write(extracted_text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
def perform_ocr(file_path):
    import pytesseract
    from PIL import Image
    import pdf2image
    if file_path.endswith(".pdf"):
        images = pdf2image.convert_from_path(file_path)
        text = " "
                  for image in images:
              text += pytesseract.image_to_string(image)

    else:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
    return text
if __name__ == "__main__":
    main()
