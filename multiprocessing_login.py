import multiprocessing
import Login
import os
import descomprimir
from multiprocessing import Pool

def run_multiprocessing():
    # Ruta al archivo chromedriver.exe
    path_to_chromedriver = r".\chromedriver\chromedriver.exe"
    # Configura tu driver de Selenium donde se descargarán los archivos
    download_path = os.path.abspath(r".\archivos")
    # Ruta al archivo de credenciales
    credentials_file = "Credentials.txt"

    # Leer todas las credenciales del archivo
    with open(credentials_file, 'r', encoding='utf-8') as file:
        credentials = [line.strip().replace('[', '').replace(']', '').split() for line in file.readlines()]

    pool = Pool(processes=2)  # Número de procesos
    pool.starmap(Login.login, [(cred, path_to_chromedriver, download_path) for cred in credentials])
    pool.close()
    pool.join()

    #descomprimir.run()#Descomprime los archivos descargados en la carpeta archivosDescomprimidos
    return("Proceso de login múltiple completado.")


if __name__ == "__main__":
    run_multiprocessing()