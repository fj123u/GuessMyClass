
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import pygame
from shape_creator import *
from log_in import *
from utils import *

# Boucle principale du jeu
def welcome_display(): 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if log_in_welcome.top_rect.collidepoint(event.pos):
                dest = log_in_display()
                if dest:
                    return dest 
    choix_shape.draw()
    welcome_title.draw()
    log_in_welcome.draw()
    dest = sans_compte.draw()
    if dest is not None:
        with open(resource_path("GuessMyClass/profile/compte.txt"), "w") as f:
            f.write("Invite\ninvit")
            f.close()
        return dest
