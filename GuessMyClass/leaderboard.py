
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
from sql_link import *
import mysql.connector


b = 3 #number of leaderboards
destination,text,width,height,pos,elevation,color, button=False, font=('GuessMyClass/font/MightySouly.ttf', 80), around=True

leave_button = Shape('home','<', 50, 50, (10, 10), 2, (200, 0, 0), True)

scoreboards = [Shape(None, '', current_w/b -15, current_h-20 -100 -10, (10, 20 +100), 0, (144, 180, 229))]

for i in range(1,b):
    scoreboards.append(Shape(None, '', current_w/b -15, current_h-20 -100 -10, (10*(i) +10 +(current_w/b -10)*i, 20 +100), 0, (144, 180, 229)))
    
    
big_leaderboard = Shape(None, 'Classements', current_w/2 -40 -150, 100, (current_w/2-(current_w/2 -40 -150)/2, 10), 0, (144, 180, 229), False)
best_of_5 = Shape(None, 'Meilleur sur 5', current_w/4, 50, (10 +((current_w/b -15)/2) -(current_w/4)/2, 125), 0, (144, 140, 189), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 35))
best_of_10 = Shape(None, 'Meilleur out of 10', current_w/4, 50, (current_w/2 -current_w/8, 125), 0, (144, 140, 189), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 35))
best_of_20 = Shape(None, 'Meilleur out of 20', current_w/4, 50, (current_w -(current_w/b -15)/2 -5 -(current_w/4)/2, 125), 0, (144, 140, 189), False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 35))

cnx = connect()
a1,a2,a3 = get_leaderboards(cnx)
cnx.close()

if a1 == None and a2 == None and a3 == None:
    connected = False
else:
    connected = True


def leaderboard_display():
    
    dest = leave_button.draw()
    if dest != None:
        pygame.time.delay(300)
        return dest
    
    for i in scoreboards:
        i.draw()
    
    big_leaderboard.draw()
    
    if connected:
        for i in a1:
            i.draw()
        for i in a2:
            i.draw()
        for i in a3:
            i.draw()

        
    best_of_5.draw()
    best_of_10.draw()
    best_of_20.draw()   
    
    return 'leaderboard'