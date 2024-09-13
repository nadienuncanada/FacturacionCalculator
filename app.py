import tkinter as tk
import adder
import spreadsheetWriter
from tkinter import messagebox


def update_result(message):
    result_text.set(message)


def run_script_1():
    try:
        adder.run()
        update_result(
            "Los archivos han sido procesados y el archivo de resultado ha sido generado.")
    except Exception as e:
        update_result(f"Error al procesar archivos: {e}")


def run_script_2():
    try:
        spreadsheetWriter.run()
        update_result("Los datos han sido cargados en la hoja de cálculo.")
    except Exception as e:
        update_result(f"Error al cargar datos: {e}")


# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz Gráfica")
root.geometry("600x400")

# Crear un área de texto para mostrar los resultados
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=500)
result_label.pack(pady=20)

# Botón para ejecutar el primer script
button1 = tk.Button(root, text="Procesar archivos",
                    command=run_script_1, width=20, height=2, font=('Arial', 14))
button1.pack(pady=10)

# Botón para ejecutar el segundo script
button2 = tk.Button(root, text="Subir datos",
                    command=run_script_2, width=20, height=2, font=('Arial', 14))
button2.pack(pady=10)

# Ejecutar el bucle principal
root.mainloop()
