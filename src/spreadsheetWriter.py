import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import os

from routesResolver import get_resource_path


def run(worksheet_name, file_name):

    # Autenticarse con la API de Google
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds_path = get_resource_path(r".\config\credencial.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    try:
        # Abrir la hoja de cálculo
        spreadsheet = client.open(file_name)
        worksheet = spreadsheet.worksheet(worksheet_name)

    except gspread.SpreadsheetNotFound:
        raise Exception(f"❌ La hoja de cálculo '{
                        file_name}' no fue encontrada.")
    except gspread.WorksheetNotFound:
        raise Exception(f"❌ La hoja de trabajo '{
                        worksheet_name}' no existe en el archivo.")
    except Exception as e:
        raise Exception(
            f"❌ Se produjo un error al intentar acceder a la hoja")

    # Leer el archivo txt
    path = get_resource_path(r'data\resultado.txt')
    with open(path, 'r') as file:
        data = file.read()

    # Extraer la información relevante con expresiones regulares
    patron_cuit = re.compile(r"Cuit\s*(\d{11})")
    patron_vta = re.compile(r"^(\d+):\s*([\d,]+)", re.MULTILINE)

    cuit_vta_dict = {}
    lines = data.strip().splitlines()
    current_cuit = None

    for line in lines:
        cuit_match = patron_cuit.search(line)
        vta_match = patron_vta.search(line)

        if cuit_match:
            current_cuit = cuit_match.group(1)
            if current_cuit not in cuit_vta_dict:
                cuit_vta_dict[current_cuit] = []
        elif vta_match and current_cuit:
            point = vta_match.group(1)
            value = vta_match.group(2)
            cuit_vta_dict[current_cuit].append((point, value))

    # Escribir los datos en la hoja de cálculo
    messages = []
    all_values = worksheet.get_all_values()

    for cuit, vtas in cuit_vta_dict.items():
        # print(f"🔍 CUIT: {cuit}, VTAS: {vtas}")
        found = False
        for row_num, row in enumerate(all_values):
            if cuit in row:
                found = True
                col_num = row.index(cuit)

                # Obtener el valor actual en la celda
                current_value = worksheet.cell(row_num + 1, col_num + 2).value

                if len(vtas) > 1:
                    new_values = ', '.join(
                        [f"Punto {point}: {value}" for point, value in vtas])
                else:
                    new_values = f"{vtas[0][1]}"

                # Solo actualizar si no están ya presentes
                if not current_value:
                    worksheet.update_cell(row_num + 1, col_num + 2, new_values)
                    # messages.append(f"✅ Actualizado CUIT {cuit} con valores de venta: {new_values}")
                else:
                    messages.append(
                        f"⚠️ CUIT {cuit} ya tiene valores. No se actualizó.")

        if not found:
            messages.append(f"❌ CUIT {cuit} no encontrado en la hoja.")

    # Devolver los mensajes acumulados
    return "\n".join(messages)
