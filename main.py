import tkinter
import customtkinter # type: ignore
from pytube import YouTube #type: ignore


def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink)

# System settings

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame

app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")

# adding UI elements
title = customtkinter.CTkLabel(app, "Youtube video URL")
title.pack(padx=10, pady=10)

#Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable= url_var )
link.pack()
# Download Button
download = customtkinter.CTkButton(app, text="Download",command=startDownload)

# Run app
app.mainloop()