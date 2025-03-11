import os
import glob
import zipfile
from routesResolver import get_resource_path
extract_path = get_resource_path(r"data\archivosDescomprimidos")
download_path = get_resource_path(r"data\archivos")
# Función para descomprimir un archivo ZIP y eliminar el archivo original


def unzip_and_delete(zip_file, extract_to):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        # # Borra el archivo ZIP original
        # os.remove(zip_file)
        # print(f"Archivo eliminado: {zip_file}")

    except Exception as e:
        print(f"Error al descomprimir {zip_file}: {e}")

# Función para descomprimir todos los archivos ZIP de una carpeta


def unzip_all_in_folder(folder_path, extract_to):
    zip_files = glob.glob(os.path.join(folder_path, '*.zip'))
    for zip_file in zip_files:
        unzip_and_delete(zip_file, extract_to)

# Función para limpiar la carpeta de descargas// NO ES NECESARIA SI UTILIZO LAS LINEAS DE os.remove, dentro de unzip and delete.


def clean_download_folder(download_path):
    files = glob.glob(os.path.join(download_path, '*'))
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"No se pudo eliminar {file}: {e}")


def run_clean_download_folder():
    # Limpiar la carpeta donde se van a extraer los archivos
    clean_download_folder(download_path)


def count_files_in_folder():
    files = glob.glob(os.path.join(extract_path, '*'))
    return len(files)


def run_clean_extract_folder():
    # Limpiar la carpeta donde se van a extraer los archivos
    clean_download_folder(extract_path)


def run():
    unzip_all_in_folder(download_path, extract_path)
    clean_download_folder(download_path)
    return ("Proceso de descompresión y limpieza finalizado.")
