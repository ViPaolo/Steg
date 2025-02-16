import tkinter
import tkinter.messagebox
import customtkinter
import os
from src.steg import *
from customtkinter import filedialog




#Basi start for customtkinter, set the appearance mode 
customtkinter.set_appearance_mode("System") # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue") # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()

app.title("Stenography Tool")

app.geometry("700x800")

def askdirectory():
    print("button pressed")
    filedialog.askdirectory(title="Select a folder")

label = customtkinter.CTkLabel(master=app, text="Ciao!", font=("Helveticaca", 20), text_color="#FFFF90")
label.place(relx = 0.5, rely= 0.2, anchor = customtkinter.CENTER)



btn = customtkinter.CTkButton(master=app, text="Ciao! Cliccami per aprire una cartella", command=askdirectory)
btn.place(relx = 0.5, rely = 0.3, anchor = customtkinter.CENTER)


app.mainloop()


