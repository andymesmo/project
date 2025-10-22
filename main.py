"""
Processamento Automatizado de PDFs por Município
------------------------------------------------

Este script processa arquivos PDF em um diretório de entrada, identifica o município 
correspondente através de análise de texto e organiza os arquivos em pastas específicas.
Otimizado para lidar com grandes volumes usando processamento paralelo.

DEPENDÊNCIAS NECESSÁRIAS:
------------------------
pip install PyMuPDF         # Para extração direta de texto de PDFs
pip install pytesseract     # Interface Python para Tesseract OCR
pip install pdf2image       # Conversão de PDF para imagem
pip install Pillow          # Processamento de imagens (dependency do pdf2image)
pip install opencv-python   # Processamento avançado de imagens
pip install numpy           # Operações numéricas (dependency do OpenCV)

DEPENDÊNCIAS EXTERNAS:
---------------------
1. Tesseract OCR:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: sudo apt-get install tesseract-ocr
   - macOS: brew install tesseract

2. Poppler (para pdf2image):
   - Windows: https://blog.alivate.com.au/poppler-windows/
   - Linux: sudo apt-get install poppler-utils
   - macOS: brew install poppler

Autor: Andy
Data: 03/09/2025
Versão: 1.0
"""

import sys
import os
import logging
from datetime import datetime
from typing import List
from concurrent.futures import ProcessPoolExecutor, as_completed

# Adiciona o diretório raiz ao sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

from modules.pdf_reader import process_pdf
from modules.nlp_handler import identify_municipality
from modules.file_manager import move_file_to_folder
from modules.ocr_handler import is_image_pdf, extract_text_from_image_pdf
from modules.directory_manager import rename_directories

# Constantes
INPUT_DIR: str = r"C:\ProjetosDev\project\data\input"
OUTPUT_DIR: str = r"C:\ProjetosDev\project\data\processed"
LOG_DIR: str = r"C:\ProjetosDev\project\data\logs"

# Configuração de logging
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = datetime.now().strftime("pipeline_%Y%m%d_%H%M%S.log")
log_path = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(
    level=logging.INFO,  # Use DEBUG para mais detalhes
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Função para processar um único PDF
def process_single_pdf(file_name: str) -> str:
    file_path = os.path.join(INPUT_DIR, file_name)

    try:
        # Decide se precisa de OCR ou não
        if is_image_pdf(file_path):
            text = extract_text_from_image_pdf(file_path)
        else:
            text = process_pdf(file_path)

        # Identifica município (fallback para 'Desconhecido')
        municipality = identify_municipality(text or "")
        
        # Move o arquivo
        move_file_to_folder(file_path, municipality, OUTPUT_DIR)

        return f"{file_name} -> {municipality}"

    except Exception as e:
        return f"Erro: {file_name} -> {e}"

# Função principal
def main(batch_size: int = 1000, max_workers: int = 8) -> None:
    """
    Processa arquivos PDF em lotes (batch) usando paralelismo.
    
    Args:
        batch_size (int): Quantidade de arquivos a processar por vez.
        max_workers (int): Número máximo de processos em paralelo.
    """
    files: List[str] = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

    logger.info(f"Total de arquivos encontrados: {len(files)}")
    if not files:
        logger.info("Nenhum PDF encontrado no diretorio de entrada.")
        return

    # Função auxiliar para dividir lista em lotes
    def chunked(iterable, size):
        for i in range(0, len(iterable), size):
            yield iterable[i:i + size]

    for batch_num, batch in enumerate(chunked(files, batch_size), start=1):
        logger.info(f"Processando lote {batch_num} com {len(batch)} arquivos...")

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_single_pdf, f): f for f in batch}
            for future in as_completed(futures):
                result = future.result()
                logger.info(result)

    logger.info("Renomeando e organizando diretorios...")
    rename_directories(INPUT_DIR)

if __name__ == "__main__":
    main()
