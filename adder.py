import pandas as pd
import os
from routesResolver import get_resource_path


def run():
    messages = []

    def procesar_archivo(archivo):

        df = pd.read_csv(archivo, sep=';')

        # Convertir la columna 'Imp. Total' a números
        df['Imp. Total'] = df['Imp. Total'].str.replace(',', '.').astype(float)

        tipo_13 = df.loc[df['Tipo de Comprobante'] == 13].groupby('Punto de Venta')[
            'Imp. Total'].sum().reindex(df['Punto de Venta'].unique(), fill_value=0)
        no_tipo_13 = df.loc[df['Tipo de Comprobante'] != 13].groupby('Punto de Venta')[
            'Imp. Total'].sum().reindex(df['Punto de Venta'].unique(), fill_value=0)

        if tipo_13.empty:
            tipo_13 = pd.Series(dtype=float)
        if no_tipo_13.empty:
            no_tipo_13 = pd.Series(dtype=float)

        # Restar los valores donde el tipo de comprobante es 13
        suma_por_punto_venta = no_tipo_13 - tipo_13

        # Limpiar la salida, solo mostrar los valores
        resultado = suma_por_punto_venta[suma_por_punto_venta != 0].replace(
            '.', ',')
        if resultado.empty:
            return "1: 0"
        else:
            return "\n".join(f"{punto_venta}: {str(valor).replace('.', ',')}" for punto_venta, valor in resultado.items() if valor != 0)

    directorio = (get_resource_path('archivosDescomprimidos'))

    archivos = os.listdir(directorio)

    # Abrir el archivo de salida
    with open(get_resource_path('resultado.txt'), 'w') as output_file:
        for archivo in archivos:
            if archivo.endswith('.csv'):
                nombre_archivo = archivo.split('_')[5]
                ruta_completa = os.path.join(directorio, archivo)
                suma_por_punto_venta = procesar_archivo(ruta_completa)
                output_file.write(f"Cuit {nombre_archivo}\n")
                output_file.write(f"{suma_por_punto_venta}\n")
                output_file.write("\n")
    return "\n".join(messages)
