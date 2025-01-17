import tkinter as tk
import adder
import spreadsheetWriter
import getCredentials
import multiprocessing_login
from tkinter import Toplevel, messagebox
import multiprocessing
import os
import descomprimir
from routesResolver import get_resource_path


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


def update_message3_area(message):
    message_text3.config(state=tk.NORMAL)
    message_text3.delete(1.0, tk.END)
    message_text3.insert(tk.END, message)
    message_text3.config(state=tk.DISABLED)


def run_script_1():
    global login_pool  # Mantén una referencia global al Pool de procesos
    """ try:
        res = getCredentials.run()
        update_result(res)
    except Exception as e:
        update_result(f"Error al obtener credenciales: {e}") """

    try:
        # Inicia los procesos de login
        periodo_facturacion = selected_option_facturacion.get()
        results = multiprocessing_login.run(periodo_facturacion)
        print(results)
        update_message_area("\n".join(results))
        update_result("Los procesos de login han finalizado.")
    except Exception as e:
        update_result(f"Error al iniciar sesiones: {e}")

    try:
        messages = adder.run()
        update_result(
            "Los archivos han sido procesados y el archivo de resultado ha sido generado.")
        update_message2_area(messages)
    except Exception as e:
        update_result(f"Error al procesar archivos: {e}")


def run_spreadsheet_writer():
    file_name = selected_option.get()
    worksheet_name = entry1.get()
    if not worksheet_name:
        messagebox.showerror(
            "Error", "El nombre de la pestaña no puede estar vacío.")
        return
    try:
        messages = spreadsheetWriter.run(worksheet_name, file_name)
        update_message3_area(messages)
        update_result("Los datos han sido cargados en la hoja de cálculo.")
        run_eliminar_archivos()
    except Exception as e:
        update_result(f"Error al cargar datos: {e}")


def run_eliminar_archivos():
    descomprimir.run_clean_download_folder()


def on_closing():
    global login_pool
    if login_pool:
        login_pool.terminate()  # Termina todos los procesos activos
        login_pool.join()  # Espera a que terminen los procesos
    root.destroy()  # Cierra la ventana


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
    help_window.geometry("1000x850")  # Ancho x Alto
    help_window.configure(bg="#ffe5ee")  # Fondo claro

    # Crear un área de texto con scroll
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
        "**Mensajes del sumador**: Donde dice 'Mensajes del sumador' no debería aparecer nunca nada. Eso solamente va a informar si pasó algo muuuy raro.\n\n"
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
    # Hacer que el texto sea de solo lectura
    text_area.config(state="disabled")

    # Botón para cerrar
    close_button = tk.Button(help_window, text="Cerrar", command=help_window.destroy, font=(
        "Arial", 12), bg="#f08080", fg="white")
    close_button.pack(pady=10)


def on_enter(e, button, hover_color):
    button['bg'] = hover_color


def on_leave(e, button, original_color):
    button['bg'] = original_color


def open_file_explorer():
    # Ruta de la carpeta que deseas abrir
    # Ajusta la ruta de la carpeta
    folder_path = get_resource_path("archivosDescomprimidos")
    os.startfile(folder_path)  # Abre la carpeta en el explorador de archivos


if __name__ == "__main__":
    # Configuración para evitar reinicios
    multiprocessing.set_start_method("spawn")
    root = tk.Tk()

    # Establecer el color de fondo de la ventana raíz
    root.config(bg="#ffe5ee")

    # Establecer el icono y las propiedades de la ventana
    root.iconbitmap(get_resource_path('iconoInterfaz.ico'))
    root.title("Facturador")
    root.geometry("1000x800")

    # Definir colores que combinen con el rosa claro
    button_color = "#d3a6cc"  # Violeta suave para botones
    hover_color = "#dbbad6"    # Violeta más oscuro para botones al pasar el ratón
    text_box_bg = "#e7d3e0"   # Rosa suave para los cuadros de texto
    text_color = "#4b0082"     # Color de texto violeta oscuro
    label_color = "#ffe5ee"    # Color de fondo de las etiquetas
    # Crear el botón de ayuda (signo de pregunta en círculo)
    help_button = tk.Button(
        root,
        text="?",
        command=show_help,
        font=('Arial', 10, 'bold'),
        bg="#ffcccb",

        width=3,
        height=2,
        borderwidth=2,
        relief="raised"
    )

    # Ubicar el botón en la esquina superior izquierda
    help_button.place(x=5, y=5)

    # Crear un ToolTip para el botón de ayuda
    tooltip = ToolTip(help_button, "Haz clic para ver el instructivo.")

    # Etiqueta para mostrar el resultado
    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text,
                            wraplength=500, font=('Arial', 14), bg="#ffe5ee", fg=text_color)
    result_label.pack(pady=20)

    # Lista desplegable con opciones
    options_facturacion = ["Mensual", "Anual"]

    # Variable para almacenar la selección
    selected_option_facturacion = tk.StringVar(root)
    # Establecer el valor predeterminado
    selected_option_facturacion.set(options_facturacion[0])

   # Frame para organizar todos los elementos
    button_frame = tk.Frame(root, bg="#ffe5ee")
    button_frame.pack(pady=10)

    # Crear el OptionMenu dentro del button_frame
    dropdown_menu_periodo = tk.OptionMenu(
        button_frame, selected_option_facturacion, *options_facturacion)
    dropdown_menu_periodo.config(
        font=('Arial', 12), bg=text_box_bg, fg=text_color)  # Configurar estilo
    dropdown_menu_periodo.pack(side=tk.LEFT, padx=5)

    # Crear los botones con el color de fondo violeta
    button1 = tk.Button(button_frame, text="Obtener archivos",
                        command=run_script_1, width=20, height=2, font=('Arial', 14), bg=button_color, fg=text_color)
    button1.pack(side=tk.LEFT, padx=5)
    button1.bind("<Enter>", lambda e: on_enter(
        e, button1, hover_color))  # Cambiar a color hover
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
    message_frame = tk.Frame(root, bg="#ffe5ee")
    message_frame.pack(pady=10)

    # Etiqueta para "Mensajes de la descarga de archivos"
    login_title = tk.Label(
        message_frame, text="Mensajes de la descarga de archivos", font=('Arial', 12, 'bold'), bg=label_color, fg=text_color)
    login_title.grid(row=0, column=0, padx=5, pady=5)

    # Cuadro de texto para "Mensajes de la descarga de archivos"
    message_text = tk.Text(message_frame, height=10,
                           width=70, bg=text_box_bg, fg=text_color)
    message_text.grid(row=1, column=0, padx=5, pady=5)
    message_text.config(state=tk.DISABLED)

    # Etiqueta para "Mensajes del sumador"
    adder_title = tk.Label(
        message_frame, text="Mensajes del sumador", font=('Arial', 12, 'bold'), bg=label_color, fg=text_color)
    adder_title.grid(row=0, column=1, padx=5, pady=5)

    # Cuadro de texto para "Mensajes del sumador"
    message_text2 = tk.Text(message_frame, height=10,
                            width=35, bg=text_box_bg, fg=text_color)
    message_text2.grid(row=1, column=1, padx=5, pady=5)
    message_text2.config(state=tk.DISABLED)

    # Lista desplegable con opciones
    options = ["Copia de Claves y anio 2024", "Facturacion anual"]

    # Variable para almacenar la selección
    selected_option = tk.StringVar(root)
    selected_option.set(options[0])  # Establecer el valor predeterminado

    # Crear el OptionMenu
    dropdown_menu = tk.OptionMenu(root, selected_option, *options)
    dropdown_menu.config(font=('Arial', 12), bg=text_box_bg,
                         fg=text_color)  # Configurar estilo
    dropdown_menu.pack(pady=5)

    # Entrada para "Nombre de la pestaña"
    tk.Label(root, text="Nombre de la hoja de cálculo:",
             font=('Arial', 12), bg="#ffe5ee", fg=text_color).pack(pady=5)
    entry1 = tk.Entry(root, font=('Arial', 12), width=40,
                      bg=text_box_bg, fg=text_color)
    entry1.pack(pady=5)

    button2 = tk.Button(root, text="Cargar datos",
                        command=run_spreadsheet_writer, width=20, height=2, font=('Arial', 14), bg=button_color, fg=text_color)
    button2.pack(pady=10)
    button2.bind("<Enter>", lambda e: on_enter(e, button2, hover_color))
    button2.bind("<Leave>", lambda e: on_leave(e, button2, button_color))

    # Etiqueta para "Mensajes del Escritor del SpreadSheet"
    writer_title = tk.Label(
        root, text="Mensajes del escritor", font=('Arial', 12, 'bold'), bg=label_color, fg=text_color)
    writer_title.pack(pady=(10, 0))

    # Cuadro de texto para "Mensajes del Escritor del SpreadSheet"
    message_text3 = tk.Text(root, height=10, width=70,
                            bg=text_box_bg, fg=text_color)
    message_text3.pack(pady=20)
    message_text3.config(state=tk.DISABLED)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    login_pool = None
    root.mainloop()
