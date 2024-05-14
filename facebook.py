import wget 
import re
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import uuid

home = os.path.expanduser("~")
ruta_guardado = os.path.join(home, "Descargas")

def generar_uuid():
    """Genera un UUID (identificador único universal) versión 4."""
    return str(uuid.uuid4())

def obtener_contenido_pagina(url):
    """Obtiene el contenido de una página web dinámica utilizando Selenium en modo headless."""
    try:
        # Configurar las opciones del navegador para ejecutar en modo headless
        opciones = Options()
        opciones.add_argument('--headless')
        opciones.add_argument('--disable-gpu')
        opciones.add_argument('--disable-dev-shm-usage')

        # Configurar el controlador de Selenium con las opciones
        driver = webdriver.Chrome(options=opciones)

        # Hacer una solicitud a la URL
        driver.get(url)

        # Esperar un tiempo para que la página se cargue completamente (ajusta esto según la velocidad de carga de la página)
        time.sleep(3)

        # Obtener el contenido de la página después de que se ha cargado completamente
        pagina_compilada = driver.page_source

        return pagina_compilada

    except Exception as e:
        print(f"Error al obtener el contenido de la página: {e}")
    finally:
        # Cerrar el navegador
        driver.quit()


def escribir_en_archivo(contenido, nombre_archivo):
    """
    Escribe el contenido proporcionado en un archivo.

    Parameters:
    - contenido (str): El contenido que se escribirá en el archivo.
    - nombre_archivo (str): El nombre del archivo en el que se escribirá el contenido.

    Returns:
    None

    Raises:
    - Exception: Se lanza una excepción en caso de error durante la escritura en el archivo.

    Example:
    >>> escribir_en_archivo("Hola, mundo!", "saludo.txt")
    Contenido ha sido escrito en el archivo 'saludo.txt'.
    """

    try:
        # Abrir el archivo en modo escritura
        with open(nombre_archivo, "w") as archivo:
            # Escribir el contenido en el archivo
            archivo.write(contenido)
        print(f"Contenido ha sido escrito en el archivo '{nombre_archivo}'.")
    except Exception as e:
        # Manejar errores durante la escritura en el archivo
        print(f"Error al escribir en el archivo '{nombre_archivo}': {e}")



def obtener_primer_grupo_captura(patrones, cadena):
    # Utiliza re.search para buscar la primera coincidencia
    coincidencia = re.search(patrones, cadena)

    # Verifica si hay coincidencia
    if coincidencia:
        # Devuelve el primer grupo de captura
        return coincidencia.group(1).replace("\/", "/")
    else:
        # Si no hay coincidencia, devuelve None
        return None

def descargar_facebook(url):
    try:
        data = obtener_contenido_pagina(url)
        sd_url = obtener_primer_grupo_captura('sd_url":"(.+?)"', data)
        hd_url = obtener_primer_grupo_captura('hd_url":"(.+?)"', data)
        
        ruta_completa = os.path.join(ruta_guardado , f"video_{generar_uuid()}.mp4")
        print("Descargando...")
   
        if hd_url is not None:
            print("sd: "+sd_url)
            wget.download(sd_url, ruta_completa)
        else:
            print("hd: "+hd_url)
            wget.download(hd_url, ruta_completa)
     
        print("Descarga completada.")
        return "Descarga completada.", ruta_completa
    
    except Exception as e:
        print(f"Error al descargar: {url}, {e}")
        return f"Error al descargar: {e}", None
