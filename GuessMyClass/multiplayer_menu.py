import sys, os
import pygame
from utils import *
from connection_check import check_supabase_connection, is_online

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Bouton retour
leave_button_multi = Shape('home', '<', 50, 50, (10, 10), 2, (200, 0, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))

# ✅ Titre centré dynamiquement
font_temp = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 80)
title_text_surf = font_temp.render("Mode Multijoueur", True, (255, 255, 255))
title_width = title_text_surf.get_width()
title_x = (current_w - title_width) / 2

title_multi = Shape(None, 'Mode Multijoueur', title_width, 100, (title_x, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 80))

# Boutons
button_create = Shape('create_room_screen', 'Créer une partie', 470, 100, (current_w/2 - 235, current_h/2 - 80), 5, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 50))
button_join = Shape('join_room_screen', 'Rejoindre une partie', 470, 100, (current_w/2 - 235, current_h/2 + 60), 5, (169, 148, 223), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 50))

_connection_checked = False
_is_online = False

def multiplayer_menu_display():
    global _connection_checked, _is_online
    
    # ✅ Lance la musique de menu
    try:
        from audio_manager import audio
        audio.play_music_menu()
    except:
        pass
    
    screen = pygame.display.get_surface()
    
    # ✅ Vérifie la connexion au premier affichage
    if not _connection_checked:
        print("🔍 Vérification de la connexion Supabase...")
        _is_online = check_supabase_connection()
        _connection_checked = True
    
    # Fond
    screen.fill((205, 228, 226))
    
    # Bouton retour
    dest = leave_button_multi.draw()
    if dest:
        _connection_checked = False  # Reset pour la prochaine fois
        return dest
    
    # Titre
    title_multi.draw()
    
    # ✅ Message d'avertissement si hors ligne
    if not _is_online:
        font_warning = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 30)
        warning_text = font_warning.render("⚠️ Mode multijoueur indisponible", True, (255, 0, 0))
        warning_bg = pygame.Rect(
            current_w/2 - warning_text.get_width()/2 - 20,
            current_h/2 - 200,
            warning_text.get_width() + 40,
            warning_text.get_height() + 20
        )
        pygame.draw.rect(screen, (255, 200, 200), warning_bg, border_radius=10)
        screen.blit(warning_text, (current_w/2 - warning_text.get_width()/2, current_h/2 - 190))
        
        font_small = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 20)
        info_text = font_small.render("(Vérifiez votre connexion Internet ou pare-feu)", True, (100, 100, 100))
        screen.blit(info_text, (current_w/2 - info_text.get_width()/2, current_h/2 - 150))
        
        # Boutons grisés et désactivés
        grey_color = (150, 150, 150)
        pygame.draw.rect(screen, grey_color, (current_w/2 - 235, current_h/2 - 80, 470, 100), border_radius=15)
        pygame.draw.rect(screen, grey_color, (current_w/2 - 235, current_h/2 + 60, 470, 100), border_radius=15)
        
        font_button = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 50)
        create_text = font_button.render("Créer une partie", True, (200, 200, 200))
        join_text = font_button.render("Rejoindre une partie", True, (200, 200, 200))
        
        screen.blit(create_text, (current_w/2 - create_text.get_width()/2, current_h/2 - 55))
        screen.blit(join_text, (current_w/2 - join_text.get_width()/2, current_h/2 + 85))
        
        return "multiplayer_menu"
    
    # ✅ Mode en ligne : boutons actifs
    dest = button_create.draw()
    if dest:
        return dest
    
    dest = button_join.draw()
    if dest:
        return dest
    
    return "multiplayer_menu"