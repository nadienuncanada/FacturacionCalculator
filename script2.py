import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re


# Paso 1: Autenticarse con la API de Google
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "C:/Users/Capi/Desktop/mamá/mama-12345-d8e50fd8bcf3.json", scope)
client = gspread.authorize(creds)

sheets = client.openall()
for sheet in sheets:
    print(sheet.title)

# Abrir la hoja de cálculo
spreadsheet = client.open("Copia de Claves y anio 2024")  # Ajusta el nombre
# Ajusta el nombre de la pestaña
worksheet = spreadsheet.worksheet("Agosto")


# Paso 2: Leer el archivo txt
with open('C:/Users/Capi/Desktop/mamá/resultado.txt', 'r') as file:
    data = file.read()

# Paso 3: Extraer la información relevante con expresiones regulares
patron_cuit = re.compile(r"Cuit: (\d+)")
patron_vta = re.compile(r"Punto de Venta\s*\d+\s+([\d,\.]+)")

# Buscar todos los CUITs y los puntos de venta
cuit_list = patron_cuit.findall(data)
vta_list = patron_vta.findall(data)

# Paso 4: Escribir los datos en la hoja de cálculo
for i, cuit in enumerate(cuit_list):
    # Encontrar la fila correspondiente al CUIT en la hoja de cálculo
    cell = worksheet.find(cuit)
    if cell:
        # Escribir el valor de punto de venta en la columna correspondiente
        # Asegúrate de ajustar el índice de la columna según el formato
        worksheet.update_cell(cell.row, cell.col + 1,
                              vta_list[i].replace(",", ""))
    else:
        print(f"CUIT {cuit} no encontrado en la hoja.")
