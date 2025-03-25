import os
import shutil

def rename_directories(base_directory):
    """
    Renomeia pastas no diretório base, mesclando conteúdo caso necessário.
    """
    for folder in os.listdir(base_directory):
        full_path = os.path.join(base_directory, folder)

        # Verifica se é uma pasta
        if os.path.isdir(full_path):
            # Extrai o nome antes do primeiro '_'
            new_name = folder.split('_')[0].strip()
            new_path = os.path.join(base_directory, new_name)

            # Caso o novo nome já exista, mesclar o conteúdo
            if os.path.exists(new_path):
                try:
                    for item in os.listdir(full_path):
                        source = os.path.join(full_path, item)
                        destination = os.path.join(new_path, item)

                        if os.path.exists(destination):
                            # Se já existir um arquivo ou pasta com o mesmo nome, sobrescreve/mescla
                            if os.path.isdir(source) and os.path.isdir(destination):
                                # Recursivamente mesclar pastas
                                shutil.copytree(source, destination, dirs_exist_ok=True)
                            else:
                                # Sobrescrever arquivos
                                shutil.copy2(source, destination)
                        else:
                            # Move o arquivo ou pasta se não existir no destino
                            shutil.move(source, destination)

                    # Após mesclar o conteúdo, remover a pasta original vazia
                    os.rmdir(full_path)
                    print(f"Conteúdo mesclado: {folder} -> {new_name}")

                except Exception as e:
                    print(f"Erro ao mesclar conteúdo de {folder}: {e}")
            else:
                # Renomeia a pasta diretamente se o nome não existir
                try:
                    os.rename(full_path, new_path)
                    print(f"Renomeado: {folder} -> {new_name}")
                except Exception as e:
                    print(f"Erro ao renomear {folder}: {e}")
