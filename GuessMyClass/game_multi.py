import sys, os
import pygame
import random
import time
from math import sqrt, exp
from shape_creator import *
from utils import *
from multiplayer import get_room_info, submit_answer, get_round_results, next_round, finish_game
from sql_link import load_local_profile
from coordonées_salles import coo

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

current_room_code = None
current_round = 0
total_rounds = 0
current_salle = None
player_answered = False
pin_position = None
current_etage = 0
show_results = False
results_data = []
last_update_time = 0

def calcul_points(salle, coo_pin, nb_etage):
    distance = sqrt((coo_pin[0] - coo[salle][0])**2 + (coo_pin[1] - coo[salle][1])**2)
    
    if distance <= 10:
        score = 5000
    elif distance <= 300:
        lambda_ = 0.015
        score = 5000 * exp(-lambda_ * distance)
        score = max(score, 500)
    else:
        score = 500 - ((distance - 300) / 700) * 450
        score = max(score, 50)
    
    if nb_etage != coo[salle][2]:
        score *= 0.25
    
    return round(score)

def init_game(room_code):
    global current_room_code, current_round, total_rounds, current_salle, player_answered, show_results
    
    current_room_code = room_code
    room = get_room_info(room_code)
    
    if not room:
        return False
    
    total_rounds = room["mode"]
    current_round = room["current_round"]
    current_salle = room["current_room"]
    player_answered = False
    show_results = False
    
    return True

def game_multi_display(room_code):
    global current_round, current_salle, player_answered, pin_position, current_etage, show_results, results_data, last_update_time
    
    if current_round == 0:
        if not init_game(room_code):
            return "multiplayer_menu"
    
    # Met à jour les infos de la room régulièrement
    current_time = time.time()
    if current_time - last_update_time > 1.0:
        room = get_room_info(room_code)
        if room:
            if room["current_round"] > current_round:
                reset_round()
                current_round = room["current_round"]
                current_salle = room["current_room"]
            
            if room["status"] == "finished":
                return ('final_results_multi', room_code)
        last_update_time = current_time
    
    leave_button.draw()
    
    question_text = Shape(None, f"Où est la salle {current_salle} ?", current_w/2 - 300, 80, (current_w/2 - 300, 50), 0, (220, 0, 0), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))
    question_text.draw()
    
    round_text = Shape(None, f"Manche {current_round}/{total_rounds}", 200, 50, (current_w - 220, 20), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 30))
    round_text.draw()
    
    map_img = pygame.image.load(resource_path(f'GuessMyClass/img/plan_{current_etage}.png'))
    map_rect = map_img.get_rect(center=(current_w/2, current_h/2 + 50))
    screen.blit(map_img, map_rect)
    
    if pin_position:
        pygame.draw.circle(screen, (255, 0, 0), pin_position, 10)
    
    if pygame.mouse.get_pressed()[0] and not player_answered and not show_results:
        mouse_pos = pygame.mouse.get_pos()
        if map_rect.collidepoint(mouse_pos):
            pin_position = mouse_pos
    
    etage_button = Shape(None, f"Étage: {current_etage}", 150, 60, (current_w - 170, current_h - 80), 2, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 30))
    dest = etage_button.draw()
    if dest:
        current_etage = 1 - current_etage
        pygame.time.delay(200)
    
    valider_button = Shape('valider_multi', "Valider", 150, 60, (current_w - 340, current_h - 80), 3, (0, 220, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
    
    if not player_answered and not show_results:
        dest = valider_button.draw()
        if dest == 'valider_multi' and pin_position:
            score = calcul_points(current_salle, pin_position, current_etage)
            pseudo = load_local_profile()
            submit_answer(current_room_code, current_round, pseudo, pin_position[0], pin_position[1], current_etage, score)
            player_answered = True
            pygame.time.delay(300)
    
    if player_answered:
        waiting_text = Shape(None, "En attente des autres joueurs...", 500, 60, (current_w/2 - 250, current_h - 100), 0, (255, 165, 0), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 30))
        waiting_text.draw()
        
        results_data = get_round_results(current_room_code, current_round)
        room = get_room_info(current_room_code)
        
        if len(results_data) >= len(room["players"]):
            show_results = True
    
    if show_results:
        display_results()
        
        next_button = Shape('next_multi', "Suivant", 200, 60, (current_w/2 - 100, current_h - 80), 3, (0, 200, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
        
        room = get_room_info(current_room_code)
        is_host = room["host"] == load_local_profile()
        
        if is_host:
            dest = next_button.draw()
            if dest == 'next_multi':
                if current_round < total_rounds:
                    salles_list = list(coo.keys())
                    new_salle = random.choice(salles_list)
                    next_round(current_room_code, new_salle)
                    pygame.time.delay(500)
                else:
                    finish_game(current_room_code)
                    return ('final_results_multi', current_room_code)
        else:
            waiting_host_text = Shape(None, "En attente de l'hôte...", 400, 50, (current_w/2 - 200, current_h - 80), 0, (255, 165, 0), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 30))
            waiting_host_text.draw()
    
    return ('game_multi', room_code)

def display_results():
    y = 200
    title = Shape(None, "Résultats de la manche", 400, 60, (current_w/2 - 200, 130), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))
    title.draw()
    
    sorted_results = sorted(results_data, key=lambda x: x['score'], reverse=True)
    
    for i, result in enumerate(sorted_results[:5]):
        text = f"{i+1}. {result['pseudo']}: {result['score']} pts"
        color = (0, 200, 0) if i == 0 else (184, 180, 229)
        result_shape = Shape(None, text, 400, 45, (current_w/2 - 200, y), 0, color, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
        result_shape.draw()
        y += 50

def reset_round():
    global player_answered, pin_position, show_results, results_data
    player_answered = False
    pin_position = None
    show_results = False
    results_data = []