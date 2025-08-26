"""
Processamento Automatizado de PDFs por Município

Este script processa arquivos PDF em um diretório de entrada, identifica o município 
correspondente através de análise de texto e organiza os arquivos em pastas específicas.
Após o processamento, os diretórios são renomeados e organizados.

Autor: Andy
Data de criação: N/A
Última atualização: N/A

Bibliotecas necessárias:
- sys
- os
- Módulos personalizados:
    - pdf_reader
    - nlp_handler
    - file_manager
    - ocr_handler
    - directory_manager
"""

import sys
import os
from typing import List  # Adicionado para type hints

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

def main() -> None:
    """
    Função principal que executa o processamento dos arquivos PDF.
    """
    # Lista de arquivos PDF no diretório de entrada
    files: List[str] = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]

    for file_name in files:
        file_path = os.path.join(INPUT_DIR, file_name)
        
        print(f"Processing: {file_name}")

        try:
            # Verifica se o PDF contém imagens ou texto
            if is_image_pdf(file_path):
                print(f"PDF {file_name} eh baseado em imagens. Usando OCR para extrair texto.")
                text = extract_text_from_image_pdf(file_path)
            else:
                print(f"PDF {file_name} contem texto. Extraindo diretamente.")
                text = process_pdf(file_path)
            
            if not text.strip():  # Verifica se o texto extraído está vazio
                print(f"Failed to extract text from: {file_name}")
                continue
            
            # Identifica o município com base no texto extraído
            municipality = identify_municipality(text)
            print(f"Identified Municipality: {municipality}")
            
            # Move o arquivo para a pasta correspondente
            move_file_to_folder(file_path, municipality, OUTPUT_DIR)

        except Exception as e:
            print(f"Erro ao processar {file_name}: {str(e)}")
            continue
    
    # Renomeia e organiza os diretórios após todo o processamento
    print("Renomeando e organizando diretorios...")
    rename_directories(INPUT_DIR)

if __name__ == "__main__":
    main()
