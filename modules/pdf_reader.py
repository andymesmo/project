import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path):
    try:
        with fitz.open(file_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
            logger.info(f"Texto extraido de {file_path} com PyMuPDF ({len(text)} caracteres).")
            return text
    except Exception as e:
        logger.error(f"Erro ao extrair texto de {file_path} com PyMuPDF: {e}", exc_info=True)
        return None

def extract_text_from_image_pdf(file_path):
    try:
        images = convert_from_path(file_path)
        text = ""
        for i, image in enumerate(images, start=1):
            logger.info(f"Executando OCR na pagina {i} do arquivo {file_path}")
            text += pytesseract.image_to_string(image, lang='por')
        return text
    except Exception as e:
        logger.error(f"Erro ao extrair texto por OCR de {file_path}: {e}", exc_info=True)
        return None

def process_pdf(file_path):
    logger.info(f"Iniciando processamento do arquivo {file_path}")
    text = extract_text_from_pdf(file_path)
    if text and text.strip():
        return text
    else:
        logger.warning(f"Nenhum texto encontrado no PDF {file_path}. Tentando OCR...")
        return extract_text_from_image_pdf(file_path)
