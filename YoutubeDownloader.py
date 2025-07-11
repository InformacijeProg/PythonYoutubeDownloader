import os
import sys
import tkinter
from tkinter import ttk, filedialog
import customtkinter  # type: ignore
import threading
import yt_dlp  # type: ignore
from PIL import Image, ImageTk  
import urllib.request
import io

video_url = ""
downloaded_file_path = None
video_heights: list[str] = []
selected_heights: list[int] = []
video_title = ""
thumbnail_url = ""
thumbnail_image = None

# ─────────────────────────────
def fetch_resolutions():
    global selected_heights, video_title, thumbnail_url, thumbnail_image

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get("formats", [])
            video_title = info.get("title", "video")
            thumbnail_url = info.get("thumbnail", "")

            resolutions = sorted(set(
                fmt.get("height") for fmt in formats if fmt.get("vcodec") != "none"
            ), reverse=True)

            video_heights.clear()
            selected_heights.clear()
            for h in resolutions:
                if h:
                    label = f"{h}p"
                    video_heights.append(label)
                    selected_heights.append(h)

            combo['values'] = video_heights
            if video_heights:
                combo.current(0)
                resolution_count_label.configure(text=f"{len(video_heights)} resolutions")
            else:
                resolution_count_label.configure(text="No formats")

            title_label.configure(text=f"Title: {video_title}")
            load_thumbnail(thumbnail_url)

    except Exception as e:
        resolution_count_label.configure(text="Error")
        title_label.configure(text="Title: Error")
        status_label.configure(text=f"Fetch error: {e}")

# ─────────────────────────────
def load_thumbnail(url):
    global thumbnail_image
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            img = Image.open(io.BytesIO(data))
            img = img.resize((320, 180), Image.LANCZOS)
            thumbnail_image = ImageTk.PhotoImage(img)
            thumbnail_label.configure(image=thumbnail_image)
    except Exception as e:
        thumbnail_label.configure(image="")
        print("Thumbnail load failed:", e)

# ─────────────────────────────
def start_fetch_thread():
    global video_url
    video_url = link.get().strip()
    if not video_url.startswith("http"):
        status_label.configure(text="Invalid URL.")
        return
    resolution_count_label.configure(text="Loading...")
    threading.Thread(target=fetch_resolutions, daemon=True).start()

# ─────────────────────────────
def download_video():
    global downloaded_file_path
    try:
        sel_index = combo.current()
        if sel_index < 0:
            status_label.configure(text="No resolution selected.")
            return

        height = selected_heights[sel_index]
        format_string = f"bestvideo[height={height}]+bestaudio/best"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            initialfile=f"{video_title}_{height}p.mp4",
            filetypes=[("MP4 files", "*.mp4")]
        )
        if not file_path:
            status_label.configure(text="Download cancelled.")
            return

        BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        FFMPEG_PATH = os.path.join(BASE_DIR, "bin", "ffmpeg.exe")

        ydl_opts = {
            'quiet': False,
            'format': format_string,
            'outtmpl': file_path,
            'merge_output_format': 'mp4',
            'ffmpeg_location': FFMPEG_PATH,
            'noplaylist': True,
            'progress_hooks': [progress_hook],
        }

        progress_var.set(0)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        downloaded_file_path = file_path
        status_label.configure(text="Download complete.")
        delete_button.configure(state=tkinter.NORMAL)

    except Exception as e:
        status_label.configure(text=f"Download error: {e}")
        print(e)

# ─────────────────────────────
def start_download_thread():
    delete_button.configure(state=tkinter.DISABLED)
    threading.Thread(target=download_video, daemon=True).start()

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded = d.get('downloaded_bytes', 0)
        percent = (downloaded / total) * 100 if total > 0 else 0
        progress_var.set(percent)
        progress_bar.update_idletasks()

def deleteFile():
    global downloaded_file_path
    if downloaded_file_path and os.path.exists(downloaded_file_path):
        try:
            os.remove(downloaded_file_path)
            status_label.configure(text="File deleted.")
            delete_button.configure(state=tkinter.DISABLED)
            downloaded_file_path = None
        except Exception as e:
            status_label.configure(text="Delete error.")
            print(e)

# ─────────────────────────────
# GUI SETUP
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1000x600")
app.title("YouTube Downloader - Portable (yt-dlp + ffmpeg)")

title = customtkinter.CTkLabel(app, text="YouTube video URL")
title.pack(pady=(10, 2))

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=700, height=40, textvariable=url_var)
link.pack()

url_button = customtkinter.CTkButton(app, text="Fetch Resolutions", command=start_fetch_thread)
url_button.pack(pady=(5, 10))

combo_frame = customtkinter.CTkFrame(app)
combo_frame.pack()

combo = ttk.Combobox(combo_frame, width=50)
combo.pack(side=tkinter.LEFT, padx=5)

resolution_count_label = customtkinter.CTkLabel(combo_frame, text="")
resolution_count_label.pack(side=tkinter.LEFT, padx=10)

button_frame = customtkinter.CTkFrame(app)
button_frame.pack(pady=(5, 5))

delete_button = customtkinter.CTkButton(button_frame, text="Delete File", command=deleteFile, state=tkinter.DISABLED)
delete_button.pack(side=tkinter.LEFT, padx=20)

download = customtkinter.CTkButton(button_frame, text="Download Video", command=start_download_thread)
download.pack(side=tkinter.LEFT, padx=20)

progress_frame = customtkinter.CTkFrame(app)
progress_frame.pack(pady=10)

progress_var = tkinter.DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100, length=800, mode='determinate')
progress_bar.pack()

status_label = customtkinter.CTkLabel(app, text="")
status_label.pack(pady=5)

title_label = customtkinter.CTkLabel(app, text="Title: ")
title_label.pack(pady=5)

thumbnail_label = tkinter.Label(app)
thumbnail_label.pack(pady=10)

app.mainloop()
