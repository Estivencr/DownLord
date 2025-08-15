"""
Descargador de música en alta calidad desde YouTube u otras fuentes compatibles.
Autor: Estiven Cano
Fecha: 2025-08-11
"""

import yt_dlp
import os
import re
from config import OUTPUT_PATH, AUDIO_FORMAT, AUDIO_QUALITY

OUTPUT_PATH = "downloads"

# Lista de patrones a eliminar del título
PATTERNS_REMOVE = [
    r"\(Audio\)",
    r"\(Official Music Video\)",
    r"\(Official Video\)",
    r"\(Video Oficial\)",
    r"\(Lyrics\)",
    r"\(Lyric Video\)"
]

def clean_title(title: str) -> str:
    """
    Limpia el título eliminando palabras o frases no deseadas.
    """
    for pattern in PATTERNS_REMOVE:
        title = re.sub(pattern, "", title, flags=re.IGNORECASE).strip()
    # Elimina espacios dobles si quedaron
    title = re.sub(r"\s{2,}", " ", title)
    return title

def hook(d):
    """
    Hook que se ejecuta en cada etapa de descarga.
    """
    if d['status'] == 'finished':
        print(f"✅ Descarga completa: {d['filename']}")

def download_audio_clean(url: str):
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    def sanitize(info):
        """Modifica el título antes de guardar."""
        info['title'] = clean_title(info['title'])
        return info


    ydl_opts = {
        "format": "bestaudio/best",  # Mejor calidad de audio disponible
        "outtmpl": os.path.join(OUTPUT_PATH, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": AUDIO_FORMAT,
                "preferredquality": AUDIO_QUALITY,
            }
        ],
        "quiet": False,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"📥 Descargando música desde: {url}")
        ydl.download([url])
        print("✅ Descarga completada.")

if __name__ == "__main__":
    enlace = input("Ingresa el enlace de la canción o playlist: ")
    download_audio_clean(enlace)