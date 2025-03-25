# funcao NLP - modelo de ML

import re
import unicodedata

# Padrões para identificar o município
MUNICIPALITY_PATTERNS = [
    r"Prefeitura Municipal de\s+([A-Za-zÀ-ÿ\s]+)",  
    r"Prefeitura do Munic[íí]pio de\s+([A-Za-zÀ-ÿ\s]+)",  
    r"Prefeitura do\s+([A-Za-zÀ-ÿ\s]+)",  
    r"Prefeitura da Cidade do\s+([A-Za-zÀ-ÿ\s]+)",
    r"Prefeitura Municipal da Estância Turística de\s+([A-Za-zÀ-ÿ\s]+)",
    r"Prefeitura de\s+([A-Za-zÀ-ÿ\s]+)", 
    r"Pref. Munic. de\s+([A-Za-zÀ-ÿ\s]+)", 
    r"Pref. Mun. de\s+([A-Za-zÀ-ÿ\s]+)",
    r"Munic[ií]pio de\s+([A-Za-zÀ-ÿ\s]+)",  
    r"Governo do\s+([A-Za-z\s]+)",
    r"Secretaria Municipal de\s+([A-Za-zÀ-ÿ\s]+)",  
    r"Cidade de\s+([A-Za-zÀ-ÿ\s]+)",  
    r"Nota Fiscal Eletrônica de Serviços -\s+([A-Za-zÀ-ÿ\s]+)",  
    r"-\s+([A-Za-zÀ-ÿ\s]+)"  
]

def identify_municipality(text):
    """
    Identifica o município em um texto com base em padrões predefinidos.

    Args:
        text (str): Texto extraído do documento.

    Returns:
        str: Nome do município identificado ou 'Desconhecido' se não encontrado.
    """
    for pattern in MUNICIPALITY_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Remove espaços extras e caracteres desnecessários e retorna o município completo
            return clean_municipality_name(match.group(1))

    # Retorna 'Desconhecido' se nenhum padrão corresponder
    return "Desconhecido"

def clean_municipality_name(name):
    """
    Limpa e normaliza o nome do município, garantindo que não haja cortes ou erros.

    Args:
        name (str): Nome do município identificado.

    Returns:
        str: Nome do município limpo e normalizado.
    """
    # Remove espaços extras no início e no fim
    name = name.strip()
    
    # Remove acentuação
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )

    # Converte para maiúsculas
    name = name.upper()

    # Remove caracteres não desejados, como hífens ou quebras de linha
    name = re.sub(r"[^\w\sÀ-ÿ]", "", name)

    return name
