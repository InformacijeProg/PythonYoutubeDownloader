import os
import tkinter
import customtkinter  # type: ignore
from pytube import YouTube  # type: ignore
from tkinter import ttk, scrolledtext
import threading
from youtube_transcript_api import YouTubeTranscriptApi # type: ignore

stre: list[str] = []
downloading = False
current_stream = None
download_thread = None
downloaded_file_path = None
transcription_text = ''
transcript_file_path = None

def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink)

        # Filtering streams for progressive (video + audio) streams
        streams = ytObject.streams.filter(progressive=True, file_extension='mp4')
        stre.clear()

        # List all available streams
        seen_resolutions = set()
        for stream in ytObject.streams:
            resolution = stream.resolution
            if resolution and resolution not in seen_resolutions:
                size_in_mb = round(stream.filesize / (1024 * 1024), 2)  # Convert to MB and round to 2 decimal places
                stre.append(f"{resolution} {size_in_mb}Mb")
                seen_resolutions.add(resolution)

        # Sort the list by resolution
        stre.sort(key=lambda x: int(x.split('p')[0]))

        # Populate combo box
        combo['values'] = stre
        if stre:
            combo.current(0)

    except Exception as e:
        print(f"Error retrieving video streams\n{e}")

def deleteFile():
    global downloaded_file_path
    if downloaded_file_path and os.path.exists(downloaded_file_path):
        try:
            os.remove(downloaded_file_path)
            status_label.configure(text="File deleted.")
            delete_button.configure(state=tkinter.DISABLED)
            downloaded_file_path = None
        except Exception as e:
            print(f"Error deleting file: {e}")
            status_label.configure(text="Error deleting file.")

def downloadVideo():
    global downloading, current_stream, download_thread, downloaded_file_path, transcription_text
    downloading = True
    try:
        progress_var.set(0)  # Initialize progress bar to 0
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=progressFunction)

        selected_item = combo.get()
        selected_resolution = selected_item.split(' ')[0]
        stream = ytObject.streams.filter(res=selected_resolution, file_extension='mp4').first()
        current_stream = stream

        if stream:
            downloaded_file_path = stream.default_filename
            stream.download()
            print("Download completed!")
            status_label.configure(text="VIDEO DOWNLOADED")
            delete_button.configure(state=tkinter.NORMAL)

            video_id = ytLink.split('v=')[1]
            transcription_text = get_video_transcript(video_id)
            transcript_text_box.delete('1.0', tkinter.END)
            transcript_text_box.insert(tkinter.END, transcription_text)
            save_button.configure(state=tkinter.NORMAL)
        else:
            print("Selected resolution not available.")
    except Exception as e:
        print(f"Error downloading video\n{e}")
        status_label.configure(text="Error during download")

def progressFunction(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_var.set(percentage)
    progress_bar.update()

def startDownloadThread():
    global download_thread
    delete_button.configure(state=tkinter.DISABLED)
    download_thread = threading.Thread(target=downloadVideo)
    download_thread.start()

def save_transcript():
    global transcript_file_path
    if downloaded_file_path and transcription_text:
        try:
            transcript_file_path = f"{downloaded_file_path}.txt"
            with open(transcript_file_path, 'w', encoding='utf-8') as file:
                file.write(transcription_text)
            status_label.configure(text="Transcript saved.")
            delete_transcript_button.configure(state=tkinter.NORMAL)
        except Exception as e:
            print(f"Error saving transcript: {e}")
            status_label.configure(text="Error saving transcript.")

def delete_transcript():
    global transcript_file_path
    if transcript_file_path and os.path.exists(transcript_file_path):
        try:
            os.remove(transcript_file_path)
            status_label.configure(text="Transcript file deleted.")
            delete_transcript_button.configure(state=tkinter.DISABLED)
            transcript_file_path = None
        except Exception as e:
            print(f"Error deleting transcript file: {e}")
            status_label.configure(text="Error deleting transcript file.")

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return 'Transcript not available.'

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
app.geometry("720x800")
app.title("YouTube Downloader")

title = customtkinter.CTkLabel(app, text="YouTube video URL")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=450, height=40, textvariable=url_var)
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
combo.pack(pady=20)

# Button frame
button_frame = customtkinter.CTkFrame(app, width=250, height=20)
button_frame.pack(pady=(80, 10))

# Delete Button
delete_button = customtkinter.CTkButton(button_frame, text="Delete Video", command=deleteFile, state=tkinter.DISABLED)
delete_button.pack(side=tkinter.LEFT, padx=5, pady=10)

# Download Button
download = customtkinter.CTkButton(button_frame, text="Download", command=startDownloadThread)
download.pack(side=tkinter.LEFT, padx=5, pady=10)

# Progress Bar frame
progress_frame = customtkinter.CTkFrame(app, width=350, height=20)
progress_frame.pack(pady=(10, 20))

# Progress Bar
progress_var = tkinter.DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100, length=350, mode='determinate')
progress_bar.pack(pady=5)

# Status Label
status_label = customtkinter.CTkLabel(app, text="")
status_label.pack(pady=10)

title_t = customtkinter.CTkLabel(app, text="YouTube video Transcript")
title_t.pack(pady=10)

# Transcription frame
transcription_frame = customtkinter.CTkFrame(app, width=640, height=200)
transcription_frame.pack(pady=10)

# Transcription text box
transcript_text_box = scrolledtext.ScrolledText(transcription_frame, wrap=tkinter.WORD, width=70, height=12, bg="black", fg="white")
transcript_text_box.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

# Save Button
save_button = customtkinter.CTkButton(app, text="SAVE", command=save_transcript, state=tkinter.DISABLED)
save_button.pack(pady=5)

# Delete Transcript Button
delete_transcript_button = customtkinter.CTkButton(app, text="DELETE Transcript", command=delete_transcript, state=tkinter.DISABLED)
delete_transcript_button.pack(pady=5)

style.configure("TProgressbar", troughcolor='white', background='blue')

# Run app
app.mainloop()
