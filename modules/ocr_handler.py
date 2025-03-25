# funcao para OCR - arquivos PDF como imagem

import pytesseract
from pdf2image import convert_from_path
import os
import logging
from concurrent.futures import ThreadPoolExecutor
import unicodedata

# Configuração do caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\pulinan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuração adicional do Tesseract
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜàáâãäåçèéêëìíîïòóôõöùúûü"'

def extract_text_from_image_pdf(pdf_path, dpi=300):
    try:
        images = convert_from_path(pdf_path, dpi=dpi)

        def process_page(image, page_num):
            logging.info(f"Processando OCR na página {page_num} do arquivo: {os.path.basename(pdf_path)}")
            return pytesseract.image_to_string(image, lang="por", config=custom_config)

        with ThreadPoolExecutor() as executor:
            extracted_text = list(executor.map(process_page, images, range(1, len(images) + 1)))

        return "\n".join(extracted_text)
    except Exception as e:
        logging.error(f"Erro ao processar OCR no arquivo {pdf_path}: {e}")
        return ""

def is_image_pdf(pdf_path):
    from PyPDF2 import PdfReader
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            if page.extract_text().strip():
                return False
        sample_text = extract_text_from_image_pdf(pdf_path, dpi=100)
        return not bool(sample_text.strip())
    except Exception as e:
        logging.error(f"Erro ao verificar se o PDF é baseado em imagens: {e}")
        return True
