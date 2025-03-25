# funcao para mover arquivos

import os
import shutil
import re

def sanitize_directory_name(name):
    """
    Remove caracteres inválidos de nomes de diretórios.
    Substitui caracteres proibidos por '_' e remove espaços desnecessários.
    """
    return re.sub(r'[<>:"/\\|?*\n\r\t]', '_', name).strip()

def move_file_to_folder(file_path, municipality_name, output_dir):
    """
    Move um arquivo para uma pasta específica com base no nome do município.
    Cria a pasta, se necessário, e sanitiza o nome do diretório.

    Args:
        file_path (str): Caminho completo do arquivo a ser movido.
        municipality_name (str): Nome do município.
        output_dir (str): Diretório de saída onde o arquivo será armazenado.
    """
    # Sanitiza o nome do município para evitar erros de caminho inválido
    sanitized_name = sanitize_directory_name(municipality_name)

    # Define o caminho do diretório alvo
    target_dir = os.path.join(output_dir, sanitized_name)

    # Cria o diretório, se ainda não existir
    os.makedirs(target_dir, exist_ok=True)

    # Move o arquivo para o diretório alvo
    shutil.move(file_path, os.path.join(target_dir, os.path.basename(file_path)))
