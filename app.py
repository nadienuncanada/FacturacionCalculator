import tkinter as tk
import adder
import spreadsheetWriter
import getCredentials
import Login
from tkinter import messagebox

def update_result(message):
    result_text.set(message)

def update_message_area(message):
    message_text.config(state=tk.NORMAL)  # Habilitar el texto para poder actualizar
    message_text.delete(1.0, tk.END)  # Borra el contenido anterior
    message_text.insert(tk.END, message)  # Inserta el nuevo mensaje
    message_text.config(state=tk.DISABLED)  # Deshabilitar el texto para hacerlo de solo lectura

def run_script_1():
    try:
        messages = adder.run()  
        update_result("Los archivos han sido procesados y el archivo de resultado ha sido generado.")
        update_message_area(messages) 
    except Exception as e:
        update_result(f"Error al procesar archivos: {e}")

def run_script_2():
    # Obtener los valores de las casillas de entrada
    worksheet_name = entry1.get()

    try:
        if not worksheet_name:
            messagebox.showerror("Error", "El nombre de la pestaña no puede estar vacío.")
            return
        spreadsheetWriter.run(worksheet_name)
        update_result("Los datos han sido cargados en la hoja de cálculo.")
    except Exception as e:
        update_result(f"Error al cargar datos: {e}")

def run_script_3():
    try:
       res=getCredentials.run()
       update_result(res)
    except Exception as e:
        update_result(f"Error al obtener credenciales: {e}")
        
def run_script_4():
    try:
        Login.run()
        update_result("Se ha iniciado sesión correctamente.")
    except Exception as e:
        update_result(f"Error al iniciar sesión: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz Gráfica")
root.geometry("600x450")

# Crear un área de texto para mostrar los resultados
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=500)
result_label.pack(pady=20)

# Botón para ejecutar el tercer script
button3 = tk.Button(root, text="Conseguir Credenciales", command=run_script_3, width=20, height=2, font=('Arial', 14))
button3.pack(pady=10)

# Botón para ejecutar el cuarto script
button4 = tk.Button(root, text="Conseguir archivos", command=run_script_4, width=20, height=2, font=('Arial', 14))
button4.pack(pady=10)

# Botón para ejecutar el primer script
button1 = tk.Button(root, text="Procesar archivos", command=run_script_1, width=20, height=2, font=('Arial', 14))
button1.pack(pady=10)

# Crear una etiqueta y un campo de entrada para el nombre de la pestaña
tk.Label(root, text="Nombre de la pestaña:", font=('Arial', 12)).pack(pady=5)
entry1 = tk.Entry(root, font=('Arial', 12), width=40)
entry1.pack(pady=5)

# Botón para ejecutar el segundo script
button2 = tk.Button(root, text="Subir datos", command=run_script_2, width=20, height=2, font=('Arial', 14))
button2.pack(pady=10)

# Crear un área de texto para mostrar mensajes específicos de spreadsheetWriter
message_text = tk.Text(root, height=10, width=70)  # Ajusta el tamaño según necesites
message_text.pack(pady=20)

# Configurar el área de texto como de solo lectura
message_text.config(state=tk.DISABLED)  # Deshabilitar el texto al inicio

# Ejecutar el bucle principal
root.mainloop()
