
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import pygame
from shape_creator import *
from log_in import *
import sys, os

# Fonction pour faire le .exe
# Met le bon chemin de fichier
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# Recupère le chemin du score
def get_score_options_path():
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    full_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "score", "options.txt")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path


title = Shape(None, 'Bienvenue sur GMC !',     (current_w/4-6)*2+958, current_h/6, (current_w/250, 8), 0, (104, 180, 229), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 150))
choix = Shape(None, 'Que voulez-vous faire ?', (current_w/4-6)*2+200, current_h/6, (current_w/5, 400), 0, (144, 180, 229), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 100))
log_in = Shape('home', 'Se connecter',    ((current_w/4-6)*2+58)/1.8, current_h/8, (current_w/5, 600), 2, (184, 180, 229), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 70))
sign_in = Shape('home', 'Créer un compte', ((current_w/4-6)*2+58)/1.8, current_h/8, (current_w/1.97, 600), 2, (184, 180, 229), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 70))
sans_compte = Shape("home", 'Jouer sans compte', (current_w/4-6)*1, current_h/12, (current_w/2.67, 755), 0, (193, 214, 213), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 50))
mdp = Shape("home", 'Votre mot de passe est :', (current_w/4-6)*1, current_h/12, (current_w/2.67, 755), 0, (193, 214, 213), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 50))


# Boucle principale du jeu
def welcome_display(): 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if log_in.top_rect.collidepoint(event.pos):
                dest = log_in_display()
                if dest:
                    return dest
                
    choix.draw()
    title.draw()
    sign_in.draw()
    log_in.draw()
    dest = sans_compte.draw()
    if dest is not None:
        with open(resource_path("GuessMyClass/profile/compte.txt"), "w") as f:
            f.write("Invite\ninvit")
            f.close()
        return dest
