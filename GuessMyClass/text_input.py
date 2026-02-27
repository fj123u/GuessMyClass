import pygame

class TextInput:
    """
    Champ de saisie avancé avec :
    - Répétition des touches (rester appuyé)
    - Curseur mobile avec flèches gauche/droite
    - Clic souris pour positionner le curseur
    - Supprimer en restant appuyé sur Delete/Backspace
    - Sélection avec Ctrl+A, tout supprimer avec Delete
    """
    
    def __init__(self, rect, font, max_length=20, allowed_chars=None):
        """
        rect : pygame.Rect - position et taille du champ
        font : pygame.font.Font - police d'écriture
        max_length : int - nombre max de caractères
        allowed_chars : str ou None - si None, accepte tout caractère imprimable
                        ex: "abcdefghijklmnopqrstuvwxyz0123456789" pour alphanumériques
        """
        self.rect = rect
        self.font = font
        self.max_length = max_length
        self.allowed_chars = allowed_chars
        
        self.text = ""
        self.cursor_pos = 0  # Position du curseur dans le texte
        self.active = True
        
        # Couleurs
        self.color_active = (255, 145, 0)    # Orange quand actif
        self.color_inactive = (150, 150, 150) # Gris quand inactif
        self.color_bg = (255, 255, 255)       # Fond blanc
        self.color_text = (0, 0, 0)           # Texte noir
        self.color_cursor = (0, 0, 0)         # Curseur noir
        
        # Répétition touches (delay initial, puis interval)
        pygame.key.set_repeat(400, 40)  # 400ms avant répétition, puis toutes les 40ms
    
    def handle_event(self, event):
        """Gère les événements clavier et souris. Retourne True si modifié."""
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = True
                # ✅ Clic souris : positionne le curseur à l'endroit cliqué
                click_x = event.pos[0] - self.rect.x - 10
                self.cursor_pos = self._get_cursor_from_x(click_x)
                return True
            else:
                self.active = False
        
        if not self.active:
            return False
        
        if event.type == pygame.KEYDOWN:
            
            # ✅ Flèche gauche : déplace le curseur à gauche
            if event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)
                return True
            
            # ✅ Flèche droite : déplace le curseur à droite
            if event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                return True
            
            # ✅ Home : curseur au début
            if event.key == pygame.K_HOME:
                self.cursor_pos = 0
                return True
            
            # ✅ End : curseur à la fin
            if event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
                return True
            
            # ✅ Backspace : supprime le caractère AVANT le curseur (répété si maintenu)
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
                    # ✅ Joue le son typing lors de la suppression
                    try:
                        from audio_manager import audio
                        audio.play_typing()
                    except:
                        pass  # Ignore si audio_manager non dispo
                return True
            
            # ✅ Delete : supprime le caractère APRÈS le curseur (répété si maintenu)
            if event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                    # ✅ Joue le son typing lors de la suppression
                    try:
                        from audio_manager import audio
                        audio.play_typing()
                    except:
                        pass  # Ignore si audio_manager non dispo
                return True
            
            # ✅ Ctrl+A : sélectionne tout (puis backspace supprime tout)
            if event.key == pygame.K_a and (event.mod & pygame.KMOD_CTRL):
                self.text = ""
                self.cursor_pos = 0
                return True
            
            # ✅ Caractères normaux : insère à la position du curseur
            if event.unicode and event.unicode.isprintable():
                char = event.unicode
                
                # Filtre les caractères autorisés si défini
                if self.allowed_chars and char not in self.allowed_chars:
                    return False
                
                # Vérifie la longueur max
                if len(self.text) < self.max_length:
                    self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
                    
                    # ✅ Joue le son typing
                    try:
                        from audio_manager import audio
                        audio.play_typing()
                    except:
                        pass  # Ignore si audio_manager non dispo
                    
                    return True
        
        return False
    
    def _get_cursor_from_x(self, click_x):
        """Calcule la position du curseur selon l'endroit cliqué"""
        if click_x <= 0:
            return 0
        
        for i in range(len(self.text) + 1):
            w, _ = self.font.size(self.text[:i])
            w_next = self.font.size(self.text[:i+1])[0] if i < len(self.text) else w + 999
            if click_x < (w + w_next) / 2:
                return i
        
        return len(self.text)
    
    def draw(self, screen):
        """Dessine le champ de saisie"""
        # Fond blanc
        pygame.draw.rect(screen, self.color_bg, self.rect, border_radius=5)
        
        # Bordure (orange si actif, gris sinon)
        border_color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=5)
        
        # Texte
        text_surface = self.font.render(self.text, True, self.color_text)
        text_x = self.rect.x + 10
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))
        
        # ✅ Curseur clignotant à la bonne position
        if self.active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x_offset = self.font.size(self.text[:self.cursor_pos])[0]
            cursor_x = text_x + cursor_x_offset
            cursor_top = text_y + 2
            cursor_bottom = text_y + text_surface.get_height() - 2
            pygame.draw.line(screen, self.color_cursor, (cursor_x, cursor_top), (cursor_x, cursor_bottom), 2)
    
    def get_text(self):
        return self.text
    
    def set_text(self, text):
        self.text = text[:self.max_length]
        self.cursor_pos = len(self.text)
    
    def clear(self):
        self.text = ""
        self.cursor_pos = 0