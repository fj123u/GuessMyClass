import sys, os
import pygame
import random
import time
from math import sqrt, exp
from shape_creator import *
from utils import *
from multiplayer import (get_room_info, submit_answer, get_round_results, next_round, finish_game,
                         create_game_session, save_round_detail, is_player_guest)
from sql_link import load_local_profile
from coordonées_salles import coo

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

last_point = None
C000 = ["GuessMyClass/img/C000/C006.webp", "GuessMyClass/img/C000/C008.webp", "GuessMyClass/img/C000/C012.webp", "GuessMyClass/img/C000/C009.webp", "GuessMyClass/img/C000/C005.webp"]
C100 = ["GuessMyClass/img/C100/C106.webp", "GuessMyClass/img/C100/C108.webp", "GuessMyClass/img/C100/C105.webp", "GuessMyClass/img/C100/C111.webp", "GuessMyClass/img/C100/C114.webp", "GuessMyClass/img/C100/C117.webp", "GuessMyClass/img/C100/C104.webp", "GuessMyClass/img/C100/C109.webp", "GuessMyClass/img/C100/C110.webp", "GuessMyClass/img/C100/C113.webp", "GuessMyClass/img/C100/C115.webp"]
D000 = ["GuessMyClass/img/D000/D004.webp", "GuessMyClass/img/D000/D010.webp", "GuessMyClass/img/D000/D012_v2.webp", "GuessMyClass/img/D000/D014.webp", "GuessMyClass/img/D000/Escalier D.webp", "GuessMyClass/img/D000/D006.webp"]
D100 = ["GuessMyClass/img/D100/D104.webp", "GuessMyClass/img/D100/D105.webp", "GuessMyClass/img/D100/D106.webp", "GuessMyClass/img/D100/D109.webp", "GuessMyClass/img/D100/D110.webp", "GuessMyClass/img/D100/couloir D haut.webp", "GuessMyClass/img/D100/D111.webp", "GuessMyClass/img/D100/D113.webp", "GuessMyClass/img/D100/D114.webp", "GuessMyClass/img/D100/D117.webp", "GuessMyClass/img/D100/D116.webp", "GuessMyClass/img/D100/D115.webp", "GuessMyClass/img/D100/D112.webp"]
special = ["GuessMyClass/img/special/(parking).webp", "GuessMyClass/img/special/4_arbres.webp", "GuessMyClass/img/special/biathlon.webp", "GuessMyClass/img/special/briques.webp", "GuessMyClass/img/special/cdi.webp", "GuessMyClass/img/special/cours_dehors.webp", "GuessMyClass/img/special/cours_internat.webp", "GuessMyClass/img/special/creux.webp", "GuessMyClass/img/special/dehors_physique.webp", "GuessMyClass/img/special/hall.webp", "GuessMyClass/img/special/petit_arbre.webp", "GuessMyClass/img/special/terrain_foot.webp", "GuessMyClass/img/special/couloir CDI.webp", "GuessMyClass/img/special/couloir salle prof.webp", "GuessMyClass/img/special/escalier E.webp", "GuessMyClass/img/special/Grande passerelle.webp", "GuessMyClass/img/special/Passerelle_D-C_bas.webp", "GuessMyClass/img/special/Passerelle_D-C.webp", "GuessMyClass/img/special/Passerelle_E-D_bas.webp", "GuessMyClass/img/special/Passerelle_E-D.webp"]
toilettes = ["GuessMyClass/img/toilettes/toilettes hall garçon.webp", "GuessMyClass/img/toilettes/toilette haut interieur.webp", "GuessMyClass/img/toilettes/vestiaire.webp"]
A100 = ["GuessMyClass/img/A100/A136.webp", "GuessMyClass/img/A100/A137.webp", "GuessMyClass/img/A100/A138.webp", "GuessMyClass/img/A100/A139.webp"]
E000 = ["GuessMyClass/img/E000/Beton.webp", "GuessMyClass/img/E000/bois.webp", "GuessMyClass/img/E000/couloir E bas.webp", "GuessMyClass/img/E000/E030.webp", "GuessMyClass/img/E000/Energie.webp", "GuessMyClass/img/E000/peinture.webp", "GuessMyClass/img/E000/E041.webp"]
E100 = ["GuessMyClass/img/E100/couloir E haut.webp", "GuessMyClass/img/E100/E116.webp", "GuessMyClass/img/E100/E108.webp", "GuessMyClass/img/E100/E110.webp", "GuessMyClass/img/E100/E113.webp", "GuessMyClass/img/E100/E123.webp", "GuessMyClass/img/E100/E125.webp", "GuessMyClass/img/E100/E107.webp", "GuessMyClass/img/E100/E109.webp", "GuessMyClass/img/E100/E111.webp", "GuessMyClass/img/E100/E114.webp", "GuessMyClass/img/E100/E121.webp", "GuessMyClass/img/E100/E126.webp"]

tout = [C000, C100, D100, D000, special, toilettes, A100, E000, E100]

class PanoramicView:
    def __init__(self, image_path, screen):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.image_width, self.image_height = self.image.get_size()
        self.view_width, self.view_height = screen.get_size()
        self.x_offset = 0
        self.y_offset = -(self.image_height // 2 - self.view_height // 2)
        self.dragging = False
        self.last_mouse_pos = (0, 0)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.dragging = True
            self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            dx, dy = event.pos[0] - self.last_mouse_pos[0], event.pos[1] - self.last_mouse_pos[1]
            self.x_offset -= dx 
            self.y_offset = max(-(self.image_height - self.view_height), min(0, self.y_offset + dy))
            self.last_mouse_pos = event.pos

    def draw(self):
        x = self.x_offset % self.image_width 
        self.screen.blit(self.image, (-x, self.y_offset))
        if x > 0:
            self.screen.blit(self.image, (-x + self.image_width, self.y_offset))

def get_image_for_room(room_name):
    for liste in tout:
        for img_path in liste:
            if room_name in img_path:
                return img_path
    return None

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
    
    return round(score), distance

def draw_points(point):
    if point and point != (0, 0):
        pygame.draw.circle(screen, (255, 0, 0), point, 10)

def draw_points3(last_point3):
    if last_point3:
        pygame.draw.circle(screen, (0, 0, 255), last_point3, 10)

def show_answer(salle, coo_pin):
    draw_points3((coo[salle][0], coo[salle][1]))
    draw_points(coo_pin)
    if coo_pin != (0, 0):
        pygame.draw.line(screen, (0, 0, 0), coo_pin, (coo[salle][0], coo[salle][1]), width=3)

def wait_with_events(milliseconds):
    """Attend X ms en gérant les événements QUIT"""
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < milliseconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True  # Signal pour quitter
        clock.tick(60)
    return False

def game_multi_display(room_code):
    global last_point
    
    room_data = get_room_info(room_code)
    if not room_data:
        return "multiplayer_menu"
    
    nb = room_data["mode"]
    total_players = len(room_data["players"])
    session_id = create_game_session(room_code, nb, total_players)
    start_time = time.time()
    
    current_round = room_data["current_round"]
    total_rounds = nb
    
    score = 0
    map_image_coo = (75, 75)
    etage_image_coo = (75, 75)
    path_plan = resource_path("GuessMyClass/img/plan/etage_0.png")
    pseudo = load_local_profile()
    is_host = room_data["host"] == pseudo
    last_update = time.time()
    
    for round_num in range(current_round, nb + 1):
        room_data = get_room_info(room_code)
        if not room_data or room_data["status"] == "finished":
            break
        
        salle = room_data["current_room"]
        choose = get_image_for_room(salle)
        
        if not choose:
            continue
        
        round_start_time = time.time()
        
        pano_view = PanoramicView(resource_path(choose), screen)
        map_image = pygame.image.load(path_plan)
        map_image = pygame.transform.scale(map_image, (current_w, current_h))
        timer = 30
        nb_etage = 0
        map_open = False
        map_block = False
        valider_pressed = False
        etage_pressed = False
        running = True
        clickable = False
        player_has_answered = False
        
        map_icon = pygame.image.load(resource_path('GuessMyClass/icon/map.png'))
        map_icon = pygame.transform.scale(map_icon, map_image_coo)
        
        etage_icon = pygame.image.load(resource_path('GuessMyClass/icon/fleche haut.png'))
        etage_icon = pygame.transform.scale(etage_icon, etage_image_coo)
        etage_icon2 = pygame.image.load(resource_path('GuessMyClass/icon/fleche bas.png'))
        etage_icon2 = pygame.transform.scale(etage_icon2, etage_image_coo)
        
        scoreButtonWidth = 200
        scoreButtonHeight = 50
        scoreButtonPos = (current_w - 200 - 25, 20)
        scoreButtonElevation = 5
        scoreButtonColor = (220, 0, 0)
        score_button = Shape('score', "Score : " + str(score), scoreButtonWidth, scoreButtonHeight, scoreButtonPos, scoreButtonElevation, scoreButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
        
        roundButtonWidth = 200
        roundButtonHeight = 50
        roundButtonPos = (current_w - 200 - 25, 80)
        roundButtonElevation = 5
        roundButtonColor = (104, 180, 229)
        round_button = Shape('round', f"Manche {round_num}/{total_rounds}", roundButtonWidth, roundButtonHeight, roundButtonPos, roundButtonElevation, roundButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
        
        timerButtonWidth = 150
        timerButtonHeight = 50
        timerButtonPos = (current_w/2 - 75, 20)
        timerButtonElevation = 5
        timerButtonColor = (220, 0, 0)
        
        last_point = (0, 0)
        liste_points = [(0, 0)]
        show_ui = True  # Flag pour afficher/cacher les UI elements
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'hell'
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    if 20 <= x <= 140 and 20 <= y <= 70 and clickable == False: 
                        pygame.time.delay(300)
                        return 'multiplayer_menu'
                    if current_w - 120 <= x <= current_w - 20 and current_h - 120 <= y <= current_h - 20 and map_block == False:
                        clickable = not clickable
                        map_open = not map_open 
                    if current_w - 225 <= x <= current_w - 120 and current_h - 120 <= y <= current_h - 20 and clickable == True:
                        valider_pressed = not valider_pressed
                    if current_w - 106 <= x <= current_w - 6 and current_h - 218 <= y <= current_h - 118 and clickable == True:
                        if nb_etage == 1:
                            path_plan = resource_path("GuessMyClass/img/plan/etage_0.png")
                            map_image = pygame.image.load(path_plan)
                            map_image = pygame.transform.scale(map_image, (current_w, current_h))
                        elif nb_etage == 0:
                            path_plan = resource_path("GuessMyClass/img/plan/etage_1.png")
                            map_image = pygame.image.load(path_plan)
                            map_image = pygame.transform.scale(map_image, (current_w, current_h))
                        etage_pressed = True
                    else:
                        if map_open == True:
                            if current_w - 120 <= x <= current_w - 20 and current_h - 120 <= y <= current_h - 20:
                                pass
                            else:
                                last_point = pygame.mouse.get_pos()  
                                x, y = last_point                          
                                liste_points.append(last_point)
                
                pano_view.handle_event(event)
            
            screen.fill((0, 0, 0))
            
            if map_open:
                if nb_etage == 0:
                    leave_button.hide()
                    screen.blit(map_image, (screen.get_width() // 2 - map_image.get_width() // 2, screen.get_height() // 2 - map_image.get_height() // 2))
                    draw_points(last_point)
                    game_valider.draw()
                    game_etage.draw()
                    screen.blit(etage_icon, (current_w - 75 - 17, current_h - 75 - 132))
                    
                    if valider_pressed and not player_has_answered:
                        if len(liste_points) >= 2:
                            round_time_taken = int(time.time() - round_start_time)
                            score2, distance = calcul_points(salle, liste_points[-2], nb_etage)
                            score += score2
                            
                            submit_answer(room_code, round_num, pseudo, liste_points[-2][0], liste_points[-2][1], nb_etage, score2)
                            
                            if session_id:
                                save_round_detail(session_id, round_num, salle, pseudo, 
                                                liste_points[-2][0], liste_points[-2][1], nb_etage, 
                                                score2, distance, round_time_taken)
                            
                            player_has_answered = True
                            valider_pressed = False
                            
                            score_button = Shape('score', "Score : " + str(score), scoreButtonWidth, scoreButtonHeight, scoreButtonPos, scoreButtonElevation, scoreButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                    
                    elif etage_pressed:
                        etage_pressed = False
                        nb_etage = 1
                else:
                    leave_button.hide()
                    screen.blit(map_image, (screen.get_width() // 2 - map_image.get_width() // 2, screen.get_height() // 2 - map_image.get_height() // 2))
                    draw_points(last_point)
                    game_valider.draw()
                    game_etage.draw()
                    screen.blit(etage_icon2, (current_w - 75 - 17, current_h - 75 - 132))
                    
                    if valider_pressed and not player_has_answered:
                        if len(liste_points) >= 2:
                            round_time_taken = int(time.time() - round_start_time)
                            score2, distance = calcul_points(salle, liste_points[-2], nb_etage)
                            score += score2
                            
                            submit_answer(room_code, round_num, pseudo, liste_points[-2][0], liste_points[-2][1], nb_etage, score2)
                            
                            if session_id:
                                save_round_detail(session_id, round_num, salle, pseudo, 
                                                liste_points[-2][0], liste_points[-2][1], nb_etage, 
                                                score2, distance, round_time_taken)
                            
                            player_has_answered = True
                            valider_pressed = False
                            
                            score_button = Shape('score', "Score : " + str(score), scoreButtonWidth, scoreButtonHeight, scoreButtonPos, scoreButtonElevation, scoreButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                    
                    elif etage_pressed:
                        etage_pressed = False
                        nb_etage = 0
                
                if player_has_answered:
                    waiting_text = Shape(None, "En attente des autres joueurs...", 500, 60, (current_w/2 - 250, current_h - 150), 0, (255, 165, 0), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 30))
                    waiting_text.draw()
                    
                    if time.time() - last_update > 1.0:
                        results = get_round_results(room_code, round_num)
                        room_data = get_room_info(room_code)
                        
                        if len(results) >= len(room_data["players"]):
                            sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
                            
                            # CACHER les UI IMMÉDIATEMENT
                            show_ui = False
                            
                            # SORTIR de la boucle AVANT d'afficher
                            running = False
                            
                            # ÉTAPE 1: Affiche solution directement (pas de wait)
                            screen.fill((0, 0, 0))
                            map_image_reload = pygame.image.load(path_plan)
                            map_image_reload = pygame.transform.scale(map_image_reload, (current_w, current_h))
                            screen.blit(map_image_reload, (screen.get_width() // 2 - map_image_reload.get_width() // 2, screen.get_height() // 2 - map_image_reload.get_height() // 2))
                            
                            for res in sorted_results:
                                draw_points((res['x'], res['y']))
                            
                            show_answer(salle, liste_points[-2] if len(liste_points) >= 2 else (0, 0))
                            pygame.display.flip()
                            
                            # Attend 4s en gérant les événements
                            if wait_with_events(4000):
                                return 'hell'
                            
                            # ÉTAPE 2: Affiche résultats
                            screen.fill("#CDE4E2")
                            results_title = Shape(None, "Résultats de la manche", 500, 60, (current_w/2 - 250, 50), 0, (104, 180, 229), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))
                            results_title.draw()
                            
                            y = 130
                            for i, res in enumerate(sorted_results):
                                color = (0, 200, 0) if i == 0 else (184, 180, 229)
                                result_text = Shape(None, f"{i+1}. {res['pseudo']}: {res['score']} pts", 400, 45, (current_w/2 - 200, y), 0, color, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                                result_text.draw()
                                y += 50
                            
                            pygame.display.flip()
                            
                            # Attend 5s en gérant les événements
                            if wait_with_events(2000):
                                return 'hell'
                            
                            if is_host:
                                if round_num < total_rounds:
                                    salles = list(coo.keys())
                                    new_salle = random.choice(salles)
                                    next_round(room_code, new_salle)
                                else:
                                    finish_game(room_code)
                            
                            nb_etage = 0
                            path_plan = resource_path("GuessMyClass/img/plan/etage_0.png")
                            map_image = pygame.image.load(path_plan)
                            map_image = pygame.transform.scale(map_image, (current_w, current_h))
                        
                        last_update = time.time()
            else:
                leave_button.show()
                pano_view.draw()
            
            # Ces shapes NE S'AFFICHENT QUE si show_ui est True
            if show_ui:
                leave_button.draw()
                score_button.draw()
                round_button.draw()
                game_map.draw()
                screen.blit(map_icon, (current_w - 75 - 17, current_h - 75 - 22))
                
                if timer > 0:
                    timer -= 0.015
                if timer <= 0:
                    map_open = True
                    map_block = True
                    clickable = True
                
                timer_button = Shape('timer', "Temps : " + str(round(timer)) + "s", timerButtonWidth, timerButtonHeight, timerButtonPos, timerButtonElevation, timerButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                timer_button.draw()
            
            pygame.display.flip()
            clock.tick(60)

        if not is_host:
            waiting_start = time.time()
            while True:
                screen.fill("#CDE4E2")
                waiting_text = Shape(None, "En attente de la manche suivante...", 600, 80, (current_w/2 - 300, current_h/2 - 40), 0, (255, 165, 0), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))
                waiting_text.draw()
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'hell'
                
                room_data = get_room_info(room_code)
                if not room_data:
                    return "multiplayer_menu"
                                
                if room_data["current_round"] > round_num:
                    break
                
                if room_data["status"] == "finished":
                    break
                
                if time.time() - waiting_start > 60:
                    return "multiplayer_menu"
                
                clock.tick(2)
        else:
            pygame.time.delay(2000)

        room_data = get_room_info(room_code)
        if room_data["status"] == "finished":
            break
    
    # IMPORTANT: Réaffiche le leave_button avant de sortir
    leave_button.show()
    
    return ('final_results_multi', room_code, session_id, start_time)