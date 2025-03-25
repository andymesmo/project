# funcao para ler PDFs

import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def extract_text_from_pdf(file_path):
    try:
        with fitz.open(file_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
            return text
    except Exception:
        return None

def extract_text_from_image_pdf(file_path):
    try:
        images = convert_from_path(file_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image, lang='por')  # OCR para português
        return text
    except Exception:
        return None

def process_pdf(file_path):
    text = extract_text_from_pdf(file_path)
    if text and text.strip():
        return text
    else:
        return extract_text_from_image_pdf(file_path)