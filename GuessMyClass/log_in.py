import sys, os
import customtkinter as ctk
from tkinter import messagebox

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

_log_in_window = None

def log_in_display():
    global _log_in_window
    
    if _log_in_window is not None:
        try:
            _log_in_window.lift()
            _log_in_window.focus_force()
            return None
        except:
            _log_in_window = None
    
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
        dest = "home"
        close_window()
    
    def close_window():
        global _log_in_window
        _log_in_window = None
        frame.quit()
        frame.destroy()
    
    frame = ctk.CTk()
    _log_in_window = frame
    frame.geometry("220x140")
    frame.title("GuessMyClass")
    frame.resizable(False, False)
    frame.configure(fg_color="#CDE4E2")
    frame.protocol("WM_DELETE_WINDOW", close_window)
    
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
    
    username.bind("<Return>", lambda e: validate_pseudo())
    username.focus()
    
    frame.mainloop()
    
    return dest