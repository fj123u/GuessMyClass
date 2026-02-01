# Importe les bibliothèques nécessaires pour le fonctionnement du code
import pygame
from shape_creator import *
from home import *
from about import *
from log_in import *
from game import *
from welcome import *
from utils import *
from multiplayer_menu import multiplayer_menu_display
from create_room_screen import create_room_screen_display
from join_room_screen import join_room_screen_display
from waiting_room import waiting_room_display

pygame.init()
current_w, current_h = pygame.display.Info().current_w, pygame.display.Info().current_h
font = pygame.font.Font(resource_path('GuessMyClass/font/MightySouly.ttf'), 80)
screen = pygame.display.set_mode((current_w, current_h))
clock = pygame.time.Clock()

running = True
icon = pygame.image.load(resource_path('GuessMyClass/icon/gmc.png'))
pygame.display.set_icon(icon)
icon = pygame.transform.scale(icon, (25, 25))

dest = 'welcome'
mult = None
l = False
v = False
o = False
a = False
mail_text = ''
room_code = None
is_host = False

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
        with open(resource_path("GuessMyClass/score/option.txt"), "w") as f:
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
                with open(resource_path("GuessMyClass/score/option.txt"), "w") as f:
                    f.write('True')
                    f.close()
                game_display()
                dest = 'game'
                o = False
                v = False
            elif dest == 'versus_random':
                v = False
        if a:
            dest = log_in_main.draw()
            if dest is None:
                dest = 'home'
            if s:
                a = False
    
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
    
    elif dest == "multiplayer_menu":
        dest = multiplayer_menu_display()
    
    elif dest == "create_room_screen":
        result = create_room_screen_display()
        if isinstance(result, tuple):
            dest, room_code, is_host = result
        else:
            dest = result
    
    elif dest == "join_room_screen":
        result = join_room_screen_display()
        if isinstance(result, tuple):
            dest, room_code, is_host = result
        else:
            dest = result
    
    elif dest == "waiting_room":
        result = waiting_room_display(room_code, is_host)
        if isinstance(result, tuple):
            dest = result[0]
            if len(result) > 1:
                room_code = result[1]
            if len(result) > 2:
                is_host = result[2]
        else:
            dest = result
    
    elif dest == "game_multi":
        from game_multi import game_multi_display
        result = game_multi_display(room_code)
        if isinstance(result, tuple):
            dest = result[0]
            if len(result) > 1:
                room_code = result[1]
        else:
            dest = result
    
    elif dest == "final_results_multi":
        from final_results_multi import final_results_multi_display
        result = final_results_multi_display(room_code)
        if isinstance(result, tuple):
            dest = result[0]
        else:
            dest = result
    
    pygame.display.flip()
    clock.tick(3600)

pygame.quit()