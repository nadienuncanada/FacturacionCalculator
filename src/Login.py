from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


def login(credencial, path_to_chromedriver, download_path, selected_option_facturacion):
    user, password_txt = credencial
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Crea el servicio de ChromeDriver y el WebDriver dentro del proceso
    service = Service(executable_path=path_to_chromedriver)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 3)

    try:
        # Abrir la página de login
        driver.get("https://auth.afip.gob.ar/contribuyente_/login.xhtml")

        # Ingresar usuario
        cuil = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[name="F1:username"]')))
        cuil.clear()
        cuil.send_keys(user)

        # Hacer click en siguiente
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[name="F1:btnSiguiente"]'))).click()
        try:
            mensaje_error = wait.until(
                EC.presence_of_element_located((By.ID, "F1:msg")))
            if "Número de CUIL/CUIT incorrecto" in mensaje_error.text:
                return f"❌ La cuil/cuit para el usuario {user} no es válida."
        except:
            pass  # Continuar si no aparece el mensaje de error

        # Ingresar contraseña
        password = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[name="F1:password"]')))
        password.clear()
        password.send_keys(password_txt)

        # Ingresar
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[name="F1:btnIngresar"]'))).click()

        # Ver si aparece mensaje de error
        try:
            mensaje_error = wait.until(
                EC.presence_of_element_located((By.ID, "F1:msg")))
            if "Clave o usuario incorrecto" in mensaje_error.text:
                return f"❌ Usuario o clave incorrectos para el usuario {user}."
        except:
            pass  # Continuar si no aparece el mensaje de error

        # Ver si aparece mensaje de error
        try:
            mensaje_error = wait.until(
                EC.presence_of_element_located((By.ID, "F1:msg")))
            if "El captcha ingresado es incorrecto." in mensaje_error.text:
                return f"❌ El usuario {user} pide captcha."
        except:
            pass  # Continuar si no aparece el mensaje de error

        # Verificar si muestra cartel de cambiar contraseña
        try:
            wait.until(EC.presence_of_element_located((By.NAME, "F1:j_idt41")))
            return f"⚠️ Usuario {user} debe cambiar la contraseña."
        except:
            # Buscar la sección "Mis Comprobantes"
            misComprobantes = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'input[id="buscadorInput"]')))
            misComprobantes.clear()
            misComprobantes.send_keys("Mis Comprobantes")

            # Hacer click en el item "Mis Comprobantes"
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//li[@aria-label='Mis Comprobantes']"))).click()

        # Comprobar si aparece el cartel emergente
        try:
            cartel = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='modal-content' and @role='document']")))
            if cartel:
                return f"❌ {user} no cuenta con la sección Mis Comprobantes."
        except:
            # Cambiar a la nueva pestaña
            wait.until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])

            try:
                # Verifica si aparece el formulario para seleccionar la empresa
                formulario_empresa = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//form[@name='seleccionaEmpresaForm']"))
                )
                if formulario_empresa:
                    return f"⚠️ El usuario {user} necesita seleccionar persona a representar. Hacer manualmente."
            except:
                pass

            # Hacer click en "Emitidos"
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//h3[text()='Emitidos']/ancestor::a"))).click()

            # Seleccionar "Mes pasado" o "Año pasado"
            wait.until(EC.element_to_be_clickable(
                (By.ID, "fechaEmision"))).click()
            if selected_option_facturacion == "Mensual":
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//li[@data-range-key='Mes Pasado']"))).click()
            elif selected_option_facturacion == "Anual":
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//li[@data-range-key='Año Pasado']"))).click()

            # Buscar los comprobantes
            wait.until(EC.element_to_be_clickable(
                (By.ID, "buscarComprobantes"))).click()

            # Exportar como CSV
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@title='Exportar como CSV']"))).click()

            # Tiempo de espera para la descarga del archivo
            time.sleep(3)

    except Exception as e:
        return f"❌ Error con el usuario {user}, verificar manualmente!"
    finally:
        driver.quit()
