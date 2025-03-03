import queue
import sys
import threading
import time
import tkinter as tk
import adder as adder
import spreadsheetWriter as spreadsheetWriter
import getCredentials as getCredentials
import multiprocessing_login as multiprocessing_login
from tkinter import Toplevel, messagebox
import multiprocessing
import os
import descomprimir as descomprimir
from routesResolver import get_resource_path
import psutil


def update_result(message):
    result_text.set(message)


def update_message_area(message):
    if not message or message.isspace():
        return

    message = message.rstrip("\n")

    message_text.config(state=tk.NORMAL)
    message_text.insert(tk.END, message + "\n")
    message_text.config(state=tk.DISABLED)
    message_text.see(tk.END)


def update_message3_area(message):
    if not message or message.isspace():
        return

    message = message.rstrip("\n")
    message_text3.config(state=tk.NORMAL)
    message_text3.delete(1.0, tk.END)
    message_text3.insert(tk.END, message + "\n")
    message_text3.config(state=tk.DISABLED)
    message_text3.see(tk.END)


def process_files(message_queue, counter):
    try:
        periodo_facturacion = selected_option_facturacion.get()
        results = multiprocessing_login.run(
            periodo_facturacion, counter)  # Pasar el contador
        print(results)

        filtered_results = [
            str(item) if item is not None else "" for item in results
        ]

        final_message = "\n".join(
            filter(lambda x: x.strip(), filtered_results))

        message_queue.put(
            (final_message, "✅ Los procesos de login han finalizado."))
    except Exception as e:
        error_message = f"❌ Error al iniciar sesiones (pedí ayuda, probablemente se actualizó Chrome)"
        message_queue.put((None, error_message))
        print(e)

    try:
        messages = adder.run()
        message_queue.put(("✅ Los archivos han sido procesados", None))
    except Exception as e:
        error_message = f"❌ Error al procesar archivos: {e}"
        message_queue.put((None, error_message))
        print(e)


def run_script_1():
    global login_processes
    try:
         # Verificar si la carpeta 'data' existe, si no, crearla
        data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
        if not os.path.exists(data_folder):
          os.makedirs(data_folder)
          archivos_folder = os.path.join(data_folder, 'archivos')
          os.makedirs(archivos_folder)
          archivos_descomprimidos_folder = os.path.join(data_folder, 'archivosDescomprimidos')
          os.makedirs(archivos_descomprimidos_folder)
        res = getCredentials.run()
        update_result(res)
    except Exception as e:
        update_result(f"Error al obtener credenciales: {e}")

    def check_queue(message_queue):
        try:
            while True:
                message, result = message_queue.get_nowait()
                if message:
                    update_message_area(message)
                if result:
                    update_result(result)
        except queue.Empty:
            pass
        root.after(100, check_queue, message_queue)

    # Crear un Manager y un contador compartido
    manager = multiprocessing.Manager()
    counter = manager.Value('i', 0)  # 'i' indica un entero

    # Función para actualizar el contador en la interfaz
    
    global total_credentials
    total_credentials = len(
      multiprocessing_login.filtrar_credenciales_procesadas(get_credentials_list()))
    
    def update_counter():
        # Obtener el total de credenciales
        completed = counter.value  # Logins completados
        login_counter.set(f"Completados: {completed} De: {total_credentials}")
        root.after(1000, update_counter)  # Actualizar cada segundo

    message_queue = queue.Queue()
    thread = threading.Thread(target=process_files,
                              args=(message_queue, counter))
    thread.start()

    root.after(100, check_queue, message_queue)
    root.after(1000, update_counter)  # Iniciar la actualización del contador

def get_credentials_list():
    """Obtiene la lista de credenciales desde el archivo."""
    credentials_file = get_resource_path(r".\data\Credentials.txt")
    with open(credentials_file, 'r', encoding='utf-8') as file:
        credentials = [line.strip().replace('[', '').replace(']', '').split()
                       for line in file.readlines()]
    return credentials


def run_spreadsheet_writer():

    file_name = input_field.get() if selected_option.get(
    ) == "Otro" else selected_option.get()

    worksheet_name = entry1.get()

    if not worksheet_name:
        messagebox.showerror(
            "Error", "❌ El nombre de la pestaña no puede estar vacío.")
        return

    if file_name == "Otro" or not file_name.strip():
        messagebox.showerror(
            "Error", "❌ Debes ingresar un nombre de archivo válido.")
        return

    try:

        messages = spreadsheetWriter.run(worksheet_name, file_name)
        update_message3_area(f"{messages}")
        update_result("✅ Los datos han sido cargados en la hoja de cálculo.")
        run_eliminar_archivos()
    except Exception as e:
        update_result(f"❌ Error al cargar datos: {e}")


def run_eliminar_archivos():
    descomprimir.run_clean_download_folder()
    update_result("✅ La carpeta de archivos ha sido limpiada correctamente.")


def on_closing():
    procesos_relacionados = [
        "python.exe",
        "Facturador.exe",
        "Python.exe",
    ]

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in procesos_relacionados:
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    root.quit()
    root.destroy()
    os._exit()


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, font=(
            'Arial', 10), bg="lightyellow", relief="solid", padx=5, pady=5)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


def show_help():
    # Crear una nueva ventana
    help_window = Toplevel()
    help_window.title("Instrucciones")
    help_window.geometry("1000x850")
    help_window.configure(bg="#ffe5ee")
    text_area = tk.Text(help_window, wrap="word", font=(
        "Arial", 12), bg="#ffffff", fg="#000000")
    text_area.pack(padx=20, pady=20, fill="both", expand=True)
    instructions = (
        "Hola, ma! Acá voy a tratar de dejarte un pequeño instructivo por si te surge alguna duda del uso del programita.\n\n"
        "Vamos de a poco:\n"
        "**Obtener archivos**: Esto lo que hace es tomar los usuarios de claves y año 2024 e intentar descargar la facturación. "
        "Con el selector que está a la izquierda del botón podés elegir si querés sacar la facturación anual o mensual. Si no tocas nada, "
        "por defecto descarga la mensual.\n\n"
        "**Archivos descargados**: Los archivos se descargan en una carpeta específica, NO en descargas. Para eso está el botón 'Abrir carpeta'. "
        "Te vas a dar cuenta que el formato es un poco distinto al que solés ver. Eso es porque son archivos tipo CSV y no Excel.\n\n"
        "**Espacio de mensajes**: El espacio de mensajes de la descarga de archivos te va a mostrar información sobre lo que pasó al intentar entrar a la AFIP. "
        "Tratamos de hacer los mensajes lo más específicos posibles, pero a veces salen errores raros o simplemente está fallando la AFIP. Si te da muchos errores, "
        "podés volver a tocar 'Obtener archivos' y va a intentar descargar solo los de aquellos clientes que no pudo descargar antes.\n\n"
        "**Selector de archivo**: Ahí dejé uno que hice para la facturación anual y también el que usás siempre para la mensual. Lo hicimos así para que, "
        "si necesitás agregar un nuevo archivo, sea muy fácil.\n\n"
        "**Nombre de la hoja de cálculo**: Donde te pide el nombre de la hoja de cálculo, tenés que tener cuidado de escribirlo tal cual aparece (respetando mayúsculas "
        "y demás). No lo probé, pero puede que las ñ y las tildes den problemas.\n\n"
        "**Cargar datos**: Cuando toques 'Cargar datos', deberían subirse todos los datos de los archivos descargados a la hoja que ingresaste. "
        "Lo hicimos de manera tal que, si ya hay datos en la columna, NO se va a actualizar. Si un cliente tiene más de un punto de venta, en el documento va a quedar el valor "
        "de todos los puntos de venta en una misma casilla.\n\n"
        "*IMPORTANTÍSIMO*: Hicimos que la descarga de archivos y la carga de resultados se haga por separado para darte más libertad a la hora de usar el programita. "
        "El tema es que tenés que tener cuidado porque, cuando tocás 'Obtener archivos', se van a descargar SIN BORRAR lo que había antes. "
        "Esto puede generar problemas si, por ejemplo, quedaron datos del mes pasado y ahora buscás los de este mes. Cuando se hace la carga de datos, "
        "sí se borra la carpeta.\n\n"
        "**Borrar archivos**: Si descargaste archivos, pero por algún motivo no querés cargarlos, podés usar el botón 'Borrar archivos'. "
        "Esto elimina los archivos descargados y evita problemas de datos duplicados. Es buena práctica borrar por las dudas siempre antes de hacer algo.\n\n"
        "Creo que eso es todo. Cualquier cosa sabés que nos podés preguntar.\n\n"
        "¡Te queremos!\nIgna y Jo ♥"
    )

    text_area.insert("1.0", instructions)
    text_area.config(state="disabled")

    close_button = tk.Button(help_window, text="Cerrar", command=help_window.destroy, font=(
        "Arial", 12), bg="#f08080", fg="white")
    close_button.pack(pady=10)


def on_enter(e, button, hover_color):
    button['bg'] = hover_color


def on_leave(e, button, original_color):
    button['bg'] = original_color


def open_file_explorer():
    folder_path = get_resource_path(r"data\archivosDescomprimidos")
    os.startfile(folder_path)

def update_input_field(*args):
      if selected_option.get() == "Otro":
          # Habilitar el campo de entrada
          input_field.config(state=tk.NORMAL)
      else:
          # Deshabilitar el campo de entrada
          input_field.config(state=tk.DISABLED)

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    root = tk.Tk()

    # Centrar la ventana en la pantalla
    root.config(bg="#ffe5ee")
    root.iconbitmap(get_resource_path(r'.\assets\iconoInterfaz.ico'))
    root.title("Facturador")

    # Definir el tamaño de la ventana
    root.geometry("800x800")

    # Crear el canvas y la barra de desplazamiento
    canvas = tk.Canvas(root, bg="#ffe5ee")
    scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scroll_y.set)

    # Centrar el canvas en la ventana
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    canvas.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    
    # Crear un frame dentro del canvas
    scrollable_frame = tk.Frame(canvas, bg="#ffe5ee")

    # Crear un frame contenedor para centrar el contenido
    container_frame = tk.Frame(scrollable_frame, bg="#ffe5ee")
    container_frame.pack(expand=True)

    # Crear un window en el canvas para agregar el frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

    # Configurar el scroll
    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Habilitar scroll con la rueda del mouse
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    button_color = "#d3a6cc"
    hover_color = "#dbbad6"
    text_box_bg = "#e7d3e0"
    text_color = "#4b0082"
    label_color = "#ffe5ee"

    # Crear el botón de ayuda
    help_button = tk.Button(
        container_frame,
        text="?",
        command=show_help,
        font=('Arial', 10, 'bold'),
        bg="#ffcccb",
        width=3,
        height=2,
        borderwidth=2,
        relief="raised"
    )
    help_button.place(x=5, y=5)

    # Crear un ToolTip para el botón de ayuda
    tooltip = ToolTip(help_button, "Haz clic para ver el instructivo.")

    # Etiqueta para mostrar el resultado
    result_text = tk.StringVar()
    result_label = tk.Label(container_frame, textvariable=result_text,
                            wraplength=500, font=('Arial', 14), bg="#ffe5ee", fg=text_color)
    result_label.pack(pady=20)

    # Lista desplegable con opciones
    options_facturacion = ["Mensual", "Anual"]
    selected_option_facturacion = tk.StringVar(root)
    selected_option_facturacion.set(options_facturacion[0])

    # Frame para organizar todos los elementos
    button_frame = tk.Frame(container_frame, bg="#ffe5ee")
    button_frame.pack(pady=10)

    # Crear el OptionMenu dentro del button_frame
    dropdown_menu_periodo = tk.OptionMenu(
        button_frame, selected_option_facturacion, *options_facturacion)
    dropdown_menu_periodo.config(
        font=('Arial', 12), bg=text_box_bg, fg=text_color)
    dropdown_menu_periodo.pack(side=tk.LEFT, padx=5)

    # Variable para el contador de logins
    login_counter = tk.StringVar()
    login_counter.set("Completados: 0  De: 0")

    # Etiqueta para mostrar el contador de logins
    login_counter_label = tk.Label(container_frame, textvariable=login_counter, font=(
        'Arial', 14), bg="#ffe5ee", fg=text_color)
    login_counter_label.pack(pady=10)

    # Crear los botones
    button1 = tk.Button(button_frame, text="Obtener archivos",
                        command=run_script_1, width=20, height=2, font=('Arial', 14), bg=button_color, fg=text_color)
    button1.pack(side=tk.LEFT, padx=5)
    button1.bind("<Enter>", lambda e: on_enter(
        e, button1, hover_color))
    button1.bind("<Leave>", lambda e: on_leave(e, button1, button_color))

    buttonBorrado = tk.Button(button_frame, text="Borrar archivos",
                              command=run_eliminar_archivos, width=15, height=2, font=('Arial', 14), bg=button_color, fg=text_color)
    buttonBorrado.pack(side=tk.LEFT, padx=5)
    buttonBorrado.bind("<Enter>", lambda e: on_enter(
        e, buttonBorrado, hover_color))
    buttonBorrado.bind("<Leave>", lambda e: on_leave(
        e, buttonBorrado, button_color))

    buttonAbirCarpeta = tk.Button(button_frame, text="Abrir carpeta",
                                  command=open_file_explorer, width=15, height=2, font=('Arial', 14), bg=button_color, fg=text_color)
    buttonAbirCarpeta.pack(side=tk.LEFT, padx=5)
    buttonAbirCarpeta.bind("<Enter>", lambda e: on_enter(
        e, buttonAbirCarpeta, hover_color))
    buttonAbirCarpeta.bind("<Leave>", lambda e: on_leave(
        e, buttonAbirCarpeta, button_color))

    # Frame para organizar los mensajes
    message_frame = tk.Frame(container_frame, bg="#ffe5ee")
    message_frame.pack(pady=10)

    # Etiqueta para "Mensajes de la descarga de archivos"
    login_title = tk.Label(
        message_frame, text="Mensajes de la descarga de archivos", font=('Arial', 12, 'bold'), bg=label_color, fg=text_color)
    login_title.grid(row=0, column=0, padx=5, pady=5)

    # Cuadro de texto para "Mensajes de la descarga de archivos"
    message_text = tk.Text(message_frame, height=10,
                           width=100, bg=text_box_bg, fg=text_color)
    message_text.grid(row=1, column=0, padx=5, pady=5)
    message_text.config(state=tk.DISABLED)

    # Entrada para "Nombre del archivo:"
    tk.Label(container_frame, text="Nombre del archivo:",
             font=('Arial', 12), bg="#ffe5ee", fg=text_color).pack(pady=5)

    options = ["2025 claves y facturaciones", "Facturacion anual", "Otro"]
    selected_option = tk.StringVar(root)
    selected_option.set(options[0])

    def update_input_field(*args):
        if selected_option.get() == "Otro":
            input_field.config(state=tk.NORMAL)
        else:
            input_field.config(state=tk.DISABLED)

    dropdown_menu = tk.OptionMenu(container_frame, selected_option, *options)
    dropdown_menu.config(font=('Arial', 12), bg=text_box_bg, fg=text_color)
    dropdown_menu.pack(pady=5)

    input_field = tk.Entry(container_frame, state=tk.DISABLED, font=(
        'Arial', 12), bg=text_box_bg, fg=text_color)
    input_field.pack(pady=5)

    selected_option.trace("w", update_input_field)

    tk.Label(container_frame, text="Nombre de la hoja de cálculo:",
             font=('Arial', 12), bg="#ffe5ee", fg=text_color).pack(pady=5)

    entry1 = tk.Entry(container_frame, font=('Arial', 12), width=40,
                      bg=text_box_bg, fg=text_color)
    entry1.pack(pady=5)

    button2 = tk.Button(container_frame, text="Cargar datos",
                        command=run_spreadsheet_writer, width=20, height=2, font=('Arial', 14), bg=button_color, fg=text_color)
    button2.pack(pady=10)
    button2.bind("<Enter>", lambda e: on_enter(e, button2, hover_color))
    button2.bind("<Leave>", lambda e: on_leave(e, button2, button_color))

    writer_title = tk.Label(
        container_frame, text="Mensajes del escritor", font=('Arial', 12, 'bold'), bg=label_color, fg=text_color)
    writer_title.pack(pady=(10, 0))

    message_text3 = tk.Text(container_frame, height=10, width=100,
                            bg=text_box_bg, fg=text_color)
    message_text3.pack(pady=20)
    message_text3.config(state=tk.DISABLED)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    login_pool = None
    root.mainloop()