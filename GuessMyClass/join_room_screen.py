import sys, os
import pygame
from utils import *
from multiplayer import join_room, get_room_info, MAX_PLAYERS
from sql_link import load_local_profile
from text_input import TextInput

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def show_error_popup(screen, title_text, message):
    w, h = screen.get_size()
    font_title = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 30)
    font_text  = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 20)

    popup_w, popup_h = 450, 180
    popup_x = w // 2 - popup_w // 2
    popup_y = h // 2 - popup_h // 2
    button_rect = pygame.Rect(popup_x + 175, popup_y + 120, 100, 40)

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

        overlay = pygame.Surface((w, h))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (205, 228, 226), (popup_x, popup_y, popup_w, popup_h), border_radius=15)

        title = font_title.render(title_text, True, (255, 0, 0))
        screen.blit(title, (popup_x + popup_w // 2 - title.get_width() // 2, popup_y + 20))

        text = font_text.render(message, True, (0, 0, 0))
        screen.blit(text, (popup_x + popup_w // 2 - text.get_width() // 2, popup_y + 70))

        mouse_pos = pygame.mouse.get_pos()
        button_color = (200, 110, 0) if button_rect.collidepoint(mouse_pos) else (255, 145, 0)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        ok_text = font_text.render("OK", True, (255, 255, 255))
        screen.blit(ok_text, (button_rect.centerx - ok_text.get_width() // 2,
                               button_rect.centery - ok_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)


class UppercaseTextInput(TextInput):
    """TextInput spécialisé : force l'uppercase et n'accepte que les alphanumériques"""

    def handle_event(self, event):
        # Pour les caractères normaux, on force l'uppercase avant de déléguer
        if event.type == pygame.KEYDOWN:
            if event.unicode and event.unicode.isalnum():
                upper_char = event.unicode.upper()
                if len(self.text) < self.max_length:
                    self.text = self.text[:self.cursor_pos] + upper_char + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
                    # ✅ Joue le son typing
                    try:
                        from audio_manager import audio
                        audio.play_typing()
                    except:
                        pass
                    return True
                return False
        # Pour tout le reste (backspace, flèches, delete...) on délègue au parent
        return super().handle_event(event)


def show_join_popup(screen):
    w, h = screen.get_size()
    font_title = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 35)
    font_text  = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 20)
    font_input = pygame.font.Font(resource_path("GuessMyClass/font/MightySouly.ttf"), 30)

    popup_w, popup_h = 400, 290
    popup_x = w // 2 - popup_w // 2
    popup_y = h // 2 - popup_h // 2

    input_rect          = pygame.Rect(popup_x + 50, popup_y + 100, 300, 45)
    button_join_rect    = pygame.Rect(popup_x + 100, popup_y + 170, 200, 45)
    button_cancel_rect  = pygame.Rect(popup_x + 100, popup_y + 230, 200, 35)

    # ✅ TextInput uppercase, max 6 caractères, alphanumériques seulement
    text_input = UppercaseTextInput(input_rect, font_input, max_length=6)

    clock = pygame.time.Clock()

    def try_join():
        code = text_input.get_text()
        if len(code) != 6:
            show_error_popup(screen, "Code invalide", "Le code doit contenir 6 caractères")
            return None
        pseudo = load_local_profile()
        room = join_room(code, pseudo)
        if room:
            return ('waiting_room', code, False)
        else:
            room_info = get_room_info(code)
            if room_info and len(room_info["players"]) >= MAX_PLAYERS:
                show_error_popup(screen, "Partie pleine", f"Max {MAX_PLAYERS} joueurs")
            else:
                show_error_popup(screen, "Erreur", "Partie introuvable ou déjà commencée")
            return None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    result = try_join()
                    if result:
                        return result
                elif event.key == pygame.K_ESCAPE:
                    return None
                else:
                    # ✅ Délègue au TextInput uppercase
                    text_input.handle_event(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                if button_cancel_rect.collidepoint(event.pos):
                    return None
                if button_join_rect.collidepoint(event.pos):
                    result = try_join()
                    if result:
                        return result

            # ✅ Clic souris dans le champ pour positionner le curseur
            elif event.type == pygame.MOUSEBUTTONDOWN:
                text_input.handle_event(event)

        # Overlay
        overlay = pygame.Surface((w, h))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Popup
        pygame.draw.rect(screen, (205, 228, 226), (popup_x, popup_y, popup_w, popup_h), border_radius=15)

        # Titre
        title = font_title.render("Rejoindre une partie", True, (0, 0, 0))
        screen.blit(title, (popup_x + popup_w // 2 - title.get_width() // 2, popup_y + 20))

        # Label
        label = font_text.render("Code de la partie :", True, (85, 85, 85))
        screen.blit(label, (popup_x + 50, popup_y + 65))

        # ✅ Champ de saisie avancé (uppercase, max 6)
        text_input.draw(screen)

        # Compteur de caractères
        counter = font_text.render(f"{len(text_input.get_text())}/6", True, (100, 100, 100))
        screen.blit(counter, (popup_x + popup_w - 60, popup_y + 150))

        mouse_pos = pygame.mouse.get_pos()

        # Bouton Rejoindre
        join_color = (200, 110, 0) if button_join_rect.collidepoint(mouse_pos) else (255, 145, 0)
        pygame.draw.rect(screen, join_color, button_join_rect, border_radius=10)
        join_text = font_text.render("Rejoindre", True, (255, 255, 255))
        screen.blit(join_text, (button_join_rect.centerx - join_text.get_width() // 2,
                                button_join_rect.centery - join_text.get_height() // 2))

        # Bouton Annuler (rouge)
        cancel_color = (180, 0, 0) if button_cancel_rect.collidepoint(mouse_pos) else (200, 0, 0)
        pygame.draw.rect(screen, cancel_color, button_cancel_rect, border_radius=8)
        cancel_text = font_text.render("Annuler", True, (255, 255, 255))
        screen.blit(cancel_text, (button_cancel_rect.centerx - cancel_text.get_width() // 2,
                                  button_cancel_rect.centery - cancel_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)


def join_room_screen_display():
    # ✅ Lance la musique de menu
    try:
        from audio_manager import audio
        audio.play_music_menu()
    except:
        pass
    
    screen = pygame.display.get_surface()
    result = show_join_popup(screen)
    if result:
        return result
    return "multiplayer_menu"