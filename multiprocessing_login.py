import multiprocessing
import Login
import os
import descomprimir
from routesResolver import get_resource_path


def obtener_usuarios_desde_archivos(ruta_carpeta):
    """Extrae los usuarios (CUITs) de los nombres de archivo en la carpeta."""
    archivos = os.listdir(ruta_carpeta)
    usuarios = set()
    for archivo in archivos:
        partes = archivo.split('_')
        if len(partes) > 4:  # Asegura que el formato es correcto
            usuarios.add(partes[5])  # Obtén el usuario (CUIT)
    return usuarios


def start_login_processes(periodo_facturacion):
    path_to_chromedriver = get_resource_path(r"chromedriver\chromedriver.exe")
    download_path = get_resource_path("archivos")
    credentials_file = "Credentials.txt"

    with open(credentials_file, 'r', encoding='utf-8') as file:
        credentials = [line.strip().replace('[', '').replace(']', '').split()
                       for line in file.readlines()]
    # Obtener los usuarios (CUITs) ya procesados
    usuarios_existentes = obtener_usuarios_desde_archivos(
        get_resource_path("archivosdescomprimidos"))

    credentials_filtradas = [
        cred for cred in credentials if cred[0] not in usuarios_existentes]

    pool = multiprocessing.Pool(processes=2)
    results = pool.starmap(Login.login, [(
        cred, path_to_chromedriver, download_path, periodo_facturacion) for cred in credentials_filtradas])
    pool.close()
    pool.join()
    return results


def run(periodo_facturacion):
    results = start_login_processes(periodo_facturacion)
    descomprimir.run()
    return results
