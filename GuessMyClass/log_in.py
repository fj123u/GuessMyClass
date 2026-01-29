
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import sys, os
import customtkinter as ctk
from tkinter import messagebox

# Fonction pour faire le .exe
# Met le bon chemin de fichier
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Fonction pour afficher la fenêtre de connexion
def log_in_display():
    dest = None

    # Fonction pour check si le pseudo est bon ou pas
    def validate_pseudo():
        nonlocal dest
        pseudo = username.get().strip()

        if len(pseudo) < 3:
            messagebox.showwarning(
                "Pseudo invalide",
                "Le pseudo doit contenir au moins 3 caractères"
            )
            return

        profile_path = resource_path("GuessMyClass/profile/compte.txt")
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)

        with open(profile_path, "w", encoding="utf-8") as f:
            f.write(pseudo)

        frame.destroy()
        dest = "home"

    frame = ctk.CTk()
    frame.geometry("220x140")
    frame.title("GuessMyClass")
    frame.resizable(False, False)

    frame.configure(fg_color="#CDE4E2")

    username = ctk.CTkEntry(frame, placeholder_text="Entre ton pseudo : ", width=170)
    username.place(x=25, y=30)

    try:
        with open(resource_path("GuessMyClass/profile/compte.txt"), "r", encoding="utf-8") as f:
            pseudo = f.read().strip()
            if pseudo:
                username.insert(0, pseudo)
    except FileNotFoundError:
        pass

    button = ctk.CTkButton(frame, text="Valider", command=validate_pseudo, fg_color="#FF9100", hover_color="#C35500", width=170)
    button.place(x=25, y=80)

    frame.mainloop()
    return dest
