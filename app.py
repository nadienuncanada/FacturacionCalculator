import tkinter as tk
import adder
import spreadsheetWriter
import getCredentials
import multiprocessing_login
from tkinter import messagebox
import multiprocessing
import os


def update_result(message):
    result_text.set(message)


def update_message_area(message):
    message_text.config(state=tk.NORMAL)
    message_text.delete(1.0, tk.END)
    message_text.insert(tk.END, message)
    message_text.config(state=tk.DISABLED)


def update_message2_area(message):
    message_text2.config(state=tk.NORMAL)
    message_text2.delete(1.0, tk.END)
    message_text2.insert(tk.END, message)
    message_text2.config(state=tk.DISABLED)


def run_script_1():
    global login_pool  # Mantén una referencia global al Pool de procesos
    worksheet_name = entry1.get()
    if not worksheet_name:
        messagebox.showerror(
            "Error", "El nombre de la pestaña no puede estar vacío.")
        return
    # try:
    #     res = getCredentials.run()
    #     update_result(res)
    # except Exception as e:
    #     update_result(f"Error al obtener credenciales: {e}")

    try:
        # Inicia los procesos de login
        results = multiprocessing_login.run()
        update_message2_area("\n".join(results))
        update_result("Los procesos de login han finalizado.")
    except Exception as e:
        update_result(f"Error al iniciar sesión: {e}")

    try:
        messages = adder.run()
        update_result(
            "Los archivos han sido procesados y el archivo de resultado ha sido generado.")
        update_message_area(messages)
    except Exception as e:
        update_result(f"Error al procesar archivos: {e}")

    # try:
    #     messages = spreadsheetWriter.run(worksheet_name)
    #     update_message_area(messages)
    #     update_result("Los datos han sido cargados en la hoja de cálculo.")
    # except Exception as e:
    #     update_result(f"Error al cargar datos: {e}")


def on_closing():
    global login_pool
    if login_pool:
        login_pool.terminate()  # Termina todos los procesos activos
        login_pool.join()  # Espera a que terminen los procesos
    root.destroy()  # Cierra la ventana


if __name__ == "__main__":
    # Configuración para evitar reinicios
    multiprocessing.set_start_method("spawn")
    root = tk.Tk()
    root.iconbitmap('iconoInterfaz.ico')
    root.title("Facturador")
    root.geometry("1000x700")

    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, wraplength=500)
    result_label.pack(pady=20)

    tk.Label(root, text="Nombre de la pestaña(Mes de la Hoja):",
             font=('Arial', 12)).pack(pady=5)
    entry1 = tk.Entry(root, font=('Arial', 12), width=40)
    entry1.pack(pady=5)

    button1 = tk.Button(root, text="Obtener credenciales",
                        command=run_script_1, width=20, height=2, font=('Arial', 14))
    button1.pack(pady=10)

    login_title = tk.Label(
        root, text="Mensajes de Login (MultiProcessing)", font=('Arial', 12, 'bold'))
    login_title.pack(pady=(10, 0))

    message_text2 = tk.Text(root, height=10, width=70)
    message_text2.pack(pady=10)
    message_text2.config(state=tk.DISABLED)

    login_title = tk.Label(
        root, text="Mensajes del Escritor del SpreadSheet", font=('Arial', 12, 'bold'))
    login_title.pack(pady=(10, 0))

    message_text = tk.Text(root, height=10, width=70)
    message_text.pack(pady=20)
    message_text.config(state=tk.DISABLED)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    login_pool = None
    root.mainloop()
