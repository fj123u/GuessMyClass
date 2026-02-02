import sys, os
import pygame
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

def create_room_screen_display():
    dest = leave_button_create.draw()
    if dest:
        return dest
    
    title_create.draw()
    game_question.draw()
    
    pseudo = load_local_profile()
    
    dest = nb_5.draw()
    if dest == '5':
        print("Création partie 5 manches")
        room_code = create_room(pseudo, 5)
        if room_code:
            print(f"Room créée: {room_code}")
            pygame.time.delay(300)
            return ('waiting_room', room_code, True)
        else:
            print("Erreur création room")
    
    dest = nb_10.draw()
    if dest == '10':
        print("Création partie 10 manches")
        room_code = create_room(pseudo, 10)
        if room_code:
            print(f"Room créée: {room_code}")
            pygame.time.delay(300)
            return ('waiting_room', room_code, True)
        else:
            print("Erreur création room")
    
    dest = nb_20.draw()
    if dest == '20':
        print("Création partie 20 manches")
        room_code = create_room(pseudo, 20)
        if room_code:
            print(f"Room créée: {room_code}")
            pygame.time.delay(300)
            return ('waiting_room', room_code, True)
        else:
            print("Erreur création room")
    
    return "create_room_screen"