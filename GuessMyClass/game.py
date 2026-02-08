
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import pygame
from shape_creator import *
from coordonées_salles import *
from random import *
from time import *
from sql_link import *
from utils import *


# Définition de last_point
last_point = None  
# Définition de liste contenant le chemin de l'image de chaque salle
C000 = ["GuessMyClass/img/C000/C006.webp", "GuessMyClass/img/C000/C008.webp", "GuessMyClass/img/C000/C012.webp", "GuessMyClass/img/C000/C009.webp", "GuessMyClass/img/C000/C005.webp"]
C100 = ["GuessMyClass/img/C100/C106.webp", "GuessMyClass/img/C100/C108.webp", "GuessMyClass/img/C100/C105.webp", "GuessMyClass/img/C100/C111.webp", "GuessMyClass/img/C100/C114.webp", "GuessMyClass/img/C100/C117.webp", "GuessMyClass/img/C100/C104.webp", "GuessMyClass/img/C100/C109.webp", "GuessMyClass/img/C100/C110.webp", "GuessMyClass/img/C100/C113.webp", "GuessMyClass/img/C100/C115.webp"]
D000 = ["GuessMyClass/img/D000/D004.webp", "GuessMyClass/img/D000/D010.webp", "GuessMyClass/img/D000/D012_v2.webp", "GuessMyClass/img/D000/D014.webp", "GuessMyClass/img/D000/Escalier D.webp", "GuessMyClass/img/D000/D006.webp"]
D100 = ["GuessMyClass/img/D100/D104.webp", "GuessMyClass/img/D100/D105.webp", "GuessMyClass/img/D100/D106.webp", "GuessMyClass/img/D100/D109.webp", "GuessMyClass/img/D100/D110.webp", "GuessMyClass/img/D100/couloir D haut.webp", "GuessMyClass/img/D100/D111.webp", "GuessMyClass/img/D100/D113.webp", "GuessMyClass/img/D100/D114.webp", "GuessMyClass/img/D100/D117.webp", "GuessMyClass/img/D100/D116.webp", "GuessMyClass/img/D100/D115.webp", "GuessMyClass/img/D100/D112.webp"]
special = ["GuessMyClass/img/special/(parking).webp", "GuessMyClass/img/special/4_arbres.webp", "GuessMyClass/img/special/biathlon.webp", "GuessMyClass/img/special/briques.webp", "GuessMyClass/img/special/cdi.webp", "GuessMyClass/img/special/cours_dehors.webp", "GuessMyClass/img/special/cours_internat.webp", "GuessMyClass/img/special/creux.webp", "GuessMyClass/img/special/dehors_physique.webp", "GuessMyClass/img/special/hall.webp", "GuessMyClass/img/special/petit_arbre.webp", "GuessMyClass/img/special/terrain_foot.webp", "GuessMyClass/img/special/couloir CDI.webp", "GuessMyClass/img/special/couloir salle prof.webp", "GuessMyClass/img/special/escalier E.webp", "GuessMyClass/img/special/Grande passerelle.webp", "GuessMyClass/img/special/Passerelle_D-C_bas.webp", "GuessMyClass/img/special/Passerelle_D-C.webp", "GuessMyClass/img/special/Passerelle_E-D_bas.webp", "GuessMyClass/img/special/Passerelle_E-D.webp"]
toilettes = ["GuessMyClass/img/toilettes/toilettes hall garçon.webp", "GuessMyClass/img/toilettes/toilette haut interieur.webp", "GuessMyClass/img/toilettes/vestiaire.webp"]
A100 = ["GuessMyClass/img/A100/A136.webp", "GuessMyClass/img/A100/A137.webp", "GuessMyClass/img/A100/A138.webp", "GuessMyClass/img/A100/A139.webp"]
E000 = ["GuessMyClass/img/E000/Beton.webp", "GuessMyClass/img/E000/bois.webp", "GuessMyClass/img/E000/couloir E bas.webp", "GuessMyClass/img/E000/E030.webp", "GuessMyClass/img/E000/Energie.webp", "GuessMyClass/img/E000/peinture.webp", "GuessMyClass/img/E000/E041.webp"]
E100 = ["GuessMyClass/img/E100/couloir E haut.webp", "GuessMyClass/img/E100/E116.webp", "GuessMyClass/img/E100/E108.webp", "GuessMyClass/img/E100/E110.webp", "GuessMyClass/img/E100/E113.webp", "GuessMyClass/img/E100/E123.webp", "GuessMyClass/img/E100/E125.webp", "GuessMyClass/img/E100/E107.webp", "GuessMyClass/img/E100/E109.webp", "GuessMyClass/img/E100/E111.webp", "GuessMyClass/img/E100/E114.webp", "GuessMyClass/img/E100/E121.webp", "GuessMyClass/img/E100/E126.webp"]


# Définition de liste secondaire contenant le chemin de l'image de chaque salle
C000_copy = ["GuessMyClass/img/C000/C006.webp", "GuessMyClass/img/C000/C008.webp", "GuessMyClass/img/C000/C012.webp", "GuessMyClass/img/C000/C009.webp", "GuessMyClass/img/C000/C005.webp"]
C100_copy = ["GuessMyClass/img/C100/C106.webp", "GuessMyClass/img/C100/C108.webp", "GuessMyClass/img/C100/C105.webp", "GuessMyClass/img/C100/C111.webp", "GuessMyClass/img/C100/C114.webp", "GuessMyClass/img/C100/C117.webp", "GuessMyClass/img/C100/C104.webp", "GuessMyClass/img/C100/C109.webp", "GuessMyClass/img/C100/C110.webp", "GuessMyClass/img/C100/C113.webp", "GuessMyClass/img/C100/C115.webp"]
D000_copy = ["GuessMyClass/img/D000/D004.webp", "GuessMyClass/img/D000/D010.webp", "GuessMyClass/img/D000/D012_v2.webp", "GuessMyClass/img/D000/D014.webp", "GuessMyClass/img/D000/Escalier D.webp", "GuessMyClass/img/D000/D006.webp"]
D100_copy = ["GuessMyClass/img/D100/D104.webp", "GuessMyClass/img/D100/D105.webp", "GuessMyClass/img/D100/D106.webp", "GuessMyClass/img/D100/D109.webp", "GuessMyClass/img/D100/D110.webp", "GuessMyClass/img/D100/couloir D haut.webp", "GuessMyClass/img/D100/D111.webp", "GuessMyClass/img/D100/D113.webp", "GuessMyClass/img/D100/D114.webp", "GuessMyClass/img/D100/D117.webp", "GuessMyClass/img/D100/D116.webp", "GuessMyClass/img/D100/D115.webp", "GuessMyClass/img/D100/D112.webp"]
special_copy = ["GuessMyClass/img/special/(parking).webp", "GuessMyClass/img/special/4_arbres.webp", "GuessMyClass/img/special/biathlon.webp", "GuessMyClass/img/special/briques.webp", "GuessMyClass/img/special/cdi.webp", "GuessMyClass/img/special/cours_dehors.webp", "GuessMyClass/img/special/cours_internat.webp", "GuessMyClass/img/special/creux.webp", "GuessMyClass/img/special/dehors_physique.webp", "GuessMyClass/img/special/hall.webp", "GuessMyClass/img/special/petit_arbre.webp", "GuessMyClass/img/special/terrain_foot.webp", "GuessMyClass/img/special/couloir CDI.webp", "GuessMyClass/img/special/couloir salle prof.webp", "GuessMyClass/img/special/escalier E.webp", "GuessMyClass/img/special/Grande passerelle.webp", "GuessMyClass/img/special/Passerelle_D-C_bas.webp", "GuessMyClass/img/special/Passerelle_D-C.webp", "GuessMyClass/img/special/Passerelle_E-D_bas.webp", "GuessMyClass/img/special/Passerelle_E-D.webp"]
toilettes_copy = ["GuessMyClass/img/toilettes/toilettes hall garçon.webp", "GuessMyClass/img/toilettes/toilette haut interieur.webp", "GuessMyClass/img/toilettes/vestiaire.webp"]
A100_copy = ["GuessMyClass/img/A100/A136.webp", "GuessMyClass/img/A100/A137.webp", "GuessMyClass/img/A100/A138.webp", "GuessMyClass/img/A100/A139.webp"]
E000_copy = ["GuessMyClass/img/E000/Beton.webp", "GuessMyClass/img/E000/bois.webp", "GuessMyClass/img/E000/couloir E bas.webp", "GuessMyClass/img/E000/E030.webp", "GuessMyClass/img/E000/Energie.webp", "GuessMyClass/img/E000/peinture.webp", "GuessMyClass/img/E000/E041.webp"]
E100_copy = ["GuessMyClass/img/E100/couloir E haut.webp", "GuessMyClass/img/E100/E116.webp", "GuessMyClass/img/E100/E108.webp", "GuessMyClass/img/E100/E110.webp", "GuessMyClass/img/E100/E113.webp", "GuessMyClass/img/E100/E123.webp", "GuessMyClass/img/E100/E125.webp", "GuessMyClass/img/E100/E107.webp", "GuessMyClass/img/E100/E109.webp", "GuessMyClass/img/E100/E111.webp", "GuessMyClass/img/E100/E114.webp", "GuessMyClass/img/E100/E121.webp", "GuessMyClass/img/E100/E126.webp"]


# Définition d'une liste globale contenant les autres listes
tout = [C000_copy, C100_copy, D100_copy, D000_copy, special_copy, toilettes_copy, A100_copy, E000_copy, E100_copy]

truc = []
block = False

# Fonction pour choisir une image parmi toutes les listes
def choix(liste) :

    i = 0
    run = True

    while run :
        a = liste[randint(0, len(liste) - 1)]
        choix = a[randint(0, len(a) - 1)]
        i += 1
        if choix not in truc:     
            truc.append(choix)
            return choix
        elif i > 1000 :
            for k in truc :
                truc.remove(k)

# Fonction pour incrémenter le timer du jeu
def calc_timer(timer) :

    if timer < 1 :
        return 0, "fin"
    return round(timer -0.015), ""


# Class pour gérer la vue 3D
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


# Fonction principale du gameplay
def game_display():
    
    # Gère le multijoueur
    with open(resource_path("GuessMyClass/score/option.txt"), "r") as f:
        testread = f.readlines()
    
    
    try:
        if testread[0] == "True":
            f.close()
            with open(resource_path("GuessMyClass/score/option.txt"), "w") as f :
                f.write("True")
                f.close()
            mult = True
        else:
            mult = False
    except:
        pass
        
    f.close()
    
    #Création de variables pour le bon fonctionnement du programme
    liste_points = [(0, 0)]
    liste_points2 = [(0, 0)]
    nb = 0
    score = 0
    score2 = 0
    score3 = 0
    score4 = 0
    truc2 = 0
    manche = 1
    map_image_coo = (75, 75)
    etage_image_coo = (75, 75)
    end = False
    reponse_donnee = False
    path_plan = resource_path("GuessMyClass/img/plan/etage_0.png")

    global last_point
    global last_point2
 
    leave_button.draw()
    game_question.draw()
    nb_5.draw()
    nb_10.draw()
    nb_20.draw()
    
    # Gère tous les endroits où l'utilisateur clique
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return 'hell'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 20 <= x <= 140 and 20 <= y <= 70: 
                pygame.time.delay(300)
                return 'home'
            elif (current_w/2 -125) <= x <= (current_w/2 -125 +50) and (current_h/2) <= y <= (current_h/2 +50):
                nb = 5
            elif (current_w/2 -25) <= x <= (current_w/2-25 +50) and (current_h/2) <= y <= (current_h/2 +50):
                nb = 10
            elif (current_w/2 +75) <= x <= (current_w/2 +75 +50) and (current_h/2) <= y <= (current_h/2 +50):
                nb = 20

            if nb == 0 :
                continue
            
            # Boucle en fonction du nombre de round pour afficher chaque image manche par manche
            for _ in range (nb) :
                if truc2 >= 1 :
                    pygame.time.delay(2000)
                choose = choix(tout)
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
                map_icon = pygame.image.load(resource_path('GuessMyClass/icon/map.png'))
                map_icon = pygame.transform.scale(map_icon, map_image_coo)
                map_icon = pygame.image.load(resource_path('GuessMyClass/icon/map.png'))
                map_icon = pygame.transform.scale(map_icon, map_image_coo)
            
                etage_icon = pygame.image.load(resource_path('GuessMyClass/icon/fleche haut.png'))
                etage_icon = pygame.transform.scale(etage_icon, etage_image_coo)
                etage_icon2 = pygame.image.load(resource_path('GuessMyClass/icon/fleche bas.png'))
                etage_icon2 = pygame.transform.scale(etage_icon2, etage_image_coo)
            
                scoreButtonWidth = 200
                scoreButtonHeight = 50
                scoreButtonPos = (current_w -200 - 25, 20)
                scoreButtonElevation = 5
                scoreButtonColor = (220, 0, 0)
                score_button = Shape('score', "Score J1 : " + str(score), scoreButtonWidth, scoreButtonHeight, scoreButtonPos, scoreButtonElevation, scoreButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                
                scoreButton2Width = 200
                scoreButton2Height = 50
                scoreButton2Pos = (current_w -200 - 25, 80)
                scoreButton2Elevation = 5
                scoreButton2Color = (220, 0, 0)
                score_button2 = Shape('score', "Score J2 : " + str(score4), scoreButton2Width, scoreButton2Height, scoreButton2Pos, scoreButton2Elevation, scoreButton2Color, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))

                roundButtonWidth = 200
                roundButtonHeight = 50
                roundButtonPos = (current_w - 400 - 50, 20)
                roundButtonElevation = 5
                roundButtonColor = (104, 180, 229)
                round_button = Shape('round', f"Manche {manche}/{nb}", roundButtonWidth, roundButtonHeight, roundButtonPos, roundButtonElevation, roundButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
        

                if mult == True :
                    score_button2.draw()
                else :
                    score_button2.hide()
            
                timerButtonWidth = 150
                timerButtonHeight = 50
                timerButtonPos = (current_w/2 -75, 20)
                timerButtonElevation = 5
                timerButtonColor = (220, 0, 0)
                timer_button = Shape('timer', "Temps : " + str(timer) + "s", timerButtonWidth, timerButtonHeight, timerButtonPos, timerButtonElevation, timerButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                
                last_point = (0, 0)
                last_point2 = (0, 0)

                while running:
                    salle = choose.split("/")[-1]
                    salle = salle.split(".")[0]
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return 'hell'
                        elif event.type == pygame.KEYDOWN :
                            if map_open == True :
                                last_point2 = pygame.mouse.get_pos()  
                                x2, y2 = last_point2
                                liste_points2.append(last_point2)
                                salle = choose.split("/")[-1]
                                salle = salle.split(".")[0]
                                if len(liste_points2) >= 1 :
                                    score3 = calcul_points(salle, liste_points2[-1], nb_etage)
                        elif event.type == pygame.MOUSEBUTTONUP:
                            x, y = event.pos
                            if 20 <= x <= 140 and 20 <= y <= 70 and clickable == False: 
                                pygame.time.delay(300)
                                return 'home'
                            if current_w - 120 <= x <= current_w - 20 and current_h - 120 <= y <= current_h - 20 and map_block == False:
                                clickable = not clickable
                                map_open = not map_open 
                            if current_w - 225 <= x <= current_w - 120 and current_h - 120 <= y <= current_h - 20 and clickable == True:
                                valider_pressed = not valider_pressed
                            if current_w - 106 <= x <= current_w -6 and current_h -218 <= y <= current_h - 118 and clickable == True:
                                if nb_etage == 1 :
                                    path_plan = resource_path("GuessMyClass/img/plan/etage_0.png")
                                    map_image = pygame.image.load(path_plan)
                                    map_image = pygame.transform.scale(map_image, (current_w, current_h))
                                elif nb_etage == 0 :
                                    path_plan = resource_path("GuessMyClass/img/plan/etage_1.png")
                                    map_image = pygame.image.load(path_plan)
                                    map_image = pygame.transform.scale(map_image, (current_w, current_h))
                                etage_pressed = True
                            else :
                                if map_open == True :
                                    if current_w - 120 <= x <= current_w - 20 and current_h - 120 <= y <= current_h - 20:
                                        pass
                                    else :
                                        last_point = pygame.mouse.get_pos()  
                                        x, y = last_point                          
                                        liste_points.append(last_point)
                                        salle = choose.split("/")[-1]
                                        salle = salle.split(".")[0]
                                        if len(liste_points) >= 2 :
                                            score2 = calcul_points(salle, liste_points[-2], nb_etage)
                        pano_view.handle_event(event)
                    
                    screen.fill((0, 0, 0))

                    if map_open:
                        if mult == True :
                            if nb_etage == 0 :
                                leave_button.hide()
                                screen.blit(map_image, (screen.get_width() // 2 - map_image.get_width() // 2, screen.get_height() // 2 - map_image.get_height() // 2))
                                draw_points(last_point)
                                draw_points2(last_point2)
                                game_valider.draw()
                                game_etage.draw()
                                screen.blit(etage_icon, (current_w -75 - 17,current_h -75 -132))
                                if valider_pressed :
                                    score += score2
                                    score4 += score3
                                    manche += 1
                                    map_open = not map_open
                                    
                                    scoreButtonWidth = 200
                                    scoreButtonHeight = 50
                                    scoreButtonPos = (current_w -200 -25, 20)
                                    scoreButtonElevation = 5
                                    scoreButtonColor = (220, 0, 0)
                                    score_button = Shape('score J1', "Score J1 : " + str(score), scoreButtonWidth, scoreButtonHeight, scoreButtonPos, scoreButtonElevation, scoreButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                                    
                                    scoreButton2Width = 200
                                    scoreButton2Height = 50
                                    scoreButton2Pos = (current_w -200 -25, 80)
                                    scoreButton2Elevation = 5
                                    scoreButton2Color = (220, 0, 0)
                                    score_button2 = Shape('score J2', "Score J2 : " + str(score4), scoreButton2Width, scoreButton2Height, scoreButton2Pos, scoreButton2Elevation, scoreButton2Color, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                                    
                                    show_answer2(salle, liste_points[-2], liste_points2[-1])
                                    truc2 += 1
                                    running = False
                                    clickable = False
                                    nb_etage = 1
                                    path_plan = resource_path("GuessMyClass/img/plan/etage_0.png")
                                    map_image = pygame.image.load(path_plan)
                                    map_image = pygame.transform.scale(map_image, (current_w, current_h))
                                elif etage_pressed :
                                    etage_pressed = False
                                    nb_etage = 1
                            else :
                                leave_button.hide()
                                screen.blit(map_image, (screen.get_width() // 2 - map_image.get_width() // 2, screen.get_height() // 2 - map_image.get_height() // 2))
                                draw_points(last_point)
                                draw_points2(last_point2)
                                game_valider.draw()
                                game_etage.draw()
                                screen.blit(etage_icon2, (current_w -75 - 17,current_h -75 -132))
                                if valider_pressed :
                                    score += score2
                                    score4 += score3
                                    manche += 1
                                    map_open = not map_open
                                    
                                    scoreButtonWidth = 200
                                    scoreButtonHeight = 50
                                    scoreButtonPos = (current_w -200 -25, 20)
                                    scoreButtonElevation = 5
                                    scoreButtonColor = (220, 0, 0)
                                    score_button = Shape('score J1', "Score J1 : " + str(score), scoreButtonWidth, scoreButtonHeight, scoreButtonPos, scoreButtonElevation, scoreButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                                    
                                    scoreButton2Width = 200
                                    scoreButton2Height = 50
                                    scoreButton2Pos = (current_w -200 -25, 80)
                                    scoreButton2Elevation = 5
                                    scoreButton2Color = (220, 0, 0)
                                    score_button2 = Shape('score J2', "Score J2 : " + str(score4), scoreButton2Width, scoreButton2Height, scoreButton2Pos, scoreButton2Elevation, scoreButton2Color, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                                    
                                    show_answer2(salle, liste_points[-2], liste_points2[-1])
                                    truc2 += 1
                                    running = False
                                    clickable = False
                                    nb_etage = 1
                                    path_plan = resource_path("GuessMyClass/img/plan/etage_0.png")
                                    map_image = pygame.image.load(path_plan)
                                    map_image = pygame.transform.scale(map_image, (current_w, current_h))
                                elif etage_pressed :
                                    etage_pressed = False
                                    nb_etage = 0
                        else :
                            if nb_etage == 0 :
                                leave_button.hide()
                                screen.blit(map_image, (screen.get_width() // 2 - map_image.get_width() // 2, screen.get_height() // 2 - map_image.get_height() // 2))
                                draw_points(last_point)
                                game_valider.draw()
                                game_etage.draw()
                                screen.blit(etage_icon, (current_w -75 - 17,current_h -75 -132))
                                if valider_pressed :
                                    score += score2
                                    manche += 1
                                    map_open = not map_open
                                    
                                    scoreButtonWidth = 200
                                    scoreButtonHeight = 50
                                    scoreButtonPos = (current_w -200 -25, 20)
                                    scoreButtonElevation = 5
                                    scoreButtonColor = (220, 0, 0)
                                    score_button = Shape('score', "Score J1 : " + str(score), scoreButtonWidth, scoreButtonHeight, scoreButtonPos, scoreButtonElevation, scoreButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                                    
                                    show_answer(salle, liste_points[-2])
                                    truc2 += 1
                                    running = False
                                    clickable = False
                                    nb_etage = 1
                                    path_plan = resource_path("GuessMyClass/img/plan/etage_0.png")
                                    map_image = pygame.image.load(path_plan)
                                    map_image = pygame.transform.scale(map_image, (current_w, current_h))
                                elif etage_pressed :
                                    etage_pressed = False
                                    nb_etage = 1
                            else :
                                leave_button.hide()
                                screen.blit(map_image, (screen.get_width() // 2 - map_image.get_width() // 2, screen.get_height() // 2 - map_image.get_height() // 2))
                                draw_points(last_point)
                                game_valider.draw()
                                game_etage.draw()
                                screen.blit(etage_icon2, (current_w -75 - 17,current_h -75 -132))
                                if valider_pressed :
                                    score += score2
                                    manche += 1
                                    map_open = not map_open
                                    
                                    scoreButtonWidth = 200
                                    scoreButtonHeight = 50
                                    scoreButtonPos = (current_w -200 -25, 20)
                                    scoreButtonElevation = 5
                                    scoreButtonColor = (220, 0, 0)
                                    score_button = Shape('score', "Score J1 : " + str(score), scoreButtonWidth, scoreButtonHeight, scoreButtonPos, scoreButtonElevation, scoreButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                                    
                                    show_answer(salle, liste_points[-2])
                                    truc2 += 1
                                    running = False
                                    clickable = False
                                    nb_etage = 1
                                    path_plan = resource_path("GuessMyClass/img/plan/etage_0.png")
                                    map_image = pygame.image.load(path_plan)
                                    map_image = pygame.transform.scale(map_image, (current_w, current_h))
                                elif etage_pressed :
                                    etage_pressed = False
                                    nb_etage = 0
                    else:
                        leave_button.show()
                        pano_view.draw()

                    leave_button.draw()
                    score_button.draw()
                    score_button2.draw()
                    round_button.draw()
                    game_map.draw()
                    screen.blit(map_icon, (current_w -75 -17,current_h -75 -22))
                    aze = calc_timer(timer)
                    if timer > 0 :
                        timer -= 0.015
                    if aze[1] == "fin" :
                        map_open = True
                        map_block = True
                        clickable = True
                    timer_button = Shape('timer', "Temps : " + str(round(timer)) + "s", timerButtonWidth, timerButtonHeight, timerButtonPos, timerButtonElevation, timerButtonColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                    timer_button.draw()
                    
                
                    pygame.display.flip()
                    clock.tick(60)
    
            pygame.time.delay(2000)
            end = True
        
            # Ouvre le fichier de score du joueur et met son meilleur score dedans, et envoie le résultat en BDD sauf si le joueur n'est pas connecté
            with open(resource_path("GuessMyClass/profile/compte.txt"), "r") as f:
                pseudo = f.read().strip()

            if pseudo != "Invite\ninvit":
                score_path = resource_path(f"GuessMyClass/score/{pseudo}_{nb}.txt")
                os.makedirs(os.path.dirname(score_path), exist_ok=True)

                best_score = 0
                if os.path.exists(score_path):
                    with open(score_path, "r") as f:
                        best_score = int(f.read().strip())

                if score > best_score:
                    with open(score_path, "w") as f:
                        f.write(str(score))
                        send_score(pseudo, nb, score)


            # Ecran de fin de partie
            if mult == True:
                scoreTotJ1Width = 650
                scoreTotJ1Height = 100
                scoreTotJ1Pos = (current_w/2 -325, current_h/4 -150)
                scoreTotJ1Elevation = 5
                scoreTotJ1Color = (220, 93, 0)
                score_tot_J1 = Shape('score_tot', "Bravo J1 vous avez fait : " + str(score) + " / " + str(nb * 5000) + " points", scoreTotJ1Width, scoreTotJ1Height, scoreTotJ1Pos, scoreTotJ1Elevation, scoreTotJ1Color, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                
                scoreTotJ2Width = 650
                scoreTotJ2Height = 100
                scoreTotJ2Pos = (current_w/2 -325, current_h/4)
                scoreTotJ2Elevation = 5
                scoreTotJ2Color = (220, 93, 0)
                score_tot_J2 = Shape('score_tot', "Bravo J2 vous avez fait : " + str(score4) + " / " + str(nb * 5000) + " points", scoreTotJ2Width, scoreTotJ2Height, scoreTotJ2Pos, scoreTotJ2Elevation, scoreTotJ2Color, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                
                question2Width = 600
                question2Height = 100
                question2Pos = (current_w/2 -300, current_h/4 +150)
                question2Elevation = 5
                question2Color = (220, 93, 0)
                question2 = Shape('question2', "Voulez-vous rejouez ?", question2Width, question2Height, question2Pos, question2Elevation, question2Color, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                
                ouiWidth = 100
                ouiHeight = 50
                ouiPos = (current_w/2 -50 -160, current_h/2 +75)
                ouiElevation = 5
                ouiColor = (0, 220, 0)
                oui = Shape("oui", "Oui", ouiWidth, ouiHeight, ouiPos, ouiElevation, ouiColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))
                
                nonWidth = 100
                nonHeight = 50
                nonPos = (current_w/2 -50 +160, current_h/2 +75)
                nonElevation = 5
                nonColor = (220, 0, 0)
                non = Shape("non", "Non", nonWidth, nonHeight, nonPos, nonElevation, nonColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))
            else:
                scoreTotWidth = 650
                scoreTotHeight = 100
                scoreTotPos = (current_w/2 -325, current_h/4 -100)
                scoreTotElevation = 5
                scoreTotColor = (220, 93, 0)
                score_tot = Shape('score_tot', "Bravo vous avez fait : " + str(score) + " / " + str(nb * 5000) + " points", scoreTotWidth, scoreTotHeight, scoreTotPos, scoreTotElevation, scoreTotColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                
                question2Width = 600
                question2Height = 100
                question2Pos = (current_w/2 -300, current_h/4 +50)
                question2Elevation = 5
                question2Color = (220, 93, 0)
                question2 = Shape('question2', "Voulez-vous rejouez ?", question2Width, question2Height, question2Pos, question2Elevation, question2Color, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))
                
                ouiWidth = 100
                ouiHeight = 50
                ouiPos = (current_w/2 -50 -160, current_h/2 +75)
                ouiElevation = 5
                ouiColor = (0, 220, 0)
                oui = Shape("oui", "Oui", ouiWidth, ouiHeight, ouiPos, ouiElevation, ouiColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))
                
                nonWidth = 100
                nonHeight = 50
                nonPos = (current_w/2 -50 +160, current_h/2 +75)
                nonElevation = 5
                nonColor = (220, 0, 0)
                non = Shape("non", "Non", nonWidth, nonHeight, nonPos, nonElevation, nonColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))


            while end:
                screen.fill("#CDE4E2")
                if mult == True:
                    score_tot_J1.draw()
                    score_tot_J2.draw()
                else:
                    score_tot.draw()
                    question2.draw()

                question2.draw()
                oui.draw()
                non.draw()

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "home"
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        if current_w/2 -50 -160 <= x <= current_w/2 -50 -160 +100 and current_h/2 +75 <= y <= current_h/2 +75 +50:
                            reponse_donnee = True
                        elif current_w/2 -50 +160 <= x <= current_w/2 -50 +160 +100 and current_h/2 +75 <= y <= current_h/2 +75 +50:
                            pygame.time.delay(300)
                            with open(resource_path("GuessMyClass/score/option.txt"), "w") as f:
                                f.write('False')
                            mult = False
                            leave_button.draw()
                            return "home"
                    if reponse_donnee:
                        while truc != [] :
                            for k in truc :
                                truc.remove(k)
                        nb_5.draw()
                        nb_10.draw()
                        nb_20.draw()
                        pygame.display.flip()

                        return "game" 
    return "game"