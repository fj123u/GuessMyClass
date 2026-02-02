import pygame
import time
from shape_creator import *
from utils import *
from multiplayer import get_room_info, start_game, leave_room
from sql_link import load_local_profile
import random


leave_button_waiting = Shape('multiplayer_menu', '<', 50, 50, (10, 10), 2, (200, 0, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))

room_data = None
is_host = False
current_room_code = None
last_update_time = 0

def waiting_room_display(room_code, host):
    global room_data, is_host, current_room_code, last_update_time
    
    current_room_code = room_code
    is_host = host
    
    # Met à jour les données toutes les secondes
    current_time = time.time()
    if room_data is None or current_time - last_update_time > 1.0:
        room_data = get_room_info(room_code)
        last_update_time = current_time
        
        if not room_data:
            return "multiplayer_menu"
    
    # Titre avec code
    title = Shape(None, f'Code: {room_code}', 400, 80, (current_w/2 - 200, 50), 0, (0, 200, 0), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 60))
    
    waiting_text = Shape(None, 'Joueurs dans la partie:', 500, 60, (current_w/2 - 250, 150), 0, (144, 180, 229), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))
    
    # Liste des joueurs
    player_shapes = []
    y_start = 230
    for i, player in enumerate(room_data["players"]):
        label = f"👑 {player}" if player == room_data["host"] else f"• {player}"
        player_shape = Shape(None, label, 400, 50, (current_w/2 - 200, y_start + i * 60), 0, (184, 180, 229), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 35))
        player_shapes.append(player_shape)
    
    # Bouton start pour l'hôte
    start_button = None
    if is_host and len(room_data["players"]) >= 1:
        start_button = Shape('start_game', 'Lancer la partie', 300, 70, (current_w/2 - 150, current_h - 150), 3, (0, 200, 0), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))
    
    # Dessine tout
    dest = leave_button_waiting.draw()
    if dest:
        leave_room(room_code, load_local_profile())
        return dest
    
    title.draw()
    waiting_text.draw()
    
    for shape in player_shapes:
        shape.draw()
    
    if start_button:
        dest = start_button.draw()
        if dest == 'start_game':
            from coordonées_salles import coo
            salles = list(coo.keys())
            first_room = random.choice(salles)
            start_game(room_code, first_room)
            pygame.time.delay(500)
            return ('game_multi', room_code)
    
    # Vérifie si la partie a commencé (pour les non-hôtes)
    if room_data["status"] == "playing":
        return ('game_multi', room_code)
    
    return ("waiting_room", room_code, is_host)