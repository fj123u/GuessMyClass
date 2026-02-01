import sys, os
import customtkinter as ctk
from tkinter import messagebox
from multiplayer import join_room
from sql_link import load_local_profile

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

_join_window = None

def join_room_screen_display():
    global _join_window
    
    if _join_window is not None:
        try:
            _join_window.lift()
            _join_window.focus_force()
            return None
        except:
            _join_window = None
    
    result = None
    
    def validate_code():
        nonlocal result
        code = room_code_entry.get().strip().upper()
        
        if len(code) != 6:
            messagebox.showwarning("Code invalide", "Le code doit contenir 6 caractères")
            return
        
        pseudo = load_local_profile()
        room = join_room(code, pseudo)
        
        if room:
            result = ('waiting_room', code, False)
            close_window()
        else:
            messagebox.showerror("Erreur", "Partie introuvable ou déjà commencée")
    
    def close_window():
        global _join_window
        _join_window = None
        frame.quit()
        frame.destroy()
    
    frame = ctk.CTk()
    _join_window = frame
    frame.geometry("300x180")
    frame.title("Rejoindre une partie")
    frame.resizable(False, False)
    frame.configure(fg_color="#CDE4E2")
    frame.protocol("WM_DELETE_WINDOW", close_window)
    
    label = ctk.CTkLabel(frame, text="Code de la partie :", font=("Arial", 16))
    label.place(x=80, y=30)
    
    room_code_entry = ctk.CTkEntry(frame, placeholder_text="ABC123", width=200, font=("Arial", 18))
    room_code_entry.place(x=50, y=70)
    
    button = ctk.CTkButton(frame, text="Rejoindre", command=validate_code, fg_color="#FF9100", hover_color="#C35500", width=200, font=("Arial", 16))
    button.place(x=50, y=120)
    
    room_code_entry.bind("<Return>", lambda e: validate_code())
    room_code_entry.focus()
    
    frame.mainloop()
    
    if result:
        return result
    return "multiplayer_menu"