import sys, os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_score_options_path():
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    full_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "score", "options.txt")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path

import mysql.connector
import pygame
from pathlib import Path
from home import *
from about import *
from log_in import *
from game import *
from welcome import *

pygame.init()

current_w, current_h = pygame.display.Info().current_w, pygame.display.Info().current_h

font = pygame.font.Font(resource_path('GuessMyClass/font/MightySouly.ttf'), 80)

screen = pygame.display.set_mode((current_w, current_h))
clock = pygame.time.Clock()
running = True



icon = pygame.image.load(resource_path('icon/Logo PJB.png'))
pygame.display.set_icon(icon)
icon = pygame.transform.scale(icon, (25, 25))

dest = 'welcome'
mult = None
l = False
v = False
o = False
a = False
s = False
mail_text = ''

popup_leave = Shape(None, 'Êtes-vous sûr de vouloir quitter ?', current_w/4 + 100, 100, (current_w/2 - (current_w/4)/2 - 50, current_h/2 - 50), 0, (104, 180, 229), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
popup_yes = Shape('hell', 'Oui', current_w/20, 50, (current_w/2 - 125, current_h/2 + 100), 2, (0, 180, 0), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
popup_no = Shape('paradise', 'Non', current_w/20, 50, (current_w/2 - 125 + 250 - (current_w/20), current_h/2 + 100), 2, (180, 0, 0), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
popup_versus1 = Shape('versus_friend', 'Versus friend', 350, 350, (current_w/2 - 175, current_h/2 - 175), 3, (184, 180, 229), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 50))
log_in = Shape('log_in', 'Changer de pseudo', 350, 50, (6, current_h/6 + 6 + 5 + 55), 2, (184, 180, 229), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

def reset(db=False):
    print('r')

def shade():
    s = pygame.Surface((current_w, current_h))
    s.set_alpha(175)
    s.fill((255, 255, 255))
    screen.blit(s, (0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#CDE4E2")

    if dest in ['home', 'leave', 'versus', 'account']:
        with open(resource_path("score/option.txt"), "w") as f:
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
                print('hellyeah')
                with open(resource_path("score/option.txt"), "w") as f:
                    f.write('True')
                    f.close()
                game_display()
                dest = 'game'
                o = False
                v = False
            elif dest == 'versus_random':
                v = False

        if a:
            dest = sign_in.draw()
            if dest == 'sign_in':
                s = True
            dest = log_in.draw()
            if dest is None:
                dest = 'home'
            if s:
                dest = 'sign_in'
                a = False
                s = False

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
