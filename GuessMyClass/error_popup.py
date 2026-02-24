"""
Module de popup d'erreur Pygame réutilisable
"""

import pygame
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def show_error_popup_connection(screen, title="Erreur de connexion", message="Impossible de se connecter au serveur"):
    """
    Affiche un popup d'erreur de connexion.
    Utilisé quand Supabase est inaccessible.
    """
    w, h = screen.get_size()
    font_title = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 30)
    font_text = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 20)
    
    popup_w, popup_h = 500, 220
    popup_x = w // 2 - popup_w // 2
    popup_y = h // 2 - popup_h // 2
    button_rect = pygame.Rect(popup_x + 200, popup_y + 160, 100, 40)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return
            if event.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(event.pos):
                    return
        
        # Overlay sombre
        overlay = pygame.Surface((w, h))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Popup
        pygame.draw.rect(screen, (255, 230, 230), (popup_x, popup_y, popup_w, popup_h), border_radius=15)
        
        # Titre
        title_surf = font_title.render(title, True, (200, 0, 0))
        screen.blit(title_surf, (popup_x + popup_w // 2 - title_surf.get_width() // 2, popup_y + 20))
        
        # Message (2 lignes possibles)
        lines = message.split('\n') if '\n' in message else [message]
        y_offset = popup_y + 70
        for line in lines:
            text = font_text.render(line, True, (0, 0, 0))
            screen.blit(text, (popup_x + popup_w // 2 - text.get_width() // 2, y_offset))
            y_offset += 30
        
        # Conseil
        hint = font_text.render("Vérifiez votre connexion Internet", True, (100, 100, 100))
        screen.blit(hint, (popup_x + popup_w // 2 - hint.get_width() // 2, popup_y + 120))
        
        # Bouton OK
        mouse_pos = pygame.mouse.get_pos()
        button_color = (200, 110, 0) if button_rect.collidepoint(mouse_pos) else (255, 145, 0)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        ok_text = font_text.render("OK", True, (255, 255, 255))
        screen.blit(ok_text, (button_rect.centerx - ok_text.get_width() // 2,
                               button_rect.centery - ok_text.get_height() // 2))
        
        pygame.display.flip()
        clock.tick(60)