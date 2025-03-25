# Processa arquivos PDF em um diretório de entrada, identifica o município correspondente e move os arquivos para pastas. 
# Após o processamento, renomeia e organiza os diretórios.

import sys
import os

# Adiciona o diretório raiz ao sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

from modules.pdf_reader import process_pdf
from modules.nlp_handler import identify_municipality
from modules.file_manager import move_file_to_folder
from modules.ocr_handler import is_image_pdf, extract_text_from_image_pdf
from modules.directory_manager import rename_directories

INPUT_DIR = r"C:\ProjetosDev\project\data\input"
OUTPUT_DIR = r"C:\ProjetosDev\project\data\processed"

def main():
    # Lista de arquivos PDF no diretório de entrada
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

    for file_name in files:
        file_path = os.path.join(INPUT_DIR, file_name)
        
        print(f"Processing: {file_name}")

        # Verifica se o PDF contém imagens ou texto
        if is_image_pdf(file_path):
            print(f"PDF {file_name} é baseado em imagens. Usando OCR para extrair texto.")
            text = extract_text_from_image_pdf(file_path)
        else:
            print(f"PDF {file_name} contém texto. Extraindo diretamente.")
            text = process_pdf(file_path)
        
        if not text.strip():  # Verifica se o texto extraído está vazio
            print(f"Failed to extract text from: {file_name}")
            continue
        
        # Identifica o município com base no texto extraído
        municipality = identify_municipality(text)
        print(f"Identified Municipality: {municipality}")
        
        # Move o arquivo para a pasta correspondente
        move_file_to_folder(file_path, municipality, OUTPUT_DIR)
    
    # Renomeia e organiza os diretórios após todo o processamento
    print("Renomeando e organizando diretórios...")
    rename_directories(INPUT_DIR)

if __name__ == "__main__":
    main()
