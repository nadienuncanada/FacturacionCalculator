import multiprocessing
import Login
import os
import descomprimir


def start_login_processes():
    path_to_chromedriver = r".\chromedriver\chromedriver.exe"
    download_path = os.path.abspath(r".\archivos")
    credentials_file = "Credentials.txt"

    with open(credentials_file, 'r', encoding='utf-8') as file:
        credentials = [line.strip().replace('[', '').replace(']', '').split()
                       for line in file.readlines()]

    pool = multiprocessing.Pool(processes=2)
    pool.starmap_async(Login.login, [
                       (cred, path_to_chromedriver, download_path) for cred in credentials])
    return pool


def run():
    pool = start_login_processes()
    pool.close()
    pool.join()
    descomprimir.run()
    return "Proceso de login múltiple completado."
