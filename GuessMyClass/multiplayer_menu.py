import sys, os
import pygame
from utils import *
from multiplayer import create_room, join_room
from sql_link import load_local_profile

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

leave_button_multi = Shape('home', '<', 50, 50, (10, 10), 2, (200, 0, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))

title_multi = Shape(None, 'Mode Multijoueur', current_w/2 - 300, 100, (current_w/2 - 300, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 80))

create_room_button = Shape('create_room_screen', 'Créer une partie', 350, 80, (current_w/2 - 175, current_h/2 - 60), 3, (104, 208, 229), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 50))

join_room_button = Shape('join_room_screen', 'Rejoindre une partie', 350, 80, (current_w/2 - 175, current_h/2 + 60), 3, (184, 180, 229), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 50))

def multiplayer_menu_display():
    dest = leave_button_multi.draw()
    if dest:
        return dest
    
    title_multi.draw()
    
    dest = create_room_button.draw()
    if dest:
        return dest
    
    dest = join_room_button.draw()
    if dest:
        return dest
    
    return "multiplayer_menu"