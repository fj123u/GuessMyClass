import sys, os
import pygame
from utils import *
from multiplayer import join_room, get_room_info, MAX_PLAYERS
from sql_link import load_local_profile

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def show_error_popup(screen, title_text, message):
    """Popup d'erreur en Pygame"""
    w, h = screen.get_size()
    font_title = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 30)
    font_text = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 20)
    
    popup_w, popup_h = 450, 180
    popup_x, popup_y = w//2 - popup_w//2, h//2 - popup_h//2
    button_rect = pygame.Rect(popup_x + 175, popup_y + 120, 100, 40)
    
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
        title = font_title.render(title_text, True, (255, 0, 0))
        screen.blit(title, (popup_x + popup_w//2 - title.get_width()//2, popup_y + 20))
        
        # Message
        text = font_text.render(message, True, (0, 0, 0))
        screen.blit(text, (popup_x + popup_w//2 - text.get_width()//2, popup_y + 70))
        
        # Bouton OK
        mouse_pos = pygame.mouse.get_pos()
        button_color = (200, 110, 0) if button_rect.collidepoint(mouse_pos) else (255, 145, 0)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        ok_text = font_text.render("OK", True, (255, 255, 255))
        screen.blit(ok_text, (button_rect.centerx - ok_text.get_width()//2, button_rect.centery - ok_text.get_height()//2))
        
        pygame.display.flip()
        clock.tick(60)

def show_join_popup(screen):
    """Popup pour entrer le code de partie en Pygame"""
    w, h = screen.get_size()
    font_title = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 35)
    font_text = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 20)
    font_input = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 30)
    
    code_text = ""
    
    popup_w, popup_h = 400, 290
    popup_x, popup_y = w//2 - popup_w//2, h//2 - popup_h//2
    
    input_rect = pygame.Rect(popup_x + 50, popup_y + 100, 300, 45)
    button_join_rect = pygame.Rect(popup_x + 100, popup_y + 170, 200, 45)
    button_cancel_rect = pygame.Rect(popup_x + 100, popup_y + 230, 200, 35)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Validation
                    if len(code_text) != 6:
                        show_error_popup(screen, "Code invalide", "Le code doit contenir 6 caractères")
                    else:
                        pseudo = load_local_profile()
                        room = join_room(code_text.upper(), pseudo)
                        
                        if room:
                            return ('waiting_room', code_text.upper(), False)
                        else:
                            room_info = get_room_info(code_text.upper())
                            if room_info and len(room_info["players"]) >= MAX_PLAYERS:
                                show_error_popup(screen, "Partie pleine", f"Cette partie est complète ({MAX_PLAYERS} joueurs max)")
                            else:
                                show_error_popup(screen, "Erreur", "Partie introuvable ou déjà commencée")
                
                elif event.key == pygame.K_BACKSPACE:
                    code_text = code_text[:-1]
                
                elif event.key == pygame.K_ESCAPE:
                    return None
                
                else:
                    # Accepte seulement lettres et chiffres, max 6 caractères
                    if len(code_text) < 6 and (event.unicode.isalnum()):
                        code_text += event.unicode.upper()
            
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                
                # Bouton Annuler
                if button_cancel_rect.collidepoint(x, y):
                    return None
                
                # Bouton Rejoindre
                if button_join_rect.collidepoint(x, y):
                    if len(code_text) != 6:
                        show_error_popup(screen, "Code invalide", "Le code doit contenir 6 caractères")
                    else:
                        pseudo = load_local_profile()
                        room = join_room(code_text.upper(), pseudo)
                        
                        if room:
                            return ('waiting_room', code_text.upper(), False)
                        else:
                            room_info = get_room_info(code_text.upper())
                            if room_info and len(room_info["players"]) >= MAX_PLAYERS:
                                show_error_popup(screen, "Partie pleine", f"Cette partie est complète ({MAX_PLAYERS} joueurs max)")
                            else:
                                show_error_popup(screen, "Erreur", "Partie introuvable ou déjà commencée")
        
        # Assombrit l'arrière-plan
        overlay = pygame.Surface((w, h))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Popup
        pygame.draw.rect(screen, (205, 228, 226), (popup_x, popup_y, popup_w, popup_h), border_radius=15)
        
        # Titre
        title = font_title.render("Rejoindre une partie", True, (0, 0, 0))
        screen.blit(title, (popup_x + popup_w//2 - title.get_width()//2, popup_y + 20))
        
        # Label
        label = font_text.render("Code de la partie :", True, (85, 85, 85))
        screen.blit(label, (popup_x + 50, popup_y + 65))
        
        # Champ de saisie
        pygame.draw.rect(screen, (255, 145, 0), input_rect, 3, border_radius=5)
        
        # Texte saisi (centré avec espacement)
        display_text = " ".join(code_text)  # Espace entre chaque lettre
        text_surface = font_input.render(display_text, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect.centerx - text_surface.get_width()//2, input_rect.y + 8))
        
        # Curseur clignotant
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = input_rect.centerx + text_surface.get_width()//2 + 5
            pygame.draw.line(screen, (0, 0, 0), (cursor_x, input_rect.y + 10), (cursor_x, input_rect.y + 35), 2)
        
        # Compteur de caractères
        counter = font_text.render(f"{len(code_text)}/6", True, (100, 100, 100))
        screen.blit(counter, (popup_x + popup_w - 60, popup_y + 150))
        
        # Bouton Rejoindre
        mouse_pos = pygame.mouse.get_pos()
        button_color = (200, 110, 0) if button_join_rect.collidepoint(mouse_pos) else (255, 145, 0)
        pygame.draw.rect(screen, button_color, button_join_rect, border_radius=10)
        join_text = font_text.render("Rejoindre", True, (255, 255, 255))
        screen.blit(join_text, (button_join_rect.centerx - join_text.get_width()//2, button_join_rect.centery - join_text.get_height()//2))
        
        # ✅ Bouton Annuler ROUGE
        button_cancel_color = (180, 0, 0) if button_cancel_rect.collidepoint(mouse_pos) else (200, 0, 0)
        pygame.draw.rect(screen, button_cancel_color, button_cancel_rect, border_radius=8)
        cancel_text = font_text.render("Annuler", True, (255, 255, 255))
        screen.blit(cancel_text, (button_cancel_rect.centerx - cancel_text.get_width()//2, button_cancel_rect.centery - cancel_text.get_height()//2))
        
        pygame.display.flip()
        clock.tick(60)

def join_room_screen_display():
    screen = pygame.display.get_surface()
    
    # Affiche le popup de saisie du code
    result = show_join_popup(screen)
    
    if result:
        return result
    
    return "multiplayer_menu"