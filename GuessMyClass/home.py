
# Importe les bibliothèques nécessaires pour le fonctionnement du code

from shape_creator import *
from utils import *

# Menu de l'écran d'acceuil

# Affiche le menu
def home_display(icon):
    screen.fill((205,228,226))
    with open(resource_path("GuessMyClass/profile/compte.txt"), "r") as f:
        lines = f.readlines()
        f.close()
    ide = ''
    for i in range(len(lines[0])):
        ide = ide + lines[0][i]
    
    button1Width = current_w/4-12
    button1Height = current_h/6
    button1Pos = (6, 6)
    button1Elevation = 0
    button1Color = (104, 208, 229)
    button1 = Shape(None, ide, button1Width, button1Height, button1Pos, button1Elevation, button1Color)

    dest = button1.draw()
    if dest != None:
        return dest
    home_title.draw()

    dest = home_button2.draw()
    if dest != None:
        return dest

    bottom_bar.draw()

    dest = play_button.draw()
    if dest != None:
        return dest
    # Bouton paramètre pas encore en place
    #dest = button_list1.draw()
    #if dest != None:
    #    return dest
    dest = button_list2.draw()
    if dest != None:
        return dest
    dest = button_list3.draw()
    if dest != None:
        return dest
    dest = button_list4.draw()
    if dest != None:
        return dest
    dest = online.draw()
    if dest != None:
        return dest

    infos_left.draw()
    infos_right.draw()
    screen.blit(icon, (current_w-25-5,current_h-25-5))

    return 'home'
