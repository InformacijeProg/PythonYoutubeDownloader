import tkinter
import customtkinter # type: ignore
from pytube import YouTube #type: ignore


def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink)
        video = ytObject.streams.get_highest_resolution()
        video.download()
    except Exception as e:
        print(f"Error downloading video\n{e}")
    

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame

app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")

# adding UI elementsdef startDownload():
    # Assuming 'video' is an object from a library like pytube that has the necessary methods
    #video = get_video_from_url(url_var.get())
    #resolutions = video.streams.filter(progressive=True, file_extension='mp4')
    
    #resolution_dict = {}
    #for stream in resolutions:
    #    resolution_dict[stream.resolution] = round(stream.filesize / (1024 * 1024), 2)  # Convert bytes to megabytes and round to 2 decimal places
    
    # Now resolution_dict contains resolutions as keys and sizes in MB as values
    #print(resolution_dict)

title = customtkinter.CTkLabel(app, text="Youtube video URL")
title.pack(padx=10, pady=10)

#Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable= url_var )
link.pack()
# Download Button
download = customtkinter.CTkButton(app, text="Download",command=startDownload)
download.pack(padx=10, pady=10)
# Run app
app.mainloop()