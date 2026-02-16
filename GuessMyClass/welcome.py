import sys, os
import pygame
from supabase import create_client
from utils import resource_path

# Initialisation Supabase
SUPABASE_URL = "https://dfrfhlvbckvakgtridzv.supabase.co"
SUPABASE_KEY = "sb_publishable_OEqgvVyKwJGXy5rV1H1Y8Q_kGL98num"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_local_profile(pseudo):
    """Sauvegarde le pseudo localement"""
    path = resource_path("GuessMyClass/profile/compte.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(pseudo)

def check_or_create_profile(pseudo):
    """Vérifie si le pseudo existe, sinon le crée automatiquement"""
    try:
        result = supabase.table("leaderboard")\
            .select("pseudo")\
            .eq("pseudo", pseudo)\
            .limit(1)\
            .execute()
        
        if result.data and len(result.data) > 0:
            print(f"✅ Connexion: {pseudo}")
            return True
        else:
            supabase.table("leaderboard").insert({
                "pseudo": pseudo,
                "mode": 5,
                "score": 0
            }).execute()
            print(f"✅ Compte créé: {pseudo}")
            return True
            
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def show_login_popup(screen, w, h):
    """Fenêtre de connexion en Pygame pur (pas de Tkinter !)"""
    font_title = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 35)
    font_text = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 20)
    font_input = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 25)
    
    # Variables
    pseudo_text = ""
    error_message = ""
    input_active = True
    
    # Rectangles
    popup_w, popup_h = 400, 280
    popup_x, popup_y = w//2 - popup_w//2, h//2 - popup_h//2
    
    input_rect = pygame.Rect(popup_x + 50, popup_y + 110, 300, 40)
    button_valider_rect = pygame.Rect(popup_x + 100, popup_y + 180, 200, 45)
    button_annuler_rect = pygame.Rect(popup_x + 100, popup_y + 235, 200, 30)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        # Validation avec Entrée
                        if len(pseudo_text) < 3:
                            error_message = "Minimum 3 caractères"
                        elif len(pseudo_text) > 20:
                            error_message = "Maximum 20 caractères"
                        else:
                            success = check_or_create_profile(pseudo_text)
                            if success:
                                save_local_profile(pseudo_text)
                                return True
                            else:
                                error_message = "Erreur de connexion"
                    elif event.key == pygame.K_BACKSPACE:
                        pseudo_text = pseudo_text[:-1]
                        error_message = ""
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    else:
                        if len(pseudo_text) < 20 and event.unicode.isprintable():
                            pseudo_text += event.unicode
                            error_message = ""
            
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                
                # Clic sur champ de saisie
                if input_rect.collidepoint(x, y):
                    input_active = True
                
                # Bouton Valider
                if button_valider_rect.collidepoint(x, y):
                    if len(pseudo_text) < 3:
                        error_message = "Minimum 3 caractères"
                    elif len(pseudo_text) > 20:
                        error_message = "Maximum 20 caractères"
                    else:
                        success = check_or_create_profile(pseudo_text)
                        if success:
                            save_local_profile(pseudo_text)
                            return True
                        else:
                            error_message = "Erreur de connexion"
                
                # Bouton Annuler
                if button_annuler_rect.collidepoint(x, y):
                    return None
        
        # Assombrit l'arrière-plan
        overlay = pygame.Surface((w, h))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Popup
        pygame.draw.rect(screen, (205, 228, 226), (popup_x, popup_y, popup_w, popup_h), border_radius=15)
        
        # Titre
        title = font_title.render("Connexion", True, (0, 0, 0))
        screen.blit(title, (popup_x + popup_w//2 - title.get_width()//2, popup_y + 20))
        
        # Label
        label = font_text.render("Entrez votre pseudo :", True, (85, 85, 85))
        screen.blit(label, (popup_x + 50, popup_y + 75))
        
        # Champ de saisie
        input_color = (255, 145, 0) if input_active else (150, 150, 150)
        pygame.draw.rect(screen, input_color, input_rect, 3, border_radius=5)
        
        # Texte saisi
        text_surface = font_input.render(pseudo_text, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 8))
        
        # Curseur clignotant
        if input_active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = input_rect.x + 10 + text_surface.get_width() + 2
            pygame.draw.line(screen, (0, 0, 0), (cursor_x, input_rect.y + 8), (cursor_x, input_rect.y + 32), 2)
        
        # Message d'erreur
        if error_message:
            error_surf = font_text.render(error_message, True, (255, 0, 0))
            screen.blit(error_surf, (popup_x + popup_w//2 - error_surf.get_width()//2, popup_y + 155))
        
        # Bouton Valider
        mouse_pos = pygame.mouse.get_pos()
        valider_color = (200, 110, 0) if button_valider_rect.collidepoint(mouse_pos) else (255, 145, 0)
        pygame.draw.rect(screen, valider_color, button_valider_rect, border_radius=10)
        valider_text = font_text.render("Valider", True, (255, 255, 255))
        screen.blit(valider_text, (button_valider_rect.centerx - valider_text.get_width()//2, button_valider_rect.centery - valider_text.get_height()//2))
        
        # Bouton Annuler
        annuler_color = (100, 100, 100) if button_annuler_rect.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(screen, annuler_color, button_annuler_rect, border_radius=8)
        annuler_text = font_text.render("Annuler", True, (255, 255, 255))
        screen.blit(annuler_text, (button_annuler_rect.centerx - annuler_text.get_width()//2, button_annuler_rect.centery - annuler_text.get_height()//2))
        
        pygame.display.flip()
        clock.tick(60)

def welcome_display():
    """Écran d'accueil avec popup Pygame (pas de Tkinter !)"""
    screen = pygame.display.get_surface()
    w, h = screen.get_size()
    
    font_title = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 80)
    font_subtitle = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 50)
    font_button = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 30)
    
    bg_color = (205, 228, 226)
    title_color = (255, 255, 255)
    subtitle_color = (255, 255, 255)
    button_login_color = (180, 130, 230)
    button_login_hover = (150, 100, 200)
    button_guest_color = (180, 180, 180)
    button_guest_hover = (150, 150, 150)
    
    button_w, button_h = 350, 80
    button_login_rect = pygame.Rect(w//2 - 400, h//2 + 100, button_w, button_h)
    button_guest_rect = pygame.Rect(w//2 + 50, h//2 + 100, button_w, button_h)
    
    login_was_pressed = False
    guest_was_pressed = False
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'hell'
        
        login_hovered = button_login_rect.collidepoint(mouse_pos)
        guest_hovered = button_guest_rect.collidepoint(mouse_pos)
        
        if not mouse_pressed:
            # ===== BOUTON CRÉER/SE CONNECTER =====
            if login_hovered and login_was_pressed:
                login_was_pressed = False
                
                # Affiche le popup PYGAME (pas de Tkinter !)
                result = show_login_popup(screen, w, h)
                
                if result:
                    return 'home'
            
            # ===== BOUTON INVITÉ =====
            if guest_hovered and guest_was_pressed:
                guest_was_pressed = False
                save_local_profile("Invite\ninvit")
                return 'home'
        
        if mouse_pressed:
            if login_hovered:
                login_was_pressed = True
            if guest_hovered:
                guest_was_pressed = True
        
        # ===== DESSIN =====
        screen.fill(bg_color)
        
        title_text = font_title.render("Bienvenue sur GMC !", True, title_color)
        title_rect = title_text.get_rect(center=(w//2, 100))
        title_bg = pygame.Rect(title_rect.x - 20, title_rect.y - 10, title_rect.width + 40, title_rect.height + 20)
        pygame.draw.rect(screen, (104, 180, 229), title_bg, border_radius=15)
        screen.blit(title_text, title_rect)
        
        subtitle_text = font_subtitle.render("Que voulez-vous faire ?", True, subtitle_color)
        subtitle_rect = subtitle_text.get_rect(center=(w//2, 250))
        subtitle_bg = pygame.Rect(subtitle_rect.x - 20, subtitle_rect.y - 10, subtitle_rect.width + 40, subtitle_rect.height + 20)
        pygame.draw.rect(screen, (150, 180, 220), subtitle_bg, border_radius=15)
        screen.blit(subtitle_text, subtitle_rect)
        
        # Bouton "Créer/Se connecter"
        color_login = button_login_hover if login_hovered else button_login_color
        pygame.draw.rect(screen, color_login, button_login_rect, border_radius=15)
        login_text = font_button.render("Créer/Se connecter", True, (255, 255, 255))
        login_text_rect = login_text.get_rect(center=button_login_rect.center)
        screen.blit(login_text, login_text_rect)
        
        # Bouton "Jouer sans compte"
        color_guest = button_guest_hover if guest_hovered else button_guest_color
        pygame.draw.rect(screen, color_guest, button_guest_rect, border_radius=15)
        guest_text = font_button.render("Jouer sans compte", True, (255, 255, 255))
        guest_text_rect = guest_text.get_rect(center=button_guest_rect.center)
        screen.blit(guest_text, guest_text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return None