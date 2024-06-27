import os
import tkinter
import customtkinter  # type: ignore
from pytube import YouTube  # type: ignore
from tkinter import ttk
import threading

stre: list[str] = []
downloading = False
current_stream = None

def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink)

        # Filtering streams for progressive (video + audio) streams
        streams = ytObject.streams.filter(progressive=True, file_extension='mp4')
        print(f"Total streams found: {len(streams)}")  # Debugging statement
        stre.clear()
        
        # Debug: List all available streams
        seen_resolutions = set()
        for stream in ytObject.streams:
            resolution = stream.resolution
            if resolution and resolution not in seen_resolutions:
                size_in_mb = round(stream.filesize / (1024 * 1024), 2)  # Convert to MB and round to 2 decimal places
                stre.append(f"{resolution} {size_in_mb}Mb")
                seen_resolutions.add(resolution)

        print(f"Unique resolutions found: {seen_resolutions}")  # Debugging statement

        # Sort the list by resolution
        stre.sort(key=lambda x: int(x.split('p')[0]))

        # Populate combo box
        combo['values'] = stre
        if stre:
            combo.current(0)

    except Exception as e:
        print(f"Error retrieving video streams\n{e}")

def stopDownload():
    global downloading
    downloading = False
    if current_stream:
        print("Stopping download...")
        try:
            os.remove(current_stream.default_filename)
        except Exception as e:
            print(f"Error deleting file: {e}")

def downloadVideo():
    global downloading, current_stream
    downloading = True
    try:
        progress_var.set(0)  # Initialize progress bar to 0
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=progressFunction)

        selected_item = combo.get()
        selected_resolution = selected_item.split(' ')[0]
        print(f"Selected resolution: {selected_resolution}")  # Debugging statement
        stream = ytObject.streams.filter(res=str(selected_resolution), file_extension='mp4').first()
        current_stream = stream

        if stream:
            stream.download()
            print("Download completed!")
            status_label.configure(text="VIDEO DOWNLOADED")
        elif downloading == False:
            status_label.configure(text="Download stopped by user")
        else: 
            print("Selected resolution not available.")
    except Exception as e:
        print(f"Error downloading video\n{e}")
        status_label.configure(text="Error during download")

def progressFunction(stream, chunk, bytes_remaining):
    global downloading
    if not downloading:
        status_label.configure(text="Download stopped by user")
        progress_var.set(0)
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_var.set(percentage)
    progress_bar.update()

def startDownloadThread():
    threading.Thread(target=downloadVideo).start()

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

title = customtkinter.CTkLabel(app, text="YouTube video URL")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Bind the change event to the link input
def on_link_change(*args):
    startDownload()

url_var.trace_add('write', on_link_change)

# Create a style for the combo box
style = ttk.Style()
style.configure("TCombobox", font=("Helvetica", 12, "bold"))

# Combo box
combo = ttk.Combobox(app, width=40, style="TCombobox")
combo.pack(pady=10)

# Button frame
button_frame = customtkinter.CTkFrame(app)
button_frame.pack(pady=10)

# Stop Button
stop_button = customtkinter.CTkButton(button_frame, text="Stop", command=stopDownload)
stop_button.pack(side=tkinter.LEFT, padx=5)

# Download Button
download = customtkinter.CTkButton(button_frame, text="Download", command=startDownloadThread)
download.pack(side=tkinter.LEFT, padx=5)

# Progress Bar
progress_var = tkinter.DoubleVar()
progress_bar = ttk.Progressbar(app, variable=progress_var, maximum=100, length=350, mode='determinate')
progress_bar.pack(pady=10)

# Status Label
status_label = customtkinter.CTkLabel(app, text="")
status_label.pack(pady=10)

style.configure("TProgressbar", troughcolor='white', background='blue')

# Run app
app.mainloop()
