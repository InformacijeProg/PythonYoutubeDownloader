import tkinter
import customtkinter
from pytube import Youtube

# System settings

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame

app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")



# Run app
app.mainloop()