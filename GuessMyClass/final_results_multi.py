import sys, os
import pygame
from shape_creator import *
from utils import *
from multiplayer import get_final_scores

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def final_results_multi_display(room_code):
    leave_button.draw()
    
    title = Shape(None, "Résultats finaux", 500, 80, (current_w/2 - 250, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 60))
    title.draw()
    
    scores = get_final_scores(room_code)
    
    y = 180
    for i, (pseudo, score) in enumerate(scores):
        if i == 0:
            text = f"🏆 {pseudo}: {score} pts"
            color = (255, 215, 0)
        elif i == 1:
            text = f"🥈 {pseudo}: {score} pts"
            color = (192, 192, 192)
        elif i == 2:
            text = f"🥉 {pseudo}: {score} pts"
            color = (205, 127, 50)
        else:
            text = f"{i+1}. {pseudo}: {score} pts"
            color = (184, 180, 229)
        
        score_shape = Shape(None, text, 500, 50, (current_w/2 - 250, y), 0, color, False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
        score_shape.draw()
        y += 60
    
    home_button = Shape('home', 'Retour au menu', 300, 70, (current_w/2 - 150, current_h - 100), 3, (104, 180, 229), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
    dest = home_button.draw()
    if dest:
        return dest
    
    return ('final_results_multi', room_code)