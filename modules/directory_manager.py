import os
import shutil
import logging

logger = logging.getLogger(__name__)

def rename_directories(base_directory):
    """
    Renomeia pastas no diretório base, mesclando conteúdo caso necessário.
    """
    for folder in os.listdir(base_directory):
        full_path = os.path.join(base_directory, folder)

        if os.path.isdir(full_path):
            new_name = folder.split('_')[0].strip()
            new_path = os.path.join(base_directory, new_name)

            if os.path.exists(new_path):
                try:
                    for item in os.listdir(full_path):
                        source = os.path.join(full_path, item)
                        destination = os.path.join(new_path, item)

                        if os.path.exists(destination):
                            if os.path.isdir(source) and os.path.isdir(destination):
                                shutil.copytree(source, destination, dirs_exist_ok=True)
                            else:
                                shutil.copy2(source, destination)
                        else:
                            shutil.move(source, destination)

                    os.rmdir(full_path)
                    logger.info(f"Conteudo mesclado: {folder} -> {new_name}")

                except Exception as e:
                    logger.error(f"Erro ao mesclar conteudo de {folder}: {e}", exc_info=True)
            else:
                try:
                    os.rename(full_path, new_path)
                    logger.info(f"Renomeado: {folder} -> {new_name}")
                except Exception as e:
                    logger.error(f"Erro ao renomear {folder}: {e}", exc_info=True)
