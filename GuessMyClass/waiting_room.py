import sys, os
import pygame
import time
from utils import *
from multiplayer import get_room_info, start_game, leave_room, RoomListener
from sql_link import load_local_profile
import random

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

leave_button_waiting = Shape('multiplayer_menu', '<', 50, 50, (10, 10), 2, (200, 0, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))

room_listener = None
room_data = None
is_host = False
current_room_code = None

def waiting_room_display(room_code, host):
    global room_listener, room_data, is_host, current_room_code
    
    current_room_code = room_code
    is_host = host
    
    room_data = get_room_info(room_code)
    if not room_data:
        return "multiplayer_menu"
    
    title = Shape(None, f'Code: {room_code}', 400, 80, (current_w/2 - 200, 50), 0, (0, 200, 0), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 60))
    
    waiting_text = Shape(None, 'Joueurs dans la partie:', 500, 60, (current_w/2 - 250, 150), 0, (144, 180, 229), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))
    
    player_shapes = []
    y_start = 230
    for i, player in enumerate(room_data["players"]):
        label = f"👑 {player}" if player == room_data["host"] else f"• {player}"
        player_shape = Shape(None, label, 400, 50, (current_w/2 - 200, y_start + i * 60), 0, (184, 180, 229), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 35))
        player_shapes.append(player_shape)
    
    start_button = None
    if is_host:
        start_button = Shape(None, 'Lancer la partie', 300, 70, (current_w/2 - 150, current_h - 150), 3, (0, 200, 0), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))
    
    def on_room_update(payload):
        global room_data
        room_data = payload['new']
    
    if not room_listener:
        room_listener = RoomListener(room_code, on_room_update)
        room_listener.start()
    
    dest = leave_button_waiting.draw()
    if dest:
        if room_listener:
            room_listener.stop()
        leave_room(room_code, load_local_profile())
        return dest
    
    title.draw()
    waiting_text.draw()
    
    for shape in player_shapes:
        shape.draw()
    
    if start_button:
        if start_button.check_click():
            from coordonées_salles import coo
            salles = list(coo.keys())
            first_room = random.choice(salles)
            start_game(room_code, first_room)
            return ('game_multi', room_code)
        start_button.draw()
    
    if room_data and room_data["status"] == "playing":
        return ('game_multi', room_code)
    
    return ("waiting_room", room_code, is_host)