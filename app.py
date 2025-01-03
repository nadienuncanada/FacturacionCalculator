import tkinter as tk
import adder
import spreadsheetWriter
import getCredentials
import multiprocessing_login
from tkinter import messagebox

def update_result(message):
    result_text.set(message)

def update_message_area(message):
    message_text.config(state=tk.NORMAL)  # Habilitar el texto para poder actualizar
    message_text.delete(1.0, tk.END)  # Borra el contenido anterior
    message_text.insert(tk.END, message)  # Inserta el nuevo mensaje
    message_text.config(state=tk.DISABLED)  # Deshabilitar el texto para hacerlo de solo lectura

def update_message2_area(message):
    message_text2.config(state=tk.NORMAL)  # Habilitar el texto para poder actualizar
    message_text2.delete(1.0, tk.END)  # Borra el contenido anterior
    message_text2.insert(tk.END, message)  # Inserta el nuevo mensaje
    message_text2.config(state=tk.DISABLED)  # Deshabilitar el texto para hacerlo de solo lectura    

def run_script_1():
  #Transformar spreadsheet de los datos de todas las cuentas a txt-> Credentials.txt
  try:
    res=getCredentials.run()
    update_result(res)
  except Exception as e:
    update_result(f"Error al obtener credenciales: {e}")
  #Utilizar las credenciales para descargar los archivos mediante multilogeos
  try:
    res=multiprocessing_login.run()
    update_message2_area(res)
  except Exception as e:
    update_result(f"Error al iniciar sesión: {e}")  
  # #Apartir de todos los archivos csv descargador y descomprimidos en archivosDescomprimidos, realiza los calculo necesarios.
  try:
    messages = adder.run()  
    update_result("Los archivos han sido procesados y el archivo de resultado ha sido generado.")
    update_message_area(messages) 
  except Exception as e:
    update_result(f"Error al procesar archivos: {e}")

  # Obtener los valores de las casillas de entrada
  worksheet_name = entry1.get()
  # Cargar los datos en la hoja de cálculo que el adder dejo.
  try:
    if not worksheet_name:
      messagebox.showerror("Error", "El nombre de la pestaña no puede estar vacío.")
      return
    messages=spreadsheetWriter.run(worksheet_name)
    update_message_area(messages) 
    update_result("Los datos han sido cargados en la hoja de cálculo.")
  except Exception as e:
    update_result(f"Error al cargar datos: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz Gráfica")
root.geometry("1000x1000")

# Crear un área de texto para mostrar los resultados
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=500)
result_label.pack(pady=20)

# Crear una etiqueta y un campo de entrada para el nombre de la pestaña
tk.Label(root, text="Nombre de la pestaña(MesDeLaHoja):", font=('Arial', 12)).pack(pady=5)
entry1 = tk.Entry(root, font=('Arial', 12), width=40)
entry1.pack(pady=5)

# Botón para ejecutar el primer script
button1 = tk.Button(root, text="Obtener credenciales", command=run_script_1, width=20, height=2, font=('Arial', 14))
button1.pack(pady=10)

# Crear una etiqueta como título para el área de mensajes específicos de Login
login_title = tk.Label(root, text="Mensajes de Login (MultiProcessing)", font=('Arial', 12, 'bold'))
login_title.pack(pady=(10, 0))  # Añade espacio solo arriba del título

# Crear un área de texto para mostrar mensajes específicos de Login (MultiProcessing)
message_text2 = tk.Text(root, height=10, width=70)  # Ajusta el tamaño según necesites
message_text2.pack(pady=10)  # Ajusta el espacio debajo del área de texto

# Configurar el área de texto como de solo lectura
message_text2.config(state=tk.DISABLED)  # Deshabilitar el texto al inicio

# Crear una etiqueta como título para el área de mensajes específicos de spreadsheetWriter
login_title = tk.Label(root, text="Mensajes del Escritor del SpreadSheet", font=('Arial', 12, 'bold'))
login_title.pack(pady=(10, 0))  # Añade espacio solo arriba del título
# Crear un área de texto para mostrar mensajes específicos de spreadsheetWriter
message_text = tk.Text(root, height=10, width=70)  # Ajusta el tamaño según necesites
message_text.pack(pady=20)

# Configurar el área de texto como de solo lectura
message_text.config(state=tk.DISABLED)  # Deshabilitar el texto al inicio

# Ejecutar el bucle principal
root.mainloop()