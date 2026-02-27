# Importe les bibliothèques nécessaires pour le fonctionnement du code

import pygame
import sys, os

# Fonction pour faire le .exe
# Met le bon chemin de fichier
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Class utilisé pour créer les différentes formes pygame

class Shape:
    def __init__(self,destination,text,width,height,pos,elevation,color, button=False, font=(resource_path('GuessMyClass/font/MightySouly.ttf'), 80), around=True):
        pygame.font.get_init()
        self.destination = destination
        self.color = color
        self.color_dark = (color[0]-60,color[1]-60,color[2]-60)
        self.color_light_dark = (color[0]-30,color[1]-30,color[2]-30)
        self.font = pygame.font.Font(font[0],font[1])
        self.is_button = button
        self.around = around
        
        for i in range(0,3):
            if self.color_dark[i]<0:
                if i == 0:
                    self.color_dark = (0, self.color_dark[1], self.color_dark[2])
                if i == 1:
                    self.color_dark = (self.color_dark[0], 0, self.color_dark[2])
                if i == 2:
                    self.color_dark = (self.color_dark[0], self.color_dark[1], 0)
                    
            if self.color_light_dark[i]<0:
                if i == 0:
                    self.color_light_dark = (0, self.color_light_dark[1], self.color_light_dark[2])
                if i == 1:
                    self.color_light_dark = (self.color_light_dark[0], 0, self.color_light_dark[2])
                if i == 2:
                    self.color_light_dark = (self.color_light_dark[0], self.color_light_dark[1], 0)
            
                    
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = self.color
        
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = self.color_dark
        self.text_surf = self.font.render(text,True,'white')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
        self.visible = True

    def draw(self):

         if self.visible:
            self.top_rect.y = self.original_y_pos - self.dynamic_elecation
            self.text_rect.center = self.top_rect.center 

            self.bottom_rect.midtop = self.top_rect.midtop
            self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
            
            if self.around:
                pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
                pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
            else:
                pygame.draw.rect(screen,self.bottom_color, self.bottom_rect)
                pygame.draw.rect(screen,self.top_color, self.top_rect)
            screen.blit(self.text_surf, self.text_rect)
            if self.is_button == True:
                dest = self.check_click()
                if dest == 'disc':
                    return 'hell'
                elif dest != None:
                    return dest

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.color_light_dark
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    # ✅ Joue le son de clic
                    try:
                        from audio_manager import audio
                        audio.play_click()
                    except:
                        pass  # Ignore si audio_manager non dispo
                    return self.destination
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.color
        
    def hide(self):
        self.visible = False 

    def show(self):
        self.visible = True

pygame.init()
pygame.font.get_init()

# ✅ Fenêtre sans bordure qui prend tout l'écran
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Détecte la résolution de l'écran
info = pygame.display.Info()
current_w, current_h = info.current_w, info.current_h

# Crée une fenêtre sans bordure en plein écran
screen = pygame.display.set_mode((current_w, current_h), pygame.NOFRAME)
print(f"✅ Fenêtre sans bordure : {current_w}x{current_h}")

clock = pygame.time.Clock()