"""
Module de gestion audio centralisé
Gère les musiques de fond et les effets sonores du jeu
"""

import pygame
import os

def resource_path(relative_path):
    """Retourne le chemin absolu d'une ressource"""
    import sys
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class AudioManager:
    """Gestionnaire audio singleton"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not AudioManager._initialized:
            pygame.mixer.init()
            
            # Musiques de fond
            self.music_menu = None
            self.music_game = None
            self.current_music = None
            
            # Effets sonores
            self.sound_click = None
            self.sound_typing = None
            
            # ✅ Charge les volumes depuis la config
            try:
                from config_manager import get_volumes
                music_vol, sfx_vol = get_volumes()
                self.music_volume = music_vol
                self.sfx_volume = sfx_vol
                print(f"✅ Volumes chargés : Musique={int(music_vol*100)}%, SFX={int(sfx_vol*100)}%")
            except Exception as e:
                print(f"⚠️ Erreur chargement volumes: {e}, valeurs par défaut")
                self.music_volume = 0.3
                self.sfx_volume = 0.5
            
            self.music_enabled = True
            self.sfx_enabled = True
            
            self._load_sounds()
            AudioManager._initialized = True
    
    def _load_sounds(self):
        """Charge tous les sons depuis le dossier musics"""
        try:
            # Musiques
            menu_path = resource_path("GuessMyClass/musics/menu.ogg")
            if os.path.exists(menu_path):
                self.music_menu = menu_path
                print(f"✅ Musique menu chargée")
            
            game_path = resource_path("GuessMyClass/musics/fond.ogg")
            if os.path.exists(game_path):
                self.music_game = game_path
                print(f"✅ Musique jeu chargée")
            
            # Effets sonores
            click_path = resource_path("GuessMyClass/musics/click.ogg")
            if os.path.exists(click_path):
                self.sound_click = pygame.mixer.Sound(click_path)
                self.sound_click.set_volume(self.sfx_volume)
                print(f"✅ Son click chargé")
            
            typing_path = resource_path("GuessMyClass/musics/typing.ogg")
            if os.path.exists(typing_path):
                self.sound_typing = pygame.mixer.Sound(typing_path)
                self.sound_typing.set_volume(self.sfx_volume)
                print(f"✅ Son typing chargé")
        
        except Exception as e:
            print(f"⚠️ Erreur chargement audio: {e}")
    
    # ═══════════════════════════════════════════════════════════
    # MUSIQUES DE FOND
    # ═══════════════════════════════════════════════════════════
    
    def play_music_menu(self):
        """Joue la musique de menu en boucle"""
        if not self.music_enabled or not self.music_menu:
            return
        
        if self.current_music != "menu":
            try:
                pygame.mixer.music.load(self.music_menu)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # -1 = boucle infinie
                self.current_music = "menu"
                print("🎵 Musique menu démarrée")
            except Exception as e:
                print(f"⚠️ Erreur lecture musique menu: {e}")
    
    def play_music_game(self):
        """Joue la musique de gameplay en boucle"""
        if not self.music_enabled or not self.music_game:
            return
        
        if self.current_music != "game":
            try:
                pygame.mixer.music.load(self.music_game)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # -1 = boucle infinie
                self.current_music = "game"
                print("🎵 Musique gameplay démarrée")
            except Exception as e:
                print(f"⚠️ Erreur lecture musique jeu: {e}")
    
    def stop_music(self):
        """Arrête la musique en cours"""
        try:
            pygame.mixer.music.stop()
            self.current_music = None
        except Exception as e:
            print(f"⚠️ Erreur arrêt musique: {e}")
    
    def set_music_volume(self, volume):
        """Change le volume de la musique (0.0 à 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception as e:
            print(f"⚠️ Erreur changement volume musique: {e}")
    
    # ═══════════════════════════════════════════════════════════
    # EFFETS SONORES
    # ═══════════════════════════════════════════════════════════
    
    def play_click(self):
        """Joue le son de clic"""
        if self.sfx_enabled and self.sound_click:
            try:
                self.sound_click.play()
            except Exception as e:
                print(f"⚠️ Erreur son click: {e}")
    
    def play_typing(self):
        """Joue le son de frappe clavier"""
        if self.sfx_enabled and self.sound_typing:
            try:
                self.sound_typing.play()
            except Exception as e:
                print(f"⚠️ Erreur son typing: {e}")
    
    def set_sfx_volume(self, volume):
        """Change le volume des effets sonores (0.0 à 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        if self.sound_click:
            self.sound_click.set_volume(self.sfx_volume)
        if self.sound_typing:
            self.sound_typing.set_volume(self.sfx_volume)
    
    # ═══════════════════════════════════════════════════════════
    # ACTIVATION/DÉSACTIVATION
    # ═══════════════════════════════════════════════════════════
    
    def toggle_music(self):
        """Active/désactive la musique"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
        else:
            # Rejoue la musique appropriée
            if self.current_music == "menu":
                self.play_music_menu()
            elif self.current_music == "game":
                self.play_music_game()
    
    def toggle_sfx(self):
        """Active/désactive les effets sonores"""
        self.sfx_enabled = not self.sfx_enabled


# ═══════════════════════════════════════════════════════════
# INSTANCE GLOBALE
# ═══════════════════════════════════════════════════════════

audio = AudioManager()