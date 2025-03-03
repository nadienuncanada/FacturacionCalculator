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
        if len(partes) > 4:
            usuarios.add(partes[5])
    return usuarios


def login_wrapper(args):
    """Envuelve la función Login.login para incrementar el contador."""
    cred, path_to_chromedriver, download_path, periodo_facturacion, counter = args
    result = Login.login(cred, path_to_chromedriver,
                         download_path, periodo_facturacion)
    counter.value += 1  # Incrementar el contador
    return result


def filtrar_credenciales_procesadas(credentials):
    usuarios_existentes = obtener_usuarios_desde_archivos(
        get_resource_path("archivosdescomprimidos"))
    usuarios_existentes.update(
        obtener_usuarios_desde_archivos(get_resource_path("archivos"))
    )
    return [cred for cred in credentials if cred[0] not in usuarios_existentes]


def start_login_processes(periodo_facturacion, counter):
    path_to_chromedriver = get_resource_path(r"chromedriver\chromedriver.exe")
    download_path = get_resource_path("archivos")
    credentials_file = get_resource_path("Credentials.txt")

    with open(credentials_file, 'r', encoding='utf-8') as file:
        credentials = [line.strip().replace('[', '').replace(']', '').split()
                       for line in file.readlines()]
    # Obtener los usuarios (CUITs) ya procesados
    credentials_filtradas = filtrar_credenciales_procesadas(
        credentials)

    # Preparar los argumentos para el Pool
    args_list = [(cred, path_to_chromedriver, download_path, periodo_facturacion, counter)
                 for cred in credentials_filtradas]

    pool = multiprocessing.Pool(processes=4)
    # Usar map en lugar de starmap
    results = pool.map(login_wrapper, args_list)
    pool.close()
    pool.join()

    return results


def run(periodo_facturacion, counter):
    results = start_login_processes(periodo_facturacion, counter)
    descomprimir.run()
    return results
