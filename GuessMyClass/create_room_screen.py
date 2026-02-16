import sys, os
import pygame
from utils import *
from multiplayer import create_room, is_player_guest
from sql_link import load_local_profile

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

leave_button_create = Shape('multiplayer_menu', '<', 50, 50, (10, 10), 2, (200, 0, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))
title_create = Shape(None, 'Créer une partie', current_w/2 - 300, 100, (current_w/2 - 300, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 80))

def show_error_popup_pygame(screen, message):
    """Popup d'erreur en Pygame pur (pas de Tkinter !)"""
    w, h = screen.get_size()
    font_title = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 30)
    font_text = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 20)
    
    # Rectangles
    popup_w, popup_h = 500, 200
    popup_x, popup_y = w//2 - popup_w//2, h//2 - popup_h//2
    button_rect = pygame.Rect(popup_x + 200, popup_y + 140, 100, 40)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    return
            
            if event.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(event.pos):
                    return
        
        # Assombrit l'arrière-plan
        overlay = pygame.Surface((w, h))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Popup
        pygame.draw.rect(screen, (205, 228, 226), (popup_x, popup_y, popup_w, popup_h), border_radius=15)
        
        # Titre
        title = font_title.render("Accès refusé", True, (255, 0, 0))
        screen.blit(title, (popup_x + popup_w//2 - title.get_width()//2, popup_y + 20))
        
        # Message (2 lignes)
        lines = [
            "Les invités ne peuvent pas créer de partie.",
            "Veuillez vous connecter avec un compte."
        ]
        
        y_offset = popup_y + 70
        for line in lines:
            text = font_text.render(line, True, (0, 0, 0))
            screen.blit(text, (popup_x + popup_w//2 - text.get_width()//2, y_offset))
            y_offset += 30
        
        # Bouton OK
        mouse_pos = pygame.mouse.get_pos()
        button_color = (200, 110, 0) if button_rect.collidepoint(mouse_pos) else (255, 145, 0)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        ok_text = font_text.render("OK", True, (255, 255, 255))
        screen.blit(ok_text, (button_rect.centerx - ok_text.get_width()//2, button_rect.centery - ok_text.get_height()//2))
        
        pygame.display.flip()
        clock.tick(60)

def create_room_screen_display():
    screen = pygame.display.get_surface()
    
    pseudo = load_local_profile()
    
    # ✅ Vérifie si invité SANS Tkinter
    if is_player_guest(pseudo):
        show_error_popup_pygame(screen, "Invité bloqué")
        return "multiplayer_menu"
    
    dest = leave_button_create.draw()
    if dest:
        return dest
    
    title_create.draw()
    game_question.draw()
    
    dest = nb_5.draw()
    if dest == '5':
        print("Création partie 5 manches")
        room_code = create_room(pseudo, 5)
        if room_code:
            print(f"Room créée: {room_code}")
            pygame.time.delay(300)
            return ('waiting_room', room_code, True)
        else:
            print("Erreur création room")
    
    dest = nb_10.draw()
    if dest == '10':
        print("Création partie 10 manches")
        room_code = create_room(pseudo, 10)
        if room_code:
            print(f"Room créée: {room_code}")
            pygame.time.delay(300)
            return ('waiting_room', room_code, True)
        else:
            print("Erreur création room")
    
    dest = nb_20.draw()
    if dest == '20':
        print("Création partie 20 manches")
        room_code = create_room(pseudo, 20)
        if room_code:
            print(f"Room créée: {room_code}")
            pygame.time.delay(300)
            return ('waiting_room', room_code, True)
        else:
            print("Erreur création room")
    
    return "create_room_screen"