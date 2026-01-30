
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import pygame
from shape_creator import *
from home import *
from about import *
from log_in import *
from game import *
from welcome import *
from utils import *

pygame.init()

current_w, current_h = pygame.display.Info().current_w, pygame.display.Info().current_h

font = pygame.font.Font(resource_path('GuessMyClass/font/MightySouly.ttf'), 80)

screen = pygame.display.set_mode((current_w, current_h))
clock = pygame.time.Clock()
running = True

icon = pygame.image.load(resource_path('GuessMyClass/icon/gmc.png'))
pygame.display.set_icon(icon)
icon = pygame.transform.scale(icon, (25, 25))

dest = 'welcome'
mult = None
l = False
v = False
o = False
a = False
mail_text = ''


# Fonction qui fait une ombre
def shade():
    s = pygame.Surface((current_w, current_h))
    s.set_alpha(175)
    s.fill((255, 255, 255))
    screen.blit(s, (0, 0))

# Programme principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#CDE4E2")

    if dest in ['home', 'leave', 'versus', 'account']:
        with open(resource_path("GuessMyClass/score/option.txt"), "w") as f:
            f.write('False')
            f.close()

        if dest == 'leave':
            l = True
        elif dest == 'versus':
            v = True

        dest = home_display(icon)

        if dest == 'account':
            if not a:
                a = True
            else:
                a = False
                sig = False
                log = False
                s = False

        if l:
            shade()
            popup_leave.draw()
            dest = popup_yes.draw()
            if dest != 'hell':
                dest = popup_no.draw()
            if dest is None:
                dest = 'home'
            elif dest == 'paradise':
                l = False
                dest = 'home'

        if v:
            shade()
            dest = leave_button.draw()
            if dest == 'home':
                v = False
            dest = popup_versus1.draw()
            if dest is None:
                dest = 'home'
            elif dest == 'versus_friend':
                o = True

            if dest is None:
                dest = 'home'
            if o:
                with open(resource_path("GuessMyClass/score/option.txt"), "w") as f:
                    f.write('True')
                    f.close()
                game_display()
                dest = 'game'
                o = False
                v = False
            elif dest == 'versus_random':
                v = False

        if a:
            dest = log_in_main.draw()
            if dest is None:
                dest = 'home'
            if s:
                a = False

    elif dest == 'leaderboard':
        from leaderboard import *
        dest = leaderboard_display()
    elif dest == 'about':
        dest = about_display()
    elif dest == 'hell':
        running = False
    elif dest == 'game':
        dest = game_display()
    elif dest == 'log_in':
        log_in_display()
        dest = 'home'
    elif dest == "welcome":
        dest = welcome_display()
        if dest is None:
            dest = "welcome"

    pygame.display.flip()
    clock.tick(3600)

pygame.quit()
