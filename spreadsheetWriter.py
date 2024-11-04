import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import os

worksheet_name = "Octubre"

def run(worksheet_name):
    base_dir = os.path.join(os.path.dirname(__file__))

    # Paso 1: Autenticarse con la API de Google
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds_path = os.path.join(base_dir, "credencial.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    # Abrir la hoja de cálculo
    spreadsheet = client.open("A Copia de Claves y anio 2024")
    worksheet = spreadsheet.worksheet(worksheet_name)

    # Paso 2: Leer el archivo txt
    with open(os.path.join(base_dir, 'resultado.txt'), 'r') as file:
        data = file.read()

    # Paso 3: Extraer la información relevante con expresiones regulares
    patron_cuit = re.compile(r"Cuit\s*(\d{11})")
    patron_vta = re.compile(r"^\d+:\s*([\d,]+)", re.MULTILINE)

    # Crear un diccionario para almacenar múltiples "Puntos de Venta" por CUIT
    cuit_vta_dict = {}
    # Dividir el contenido por líneas y eliminar líneas en blanco
    lines = data.strip().splitlines()
    
    current_cuit = None
    for line in lines:
        cuit_match = patron_cuit.search(line)
        vta_match = patron_vta.search(line)
        
        if cuit_match:  # Encontrar un nuevo CUIT
            current_cuit = cuit_match.group(1)
            if current_cuit not in cuit_vta_dict:
                cuit_vta_dict[current_cuit] = []  # Inicializa una lista para este CUIT
              

        elif vta_match and current_cuit:  # Encontrar un valor de venta
            value = vta_match.group(1)
            cuit_vta_dict[current_cuit].append(value)
            

    # Paso 4: Escribir los datos en la hoja de cálculo
    all_values = worksheet.get_all_values()
    for cuit, vtas in cuit_vta_dict.items():
        found = False
        for row_num, row in enumerate(all_values):
            if cuit in row:
                found = True
                col_num = row.index(cuit)

                # Obtener el valor actual en la celda
                current_value = worksheet.cell(row_num + 1, col_num + 2).value
                
                # Crear una cadena con todos los valores separados por coma
                new_values = ', '.join(vtas)
                if(len(vtas) > 1):
                  new_values = f"(la cuit tiene mas de un punto de venta) {new_values}"

                # Solo actualizar si no están ya presentes
                if not current_value:  # Si está vacío
                    print(f"Actualizando CUIT {cuit} con valores de venta: {new_values}")
                    worksheet.update_cell(row_num + 1, col_num + 2, new_values)
                
        if not found:
            print(f"CUIT {cuit} no encontrado en la hoja.")

run(worksheet_name)
