import sys, os
import pygame
from utils import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Bouton retour
leave_button_multi = Shape('home', '<', 50, 50, (10, 10), 2, (200, 0, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))

# ✅ Titre centré dynamiquement
# Calcul de la largeur du texte pour centrer
font_temp = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 80)
title_text_surf = font_temp.render("Mode Multijoueur", True, (255, 255, 255))
title_width = title_text_surf.get_width()
title_x = (current_w - title_width) / 2

title_multi = Shape(None, 'Mode Multijoueur', title_width, 100, (title_x, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 80))

# Boutons
button_create = Shape('create_room_screen', 'Créer une partie', 470, 100, (current_w/2 - 235, current_h/2 - 80), 5, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 50))
button_join = Shape('join_room_screen', 'Rejoindre une partie', 470, 100, (current_w/2 - 235, current_h/2 + 60), 5, (169, 148, 223), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 50))

def multiplayer_menu_display():
    screen = pygame.display.get_surface()
    
    # Fond
    screen.fill((205, 228, 226))
    
    # Bouton retour
    dest = leave_button_multi.draw()
    if dest:
        return dest
    
    # Titre
    title_multi.draw()
    
    # Boutons
    dest = button_create.draw()
    if dest:
        return dest
    
    dest = button_join.draw()
    if dest:
        return dest
    
    return "multiplayer_menu"