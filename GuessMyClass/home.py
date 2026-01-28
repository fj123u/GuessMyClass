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

import pygame
from shape_creator import *
from pathlib import Path

play_button = Shape('game', 'Jouer', 370, 140, (current_w/2-185, current_h/2-150), 10, (255, 145, 0), True)

title = Shape(None, 'GMC', (current_w/4-6)*2+6, current_h/6, (current_w/4, 6), 0, (104, 180, 229), False, (resource_path('font/Mighty Souly.ttf'), 150))
button2 = Shape('about', 'À propos', current_w/4-6, current_h/6, (current_w-current_w/4, 6), 2, (104, 208, 229), True, (resource_path('font/Mighty Souly.ttf'), 100))

bottom_bar = Shape(None, 'GMC - 2025', current_w, 35, (0, current_h-35), 0, (104, 208, 229), False, (resource_path('font/Mighty Souly.ttf'), 20), False)

button_list1 = Shape('settings', 'Paramètres', 250, 50, (current_w/2-125, current_h/2+50), 2, (224, 180, 229), True, (resource_path('font/Mighty Souly.ttf'), 40))
button_list2 = Shape('versus', 'Versus', 250, 50, (current_w/2-125, current_h/2+106), 2, (184, 180, 229), True, (resource_path('font/Mighty Souly.ttf'), 40))
button_list3 = Shape('leaderboard', 'Classements', 250, 50, (current_w/2-125, current_h/2+212-50), 2, (144, 180, 229), True, (resource_path('font/Mighty Souly.ttf'), 40))
button_list4 = Shape('leave', 'Quitter', 250, 50, (current_w/2-125, current_h/2+218), 2, (104, 180, 229), True, (resource_path('font/Mighty Souly.ttf'), 40))

infos_left = Shape(None, '', current_w/3, current_h -current_h/6 -60 -35, (current_w/60,30 +current_h/6), 0, (144, 180, 229))
infos_right = Shape(None, '', current_w/3, current_h -current_h/6 -60 -35, (current_w -current_w/3 -current_w/60, 30 +current_h/6), 0, (144, 180, 229))

def home_display(icon):
    screen.fill((205,228,226))
    with open(resource_path("profile/compte.txt"), "r") as f:
        lines = f.readlines()
        f.close()
    ide = ''
    for i in range(len(lines[0])):
        ide = ide + lines[0][i]
    button1 = Shape(None, ide[:-1], current_w/4-12, current_h/6, (6, 6), 0, (104, 208, 229))

    dest = button1.draw()
    if dest != None:
        return dest
    title.draw()

    dest = button2.draw()
    if dest != None:
        return dest

    bottom_bar.draw()

    dest = play_button.draw()
    if dest != None:
        return dest

    #dest = button_list1.draw()
    if dest != None:
        return dest
    dest = button_list2.draw()
    if dest != None:
        return dest
    dest = button_list3.draw()
    if dest != None:
        return dest
    dest = button_list4.draw()
    if dest != None:
        return dest

    infos_left.draw()
    infos_right.draw()
    screen.blit(icon, (current_w-25-5,current_h-25-5))

    return 'home'
