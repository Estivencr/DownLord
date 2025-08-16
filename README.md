# 🎵 Music Downloader Limpio

Este script en Python descarga música en **alta calidad** desde YouTube u otras plataformas soportadas por [`yt-dlp`](https://github.com/yt-dlp/yt-dlp), limpia los títulos de palabras innecesarias y convierte el audio al formato que elijas usando FFmpeg.

---

## ✨ Características
- Descarga el **mejor audio disponible** (`bestaudio/best`).
- Limpia el título de etiquetas como `(Audio)`, `(Official Video)`, `(Lyrics)`, etc.
- Conversión automática a formatos como MP3, FLAC o WAV.
- Configuración sencilla desde `config.py`.

---

## 📦 Requisitos
- Python 3.8 o superior.
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/download.html) instalado y en el PATH.

Instalar dependencias desde `requirements.txt`:
```bash
pip install -r requirements.txt