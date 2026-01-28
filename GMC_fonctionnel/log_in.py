import sys, os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_score_options_path():
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    full_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "score", "options.txt")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path

# Importation des modules nécessaires
import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from pathlib import Path
from sql_link import *

# Variable globale pour gérer l'affichage des mots de passe
masquer = True

def log_in_display():
    global dest
    dest = None

    def print_input():
        global dest
        inp1 = username.get()
        inp2 = password.get()

        cnx = connect()
        result = get_account_password(cnx, inp1)
        cnx.close()

        if result == "None":
            print('Connection failed')
            messagebox.showwarning("Avertissement", "Mauvais mot de passe ou mauvais nom d'utilisateur")
        elif result == inp2:
            print('Connection success')
            with open(resource_path("profile/compte.txt"), "w") as f:
                f.write(f"{inp1}\n{inp2}")
            frame.destroy()
            dest = "home"
        else:
            print('Connection failed')
            messagebox.showwarning("Avertissement", "Mauvais mot de passe ou mauvais nom d'utilisateur")

    def toggle_password():
        global masquer
        if masquer:
            password.configure(show="")
            button.configure(text="°ᵜ°")
        else:
            password.configure(show="*")
            button.configure(text="˃ᴗ˂")
        masquer = not masquer

    frame = ctk.CTk()
    frame.geometry("200x155")
    frame.configure(fg_color='#CDE4E2')
    frame.title('GMC')

    username = ctk.CTkEntry(frame, placeholder_text="Nom d'utilisateur")
    username.place(x=25, y=25)
    try:
        with open(resource_path("profile/compte.txt"), "r") as f:
            testread = f.readlines()
            if testread:
                username.insert(0, testread[0].strip())
    except FileNotFoundError:
        pass

    password = ctk.CTkEntry(frame, placeholder_text="Mot de passe", show="*")
    password.place(x=25, y=65)
    try:
        with open(resource_path("profile/compte.txt"), "r") as f:
            testread = f.readlines()
            if len(testread) > 1:
                password.insert(0, testread[1].strip())
    except FileNotFoundError:
        pass

    button = ctk.CTkButton(frame, command=toggle_password, width=1, text="˃ᴗ˂", text_color="black", fg_color="transparent", hover_color="#CDE4E2")
    button.place(x=165, y=65)

    button2 = ctk.CTkButton(frame, text="Valider", command=print_input, fg_color="#FF9100", hover_color="#C35500")
    button2.place(x=25, y=105)

    frame.mainloop()
    return dest
