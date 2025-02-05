# 📊 Automatización de Facturación para Estudio Contable

Este proyecto desarrollado en Python automatiza el proceso de obtención de credenciales, inicio de sesión y descarga de archivos necesarios para calcular la facturación mensual de clientes de un estudio contable. Utiliza Google Spreadsheet API para gestionar credenciales, Selenium para la automatización del login y descarga de archivos, y multiprocessing para procesar múltiples clientes en simultáneo.

## 🚀 Características
- 📄 **Integración con Google Spreadsheet**: Obtiene credenciales de clientes de un documento de Google Sheets.
- 🌐 **Automatización con Selenium**: Accede a la web correspondiente, inicia sesión y descarga los archivos necesarios.
- ⚡ **Ejecución concurrente con Multiprocessing**: Maneja el login y descarga de archivos para más de 70 clientes de manera paralela, optimizando tiempos.
- 🔔 **Manejo de Errores y Notificaciones**: Detecta y reporta errores como captcha, cambio de contraseña o fallos de conexión.
- 📊 **Cálculo de Facturación**: Procesa los archivos descargados y almacena la facturación mensual en un Spreadsheet junto al CUIT de cada cliente.

## 🛠️ Tecnologías Utilizadas
- Python 🐍
- Selenium 🌐
- Google Spreadsheet API 📊
- Multiprocessing ⚡
- Pandas 📝

## 📦 Instalación y Configuración
1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```
2. **Crear y activar un entorno virtual (opcional pero recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. **Cambiar manualmente en los archivos correspondientes a que Spreadsheet acceder y de cuales tomar datos**
   ```
    Para mas ayuda en esto se pueden contactar con nosotros.
   ```
4. **Configurar las credenciales de Google Sheets**
   - Obtener las credenciales desde [Google Cloud Console](https://console.cloud.google.com/)
   - Guardarlas en un archivo `credentials.json` dentro del proyecto

## ▶️ Uso
Ejecutar el script principal para iniciar la interfaz grafica:
```bash
python main.py
```

## ⚠️ Posibles Errores y Soluciones
| Error                     | Posible Causa                  | Solución |
|---------------------------|--------------------------------|----------|
| Google Chrome y Drivers   | Cambio de version de chrome    | Instalar la ultima version de chromedriver |

## 📄 Licencia
Este proyecto se distribuye bajo la licencia MIT. ¡Siéntete libre de contribuir! 🤝

---
✉️ **Contacto**: Para cualquier consulta o sugerencia, puedes abrir un issue o contactarme en [josefinamartinezosti@gmail.com o meloignacionicolas@gmail.com].

