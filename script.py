import pandas as pd
import os


def procesar_archivo(archivo):
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv(archivo, sep=';')

    # Convertir la columna 'Imp. Total' a números
    df['Imp. Total'] = df['Imp. Total'].str.replace(',', '.').astype(float)

    tipo_13 = df.loc[df['Tipo de Comprobante'] == 13].groupby('Punto de Venta')[
        'Imp. Total'].sum()
    no_tipo_13 = df.loc[df['Tipo de Comprobante'] != 13].groupby('Punto de Venta')[
        'Imp. Total'].sum()

    # Llenar los valores faltantes con 0 antes de realizar la resta
    # Restar los valores donde el tipo de comprobante es 13
    if tipo_13.empty:
        tipo_13 = 0
    if no_tipo_13.empty:
        no_tipo_13 = 0
    resultado = no_tipo_13 - tipo_13

    return str(resultado).replace('.', ',')


# Directorio que contiene los archivos CSV
directorio = 'C:/Users/Capi/Desktop/mamá/archivos'

# Obtener la lista de archivos en el directorio
archivos = os.listdir(directorio)


# Abrir el archivo de salida
with open('resultado.txt', 'w') as output_file:
    # Iterar sobre cada archivo en el directorio
    for archivo in archivos:
        # Comprobar si es un archivo CSV
        if archivo.endswith('.csv'):
            # Obtener la sexta parte del nombre del archivo
            nombre_archivo = archivo.split('_')[5]

            # Ruta completa del archivo
            ruta_completa = os.path.join(directorio, archivo)

            # Llamamos a la función para procesar el archivo y obtener la suma por punto de venta
            suma_por_punto_venta = procesar_archivo(ruta_completa)

            # Escribir en el archivo de salida
            if len(suma_por_punto_venta) == 1:
                output_file.write(f"Cuit: {nombre_archivo} Valor: {
                                  suma_por_punto_venta}\n")
            else:
                output_file.write(f"Cuit: {nombre_archivo}\n")
                output_file.write(f"{suma_por_punto_venta}\n")
            # Para separar los registros con una línea en blanco
            output_file.write("\n")
