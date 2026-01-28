
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


# Importation des modules n�cessaires
import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from pathlib import Path
from sql_link import *

# Variable globale pour g�rer l'affichage des mots de passe
masquer = True

def sign_in_display():

    global dest
    dest = None
    
    # Fonction pour traiter les entr�es utilisateur
    def print_input():
        global dest
        # R�cup�ration des valeurs des champs d'entr�e
        inp1 = username.get()

        # V�rification si le nom d'utilisateur existe d�ja� dans la base de donn�es
        cnx = connect()

        result = check_pseudo(cnx, inp1)

        # Si le nom d'utilisateur existe d�ja�, afficher un avertissement
        if result == True:
            messagebox.showwarning("Avertissement", "Le nom d'utilisateur est deja pris")
        # Si les mots de passe ne correspondent pas, afficher un avertissement
        else:
            # Si tout est correct, ins�rer les informations dans la base de donn�es

            password = add_account(cnx, inp1)
            full_path = resource_path("profile/compte.txt")

            with open(full_path, "w") as f:
                f.write(f"{inp1}\n{password}")
                f.close()
            messagebox.showinfo("Mot de passe généré", f"Votre mot de passe est : {password} Merci de bien le garder, il vous sera utile pour vous reconnecter")
            # Fermer la fen�tre apr�s l'inscription r�ussie
            frame.destroy() 
            dest = "home"          
            

        cnx.close()


    # Cr�ation de la fen�tre principale
    frame = ctk.CTk()
    frame.geometry("200x195")
    frame.configure(fg_color='#CDE4E2')
    frame.title('GMC')

    # Cr�ation des champs d'entr�e pour le nom d'utilisateur et les mots de passe
    username = ctk.CTkEntry(frame, placeholder_text="Nom d'utilisateur")
    username.place(x=25, y=25)

    # Cr�ation du bouton pour valider les entr�es
    button2 = ctk.CTkButton(frame, text="Valider", command=print_input, fg_color="#FF9100", hover_color="#C35500")
    button2.place(x=25, y=145)

    # Lancement de la boucle principale de l'interface graphique
    frame.mainloop()
    return dest

