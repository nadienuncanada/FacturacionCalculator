import pandas as pd
import os

def run():
    messages = []
    def procesar_archivo(archivo):
        # Cargar el archivo CSV en un DataFrame
        df = pd.read_csv(archivo, sep=';')

        # Convertir la columna 'Imp. Total' a números
        df['Imp. Total'] = df['Imp. Total'].str.replace(',', '.').astype(float)

        # Agrupar por 'Punto de Venta' y calcular la suma de 'Imp. Total'
        suma_por_punto_venta = df.groupby('Punto de Venta')['Imp. Total'].sum()

        tipo_13 = df.loc[df['Tipo de Comprobante'] == 13].groupby('Punto de Venta')[
            'Imp. Total'].sum()
        no_tipo_13 = df.loc[df['Tipo de Comprobante'] != 13].groupby('Punto de Venta')[
            'Imp. Total'].sum()

        # Llenar los valores faltantes con 0 antes de realizar la resta
        if tipo_13.empty:
            tipo_13 = 0
        if no_tipo_13.empty:
            no_tipo_13 = 0

        # Restar los valores donde el tipo de comprobante es 13
        resultado = no_tipo_13 - tipo_13

        return suma_por_punto_venta, str(resultado).replace('.', ',')

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
                suma_por_punto_venta, resultado = procesar_archivo(ruta_completa)

                # Comprobar el número de puntos de venta
                num_puntos_venta = suma_por_punto_venta.index.size

                # Escribir siempre en el archivo
                output_file.write(f"Cuit: {nombre_archivo}\n")
                output_file.write(f"Resultado: {resultado}\n")
                
                if num_puntos_venta > 1:
                    # Si hay más de un punto de venta, imprimir en consola
                    messages.append( f"Cuit: {nombre_archivo} tiene más de un punto de venta:")
                    for punto_venta in suma_por_punto_venta.index:
                        messages.append(f"- {punto_venta}: {suma_por_punto_venta[punto_venta]:,.2f}")
                else:
                    # Si solo hay un punto de venta, solo escribimos su resultado
                    output_file.write("\n")
                
                output_file.write("\n")
                  # Para separar los registros con una línea en blanco
    return "\n".join(messages)