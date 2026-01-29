
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import sys, os
from math import *
from pygame import *
from shape_creator import *

# Fonctions pour faire le .exe
# Met le bon chemin de fichier
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# Recupère le chemin du score
def get_score_options_path():
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    full_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "score", "options.txt")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path


# Dictionnaire pour stocker les coordonnées de chaque salle
coo_original = {"C005" : [1178, 313, 0], "C006" : [1180, 265, 0], "C008" : [1284, 312, 0], "C009" : [1247, 265, 0], "C012" : [1366, 263, 0],
       "C104" : [1159, 265, 1], "C105" : [1193, 314, 1], "C106" : [1195, 263, 1], "C108" : [1232, 491, 1], "C109" : [1249, 315, 1], "C111" : [1249, 316, 1], "C113" : [1312, 263, 1], "C114" : [1347, 265, 1], "C115" : [1360, 316, 1],"C117" : [1387, 313, 1],"C110" : [1268, 262, 1], 
       "D004" : [1162, 478, 0], "D010" : [1285, 470, 0], "D012_v2" : [1388, 414, 0],"D006" : [1185, 415, 0],"D014" : [1373, 472, 0],
       "D104" : [1198, 471, 1], "D105" : [1170, 421, 1], "D106" : [1212, 419, 1], "D111" : [1271, 418, 0], "D112" : [1299, 469, 0], "D113" : [1310, 420, 0], "D114" : [1360, 471, 0], "D115" : [1358, 419, 0],"D116" : [1386, 469, 0],"D117" : [1387, 420, 0],"D109" : [1246, 471, 1], "D110" : [1274, 471, 1],
       "E107" : [1174, 643, 1], "E108" : [1176, 591, 1], "E109" : [1228, 642, 1], "E110" : [1232, 590, 1], "E111" : [1287, 646, 1], "E114" : [1377, 589, 1], "E113" : [1369, 647, 1],"E123" : [1578, 585, 1],"E125" : [1647, 642, 1], "E116" : [1462, 644, 1], "E121" : [1837, 646, 1], "E126" : [1635, 588, 1],
       "(parking)" : [1685, 501, 0], "4_arbres" : [298, 446, 0],
       "biathlon" : [812, 1003, 0], "briques" : [1668, 1051, 0], "cdi" : [1058, 291, 1], "cours_dehors" : [860, 480, 0],
       "cours_internat" : [632, 731, 0], "creux" : [1615, 360, 0], "dehors_physique" : [1376, 376, 0], "hall" : [1103, 233, 0],
       "petit_arbre" : [97, 895, 0], "terrain_foot" : [569, 207, 0], "toilettes hall garçon" : [1140, 224, 0], "toilette haut interieur" : [1136, 266, 1],
       "vestiaire" : [1154, 671, 0], "couloir CDI" : [1047, 251, 1], "couloir salle prof" : [915, 284, 1], "escalier E" : [1324, 627, 1], "Grande passerelle" : [1111, 444, 0],
       "Passerelle_D-C_bas" : [1339, 379, 0], "Passerelle_D-C" : [1338, 378, 1], "Passerelle_E-D" : [1339, 524, 1], "Passerelle_E-D_bas" : [1338, 520, 0], "couloir E haut" : [1324, 614, 1],
       "Beton" : [1561, 803, 0], "bois" : [1303, 881, 0], "couloir E bas" : [1334, 653, 0], "E030" : [1464, 612, 0], "Energie" : [1447, 725, 0],
       "peinture" : [1193, 829, 0], "couloir D haut" : [1311, 444, 1], "Escalier D" : [1324, 478, 1], "A136" : [1069, 268, 1], "A137" : [1056, 271, 1],
       "A138" : [988, 270, 1], "A139" : [1037, 268, 1], "E041" : [1639, 605, 0]}

# Fonction pour adapter les coordonnées
def scale_coordinates(coord_dict, scale_x, scale_y):
    scaled_dict = {}
    for key, value in coord_dict.items():
        # value = [x, y, étage]
        scaled_x = int(value[0] * scale_x)
        scaled_y = int(value[1] * scale_y)
        scaled_dict[key] = [scaled_x, scaled_y, value[2]]
    return scaled_dict

REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080
scale_x = current_w / REFERENCE_WIDTH
scale_y = current_h / REFERENCE_HEIGHT

# Coordonnées adaptées à l'écran actuel
coo = scale_coordinates(coo_original, scale_x, scale_y)


# Fonction qui calcul le nombre de points par rapport à la salle, les coordonnées du points et l'étage
def calcul_points(salle, coo_pin, nb_etage) :
    # Définition du lambda
    lambda_ = 0.01

    # Calcul de la distance avec pythagore
    distance = sqrt((coo_pin[0]-coo[salle][0])**2 + (coo_pin[1]-coo[salle][1])**2)
    # Fais en sorte que le point ne soit pas obligatoirement pile poil sur le vrai point pour avoir le score max (5000)
    if distance <= 1 :
        return 5000   
    # Calcul le score
    score = 5000 * exp(-lambda_ * distance)

    # Divise le score par 2 si le joueur n'est pas au bon étage
    if nb_etage == 0 and coo[salle][2] == 1 :
        score /= 2
    elif nb_etage == 1 and coo[salle][2] == 0 :
        score /= 2

    # Renvoie le score arrondi pour ne pas avoir de float
    return round(score)


# Fonction pour afficher le point du joueur 1
def draw_points(last_point):
    if last_point:
        pygame.draw.circle(screen, (255, 0, 0), last_point, 7)

# Fonction pour afficher le point du joueur 2     
def draw_points2(last_point2):
    if last_point2:
        pygame.draw.circle(screen, (0, 255, 0), last_point2, 7)

# Fonction pour afficher le point de la solution
def draw_points3(last_point3):
    if last_point3:
        pygame.draw.circle(screen, (0, 0, 255), last_point3, 7)

# Fonction pour afficher les points (joueur et solution) à la fin de la manche
def show_answer(salle, coo_pin) :
    # Solution
    draw_points3((coo[salle][0], coo[salle][1]))
    # Joueur
    draw_points(coo_pin)
    # Fais une ligne entre le point du joueur et de la solution
    pygame.draw.line(screen, (0, 0, 0), coo_pin, (coo[salle][0], coo[salle][1]), width = 3)

# Fonction pour afficher les points (joueurs et solution) à la fin de la manche
def show_answer2(salle, coo_pin, coo_pin2) :
    #Solution
    draw_points3((coo[salle][0], coo[salle][1]))
    # Joueur 1
    draw_points(coo_pin)
    # Joueur 2
    draw_points2(coo_pin2)
    # Fais une ligne entre le point du joueur et de la solution
    pygame.draw.line(screen, (0, 0, 0), coo_pin, (coo[salle][0], coo[salle][1]), width = 3)
    pygame.draw.line(screen, (0, 0, 0), coo_pin2, (coo[salle][0], coo[salle][1]), width = 3)

    
    