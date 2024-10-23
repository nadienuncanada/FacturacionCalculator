import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import os
import tkinter as tk


def run(worksheet_name):
    base_dir = os.path.join(os.path.dirname(__file__))

    # Paso 1: Autenticarse con la API de Google
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds_path = os.path.join(base_dir, "credencial.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    # Abrir la hoja de cálculo
    spreadsheet = client.open(
        "Copia de Claves y anio 2024")  # Ajusta el nombre
    # Ajusta el nombre de la pestaña
    worksheet = spreadsheet.worksheet(worksheet_name)

    # Paso 2: Leer el archivo txt
    with open(os.path.join(base_dir, 'resultado.txt'), 'r') as file:
        data = file.read()

    # Paso 3: Extraer la información relevante con expresiones regulares
    patron_cuit = re.compile(r"Cuit: (\d+)")
    patron_vta = re.compile(r"Punto de Venta\s*\d+\s+([\d,\.]+)")

    # Buscar todos los CUITs y los puntos de venta
    cuit_list = patron_cuit.findall(data)
    vta_list = patron_vta.findall(data)

    # Paso 4: Escribir los datos en la hoja de cálculo
    all_values = worksheet.get_all_values()
    for i, cuit in enumerate(cuit_list):
        found = False
        for row_num, row in enumerate(all_values):
            if cuit in row:
                found = True
                # Obtener la columna donde está el CUIT
                col_num = row.index(cuit)
                cell_value = worksheet.cell(row_num + 1, col_num + 2).value
                # Solo actualizar si la celda adyacente está vacía
                if not cell_value:
                    worksheet.update_cell(
                        row_num + 1, col_num + 2, vta_list[i])
                break
        if not found:
            print(f"CUIT {cuit} no encontrado en la hoja.")
