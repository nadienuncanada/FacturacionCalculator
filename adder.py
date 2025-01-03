import pandas as pd
import os

def run():
    messages = []
    def procesar_archivo(archivo):
        # Cargar el archivo CSV en un DataFrame
        df = pd.read_csv(archivo, sep=';')

        # Convertir la columna 'Imp. Total' a números
        df['Imp. Total'] = df['Imp. Total'].str.replace(',', '.').astype(float)

        tipo_13 = df.loc[df['Tipo de Comprobante'] == 13].groupby('Punto de Venta')['Imp. Total'].sum().reindex(df['Punto de Venta'].unique(), fill_value=0)
        no_tipo_13 = df.loc[df['Tipo de Comprobante'] != 13].groupby('Punto de Venta')['Imp. Total'].sum().reindex(df['Punto de Venta'].unique(), fill_value=0)

        if tipo_13.empty:
            tipo_13 = pd.Series(dtype=float)  # Mantiene el tipo de serie
        if no_tipo_13.empty:
            no_tipo_13 = pd.Series(dtype=float)  # Mantiene el tipo de serie

        # Restar los valores donde el tipo de comprobante es 13
        suma_por_punto_venta = no_tipo_13 - tipo_13
        
        # Limpiar la salida, solo mostrar los valores
        resultado = suma_por_punto_venta[suma_por_punto_venta != 0].replace('.', ',')
        if resultado.empty:
          return "0"
        else:
            return "\n".join(f"{punto_venta}: {str(valor).replace('.', ',')}" for punto_venta, valor in resultado.items() if valor != 0)

    base_dir = os.path.join(os.path.dirname(__file__))
    # Directorio que contiene los archivos CSV
    directorio = os.path.join(base_dir, 'archivosDescomprimidos')

    # Obtener la lista de archivos en el directorio
    archivos = os.listdir(directorio)

    # Abrir el archivo de salida
    with open(os.path.join(base_dir, 'resultado.txt'), 'w') as output_file:
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
                if((suma_por_punto_venta) == "0"):
                    messages.append(f"El archivo {archivo} no contiene datos válidos.")
                else:
                  # Escribir en el archivo de salida
                  output_file.write(f"Cuit {nombre_archivo}\n")
                  output_file.write(f"{suma_por_punto_venta}\n")
                  # Para separar los registros con una línea en blanco
                  output_file.write("\n")
    return "\n".join(messages)