import os
import sys


def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # Si estamos dentro de un ejecutable, obtenemos la ruta del ejecutable
        base_path = sys._MEIPASS
    else:
        # Si estamos en el entorno de desarrollo, usamos la ruta del script
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
