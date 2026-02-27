"""
Menu des paramètres du jeu
- Volume musique de fond
- Volume effets sonores (popup, clicks, typing)
- Taille de la fenêtre
- Changement de pseudo
"""

import pygame
import sys, os
from shape_creator import *
from utils import *
from audio_manager import audio
from config_manager import load_config, save_config, set_pseudo, set_volumes, set_resolution
from text_input import TextInput

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ═══════════════════════════════════════════════════════════
# CLASSES POUR LES SLIDERS
# ═══════════════════════════════════════════════════════════

class Slider:
    """Slider pour régler un volume (0.0 à 1.0)"""
    
    def __init__(self, x, y, width, height, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial_value  # 0.0 à 1.0
        self.dragging = False
        
        # Couleurs
        self.bg_color = (100, 100, 100)
        self.bar_color = (255, 145, 0)
        self.handle_color = (255, 255, 255)
        self.handle_hover_color = (200, 200, 200)
    
    def handle_event(self, event):
        """Gère les événements souris"""
        mouse_pos = pygame.mouse.get_pos()
        handle_x = self.rect.x + int(self.value * self.rect.width)
        handle_rect = pygame.Rect(handle_x - 8, self.rect.y - 5, 16, self.rect.height + 10)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if handle_rect.collidepoint(mouse_pos) or self.rect.collidepoint(mouse_pos):
                self.dragging = True
                self._update_value(mouse_pos[0])
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                return True
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._update_value(mouse_pos[0])
                return True
        
        return False
    
    def _update_value(self, mouse_x):
        """Met à jour la valeur selon la position de la souris"""
        relative_x = mouse_x - self.rect.x
        self.value = max(0.0, min(1.0, relative_x / self.rect.width))
    
    def draw(self, screen):
        """Dessine le slider"""
        # Barre de fond
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        
        # Barre de progression
        progress_width = int(self.value * self.rect.width)
        if progress_width > 0:
            progress_rect = pygame.Rect(self.rect.x, self.rect.y, progress_width, self.rect.height)
            pygame.draw.rect(screen, self.bar_color, progress_rect, border_radius=5)
        
        # Poignée
        handle_x = self.rect.x + int(self.value * self.rect.width)
        handle_rect = pygame.Rect(handle_x - 8, self.rect.y - 5, 16, self.rect.height + 10)
        
        mouse_pos = pygame.mouse.get_pos()
        handle_color = self.handle_hover_color if handle_rect.collidepoint(mouse_pos) or self.dragging else self.handle_color
        
        pygame.draw.rect(screen, handle_color, handle_rect, border_radius=3)
        pygame.draw.rect(screen, (0, 0, 0), handle_rect, 2, border_radius=3)
        
        # Pourcentage
        font = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 20)
        percentage_text = font.render(f"{int(self.value * 100)}%", True, (255, 255, 255))
        screen.blit(percentage_text, (self.rect.right + 15, self.rect.centery - percentage_text.get_height() // 2))
    
    def get_value(self):
        """Retourne la valeur actuelle (0.0 à 1.0)"""
        return self.value
    
    def set_value(self, value):
        """Définit la valeur (0.0 à 1.0)"""
        self.value = max(0.0, min(1.0, value))


class ResolutionButton:
    """Bouton pour une résolution"""
    
    def __init__(self, x, y, width, height, resolution_text, is_current=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = resolution_text
        self.is_current = is_current
        self.hovered = False
        
        self.normal_color = (144, 180, 229)
        self.hover_color = (104, 140, 189)
        self.current_color = (255, 145, 0)
    
    def handle_event(self, event):
        """Gère les événements"""
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONUP and self.hovered:
            audio.play_click()
            return True
        
        return False
    
    def draw(self, screen):
        """Dessine le bouton"""
        if self.is_current:
            color = self.current_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.normal_color
        
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)
        
        font = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 25)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


# ═══════════════════════════════════════════════════════════
# FONCTION PRINCIPALE
# ═══════════════════════════════════════════════════════════

def settings_display():
    """Affiche le menu des paramètres"""
    
    # Lance la musique de menu
    try:
        audio.play_music_menu()
    except:
        pass
    
    screen = pygame.display.get_surface()
    w, h = screen.get_size()
    
    # Bouton retour
    leave_settings = Shape('home', '<', 50, 50, (10, 10), 2, (200, 0, 0), True, 
                          (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))
    
    # Titre avec fond bleu comme les autres menus
    font_title = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 80)
    font_label = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 35)
    
    # ─────────────────────────────────────────────────────
    # SLIDERS AUDIO
    # ─────────────────────────────────────────────────────
    
    slider_music = Slider(w // 2 - 150, 250, 300, 20, audio.music_volume)
    slider_sfx = Slider(w // 2 - 150, 350, 300, 20, audio.sfx_volume)
    
    # ─────────────────────────────────────────────────────
    # BOUTON CHANGER D'ÉCRAN
    # ─────────────────────────────────────────────────────
    
    change_screen_button = Shape('change_screen', "Changer d'écran", 280, 50, 
                                 (w // 2 - 140, 470), 3, (104, 180, 229), True,
                                 (resource_path("GuessMyClass/font/MightySouly.ttf"), 28))
    
    # ─────────────────────────────────────────────────────
    # BOUTONS PSEUDO
    # ─────────────────────────────────────────────────────
    
    change_pseudo_button = Shape('change_pseudo', 'Changer de pseudo', 280, 50, 
                                 (w // 2 - 290, h - 150), 3, (184, 180, 229), True,
                                 (resource_path("GuessMyClass/font/MightySouly.ttf"), 28))
    
    guest_mode_button = Shape('guest_mode', 'Mode invité', 280, 50, 
                             (w // 2 + 10, h - 150), 3, (144, 140, 189), True,
                             (resource_path("GuessMyClass/font/MightySouly.ttf"), 28))
    
    # État pour le popup de changement de pseudo
    show_pseudo_popup = False
    
    clock = pygame.time.Clock()
    
    # ═══════════════════════════════════════════════════════════
    # BOUCLE PRINCIPALE
    # ═══════════════════════════════════════════════════════════
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'hell'
            
            # Gestion des sliders
            if slider_music.handle_event(event):
                audio.set_music_volume(slider_music.get_value())
                # ✅ Sauvegarde dans la config
                set_volumes(slider_music.get_value(), slider_sfx.get_value())
            
            if slider_sfx.handle_event(event):
                audio.set_sfx_volume(slider_sfx.get_value())
                # ✅ Sauvegarde dans la config
                set_volumes(slider_music.get_value(), slider_sfx.get_value())
        
        # ─────────────────────────────────────────────────────
        # DESSIN
        # ─────────────────────────────────────────────────────
        
        screen.fill((205, 228, 226))
        
        # Bouton retour
        dest = leave_settings.draw()
        if dest:
            return dest
        
        # Titre avec fond bleu style GMC
        title_text = font_title.render("Paramètres", True, (255, 255, 255))
        title_width = title_text.get_width()
        title_bg = pygame.Rect(w // 2 - title_width // 2 - 30, 30, 
                               title_width + 60, title_text.get_height() + 30)
        pygame.draw.rect(screen, (104, 180, 229), title_bg, border_radius=15)
        screen.blit(title_text, (w // 2 - title_width // 2, 45))
        
        # Labels et sliders audio avec style cohérent
        music_label = font_label.render("Volume musique :", True, (50, 50, 50))
        screen.blit(music_label, (w // 2 - 150, 210))
        slider_music.draw(screen)
        
        sfx_label = font_label.render("Volume effets sonores :", True, (50, 50, 50))
        screen.blit(sfx_label, (w // 2 - 150, 310))
        slider_sfx.draw(screen)
        
        # Bouton changer d'écran
        dest = change_screen_button.draw()
        if dest == 'change_screen':
            # ✅ Bascule l'écran dans la config
            from config_manager import load_config, save_config
            import os
            
            config = load_config()
            
            # Récupère ou initialise le numéro d'écran actuel
            current_screen = config.get("display_screen", 0)
            
            # Bascule entre écran 0 et 1
            next_screen = 1 if current_screen == 0 else 0
            config["display_screen"] = next_screen
            save_config(config)
            
            print(f"✅ Écran changé : {current_screen} → {next_screen}")
            
            # Message
            overlay = pygame.Surface((w, h))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(220)
            screen.blit(overlay, (0, 0))
            
            font_msg = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 40)
            font_msg2 = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 35)
            msg = font_msg.render(f"Passage à l'écran {next_screen + 1}", True, (255, 255, 255))
            msg2 = font_msg2.render("Le jeu va redémarrer...", True, (255, 255, 255))
            
            screen.blit(msg, (w//2 - msg.get_width()//2, h//2 - 50))
            screen.blit(msg2, (w//2 - msg2.get_width()//2, h//2 + 10))
            
            pygame.display.flip()
            pygame.time.delay(2000)
            
            return 'hell'  # Redémarre
        
        # Bouton changer de pseudo
        dest = change_pseudo_button.draw()
        if dest == 'change_pseudo':
            # ✅ Utilise la même fonction que welcome
            from welcome import show_login_popup
            from config_manager import get_pseudo
            
            # Affiche le popup de connexion (réutilisé pour changement de pseudo)
            result = show_login_popup(screen, w, h)
            if result:
                print(f"✅ Pseudo changé avec succès")
        
        # Bouton mode invité
        dest = guest_mode_button.draw()
        if dest == 'guest_mode':
            # ✅ Repasse en mode invité
            from config_manager import set_pseudo
            set_pseudo("Invite")
            print("✅ Mode invité activé")
            
            # Message de confirmation
            overlay = pygame.Surface((w, h))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(200)
            screen.blit(overlay, (0, 0))
            
            font_msg = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 35)
            msg = font_msg.render("Mode invité activé", True, (255, 255, 255))
            msg2 = font_msg.render("Vous pouvez maintenant jouer sans compte", True, (255, 255, 255))
            screen.blit(msg, (w//2 - msg.get_width()//2, h//2 - 40))
            screen.blit(msg2, (w//2 - msg2.get_width()//2, h//2 + 10))
            
            pygame.display.flip()
            pygame.time.delay(2000)
            
            return 'home'
        
        pygame.display.flip()
        clock.tick(60)