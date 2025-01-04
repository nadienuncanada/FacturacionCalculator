import multiprocessing
import Login
import os
import descomprimir

def start_login_processes():
    path_to_chromedriver = r".\chromedriver\chromedriver.exe"
    download_path = os.path.abspath(r".\archivos")
    credentials_file = "Credentials.txt"

    with open(credentials_file, 'r', encoding='utf-8') as file:
        credentials = [line.strip().replace('[', '').replace(']', '').split() for line in file.readlines()]

    pool = multiprocessing.Pool(processes=2)
    results = pool.starmap(Login.login, [(cred, path_to_chromedriver, download_path) for cred in credentials])
    pool.close()
    pool.join()
    return results

def run():
    results = start_login_processes()
    descomprimir.run()
    return results
