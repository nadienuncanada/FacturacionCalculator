import os
import glob
import zipfile
# Ruta al directorio donde se descargan los archivos
download_path = os.path.abspath(r".\archivos")
extract_path= os.path.abspath(r".\archivosDescomprimidos")
# Función para descomprimir un archivo ZIP y eliminar el archivo original
def unzip_and_delete(zip_file, extract_to):
    try:
        # Abre el archivo ZIP
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Extrae todos los archivos a la carpeta especificada
            zip_ref.extractall(extract_to)
            print(f"Archivo descomprimido: {zip_file}")
        
        # # Borra el archivo ZIP original
        # os.remove(zip_file)
        # print(f"Archivo eliminado: {zip_file}")
    
    except Exception as e:
        print(f"Error al descomprimir o eliminar {zip_file}: {e}")

# Función para descomprimir todos los archivos ZIP de una carpeta
def unzip_all_in_folder(folder_path, extract_to):
    # Encuentra todos los archivos .zip en la carpeta
    zip_files = glob.glob(os.path.join(folder_path, '*.zip'))

    for zip_file in zip_files:
        unzip_and_delete(zip_file, extract_to)

# Función para limpiar la carpeta de descargas// NO ES NECESARIA SI UTILIZO LAS LINEAS DE os.remove, dentro de unzip and delete.
def clean_download_folder(download_path):
    files = glob.glob(os.path.join(download_path, '*'))  # Obtiene todos los archivos en la carpeta
    for file in files:
        try:
            os.remove(file)  # Elimina cada archivo
        except Exception as e:
            print(f"No se pudo eliminar {file}: {e}")

def run():
    # Limpiar la carpeta donde se van a extraer los archivos
    # clean_download_folder(extract_path)  

    # Descomprimir todos los archivos ZIP en la carpeta de extraidos
    unzip_all_in_folder(download_path,extract_path)

    # # Limpiar la carpeta archivos descargados
    # clean_download_folder(download_path) 


    return("Proceso de descompresión y limpieza finalizado.")
