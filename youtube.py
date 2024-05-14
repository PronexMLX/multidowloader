
from pytube import YouTube
import os
import uuid

home = os.path.expanduser("~")
ruta_guardado = os.path.join(home, "Descargas")

def generar_uuid():
    """Genera un UUID (identificador único universal) versión 4."""
    return str(uuid.uuid4())

def descargar_youtube(url):
    try:
        # Crear un objeto YouTube
        video = YouTube(url)

        # Nombre del video
        name = f"video_{generar_uuid()}.mp4"

        # Obtener la mejor resolución disponible
        stream = video.streams.get_highest_resolution()

        # Imprimir información sobre el video
        msg = f"""Descargando: {video.title}\nResolución: {stream.resolution}\nFormato: {stream.mime_type}"""
        print(msg)
        ruta_completa = os.path.join(ruta_guardado , name)

        # Descargar el video
        stream.download(filename=name, output_path=ruta_guardado)
        print("Ruta del video: " + ruta_completa)
        print("Descarga completada.")
        return msg, ruta_completa

    except Exception as e:
        print(f"Error al descargar el video: {url}, {e}")
        return f"Error al descargar el video: {e}", None
