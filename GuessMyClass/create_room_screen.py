import sys, os
import pygame
import customtkinter as ctk
from utils import *
from multiplayer import create_room
from sql_link import load_local_profile

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

leave_button_create = Shape('multiplayer_menu', '<', 50, 50, (10, 10), 2, (200, 0, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))

title_create = Shape(None, 'Créer une partie', current_w/2 - 300, 100, (current_w/2 - 300, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 80))

mode_5_button = Shape(None, "5 manches", 150, 60, (current_w/2 - 250, current_h/2), 2, (255, 128, 0), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 35))
mode_10_button = Shape(None, "10 manches", 150, 60, (current_w/2 - 75, current_h/2), 2, (255, 128, 0), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 35))
mode_20_button = Shape(None, "20 manches", 150, 60, (current_w/2 + 100, current_h/2), 2, (255, 128, 0), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 35))

room_code_display = None
waiting_text = None

def create_room_screen_display():
    global room_code_display, waiting_text
    
    dest = leave_button_create.draw()
    if dest:
        return dest
    
    title_create.draw()
    
    pseudo = load_local_profile()
    
    if mode_5_button.check_click():
        room_code = create_room(pseudo, 5)
        if room_code:
            room_code_display = Shape(None, f'Code: {room_code}', 400, 80, (current_w/2 - 200, current_h/2 + 100), 0, (0, 200, 0), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 50))
            waiting_text = Shape(None, 'En attente de joueurs...', 500, 60, (current_w/2 - 250, current_h/2 + 200), 0, (144, 180, 229), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 35))
            return ('waiting_room', room_code, True)
    
    if mode_10_button.check_click():
        room_code = create_room(pseudo, 10)
        if room_code:
            return ('waiting_room', room_code, True)
    
    if mode_20_button.check_click():
        room_code = create_room(pseudo, 20)
        if room_code:
            return ('waiting_room', room_code, True)
    
    mode_5_button.draw()
    mode_10_button.draw()
    mode_20_button.draw()
    
    if room_code_display:
        room_code_display.draw()
    if waiting_text:
        waiting_text.draw()
    
    return "create_room_screen"