import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import os
import tkinter as tk
from routesResolver import get_resource_path


def run():

    # Paso 1: Autenticarse con la API de Google
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds_path = get_resource_path(r".\config\credencial.json")

    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open(
        "2025 claves y facturaciones")
    worksheet = spreadsheet.worksheet("claves mensuales")
    try:
        data = worksheet.get_all_values()

        # Filtrar filas donde ni la columna 4 ni la columna 7 estén vacías
        filas_filtradas = [fila for fila in data if len(
            fila) > 6 and fila[3] and fila[6]]

        # Extraer los valores de la columna 4 y la columna 7 solo de las filas filtradas
        columna_4 = [fila[3] for fila in filas_filtradas]
        columna_7 = [fila[6] for fila in filas_filtradas]

        # Crear archivo .txt para guardar los resultados
        output_file = get_resource_path(r".\data\Credentials.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, fila in enumerate(filas_filtradas):
                if i < len(filas_filtradas) - 1:
                    f.write(f"[{fila[3]}] [{fila[6]}]\n")
                else:
                    f.write(f"[{fila[3]}] [{fila[6]}]")
    except Exception as e:
        return f"Error al obtener las credenciales"
    return f"✅ Se han obtenido las credenciales de {len(filas_filtradas)} usuarios."
