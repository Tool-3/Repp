from flask import Flask, request, jsonify
import pytesseract
import cv2
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path

def extract_text(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def extract_table(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    df = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DATAFRAME)
    df = df[df.text.notna()]
    return df.to_json(orient='records')

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith(('.png', '.jpg', '.jpeg')):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        text = extract_text(file_path)
        table = extract_table(file_path)
        os.remove(file_path)
        return jsonify({
            "text": text,
            "table": table
        })
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
