"""
Descargador de música en alta calidad desde YouTube u otras fuentes compatibles.
Autor: Estiven Cano
Fecha: 2025-08-11
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import yt_dlp
import os
import re

# Ajustes generales
OUTPUT_PATH = "downloads"
AUDIO_FORMAT = "mp3"
AUDIO_QUALITY = "192"

# Patrones para limpiar títulos
PATTERNS_REMOVE = [
    r"\(Audio\)",
    r"\(Official Music Video\)",
    r"\(Official Video\)",
    r"\(Video Oficial\)",
    r"\(Lyrics\)",
    r"\(Lyric Video\)"
]

def clean_title(title: str) -> str:
    for pattern in PATTERNS_REMOVE:
        title = re.sub(pattern, "", title, flags=re.IGNORECASE).strip()
    return re.sub(r"\s{2,}", " ", title)

def download_audio_clean(url: str, progress_callback=None):
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    def hook(d):
        if d['status'] == 'downloading' and progress_callback:
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percent = int(downloaded / total * 100)
                progress_callback(percent)
        elif d['status'] == 'finished' and progress_callback:
            progress_callback(100)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(OUTPUT_PATH, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": AUDIO_FORMAT,
            "preferredquality": AUDIO_QUALITY,
        }],
        "progress_hooks": [hook],
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# ---------------- GUI ----------------
def start_download():
    url = entry_url.get()
    if not url:
        messagebox.showwarning("Error", "Por favor ingresa un enlace")
        return

    progress_bar['value'] = 0
    lbl_status.config(text="Descargando...")

    def task():
        try:
            download_audio_clean(url, progress_callback=update_progress)
            lbl_status.config(text="✅ Descarga completada")
            messagebox.showinfo("Éxito", "La descarga ha finalizado.")
        except Exception as e:
            lbl_status.config(text="❌ Error en la descarga")
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")

    threading.Thread(target=task).start()

def update_progress(value):
    progress_bar['value'] = value
    root.update_idletasks()

# Crear ventana principal
root = tk.Tk()
root.title("Music Downloader 🎵")
root.geometry("500x200")

# Widgets
label = tk.Label(root, text="Ingresa el enlace de la canción o playlist:")
label.pack(pady=10)

entry_url = tk.Entry(root, width=60)
entry_url.pack(pady=5)

btn_download = tk.Button(root, text="Descargar", command=start_download)
btn_download.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=400, mode="determinate")
progress_bar.pack(pady=5)

lbl_status = tk.Label(root, text="")
lbl_status.pack(pady=5)

root.mainloop()