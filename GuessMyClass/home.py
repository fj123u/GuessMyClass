
# Importe les bibliothèques nécessaires pour le fonctionnement du code

from shape_creator import *
from utils import *

# Menu de l'écran d'acceuil
playButtonWidth = 370
playButtonHeight = 140
playButtonPos = (current_w/2-185, current_h/2-150)
playButtonElevation = 10
playButtonColor = (255, 145, 0)
play_button = Shape('game', 'Jouer', playButtonWidth, playButtonHeight, playButtonPos, playButtonElevation, playButtonColor, True)

titleWidth = (current_w/4-6)*2+6
titleHeight = current_h/6
titlePos = (current_w/4, 6)
titleElevation = 0
titleColor = (104, 180, 229)
title = Shape(None, 'GMC', titleWidth, titleHeight, titlePos, titleElevation, titleColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 150))

button2Width = current_w/4-6
button2Height = current_h/6
button2Pos = (current_w-current_w/4, 6)
button2Elevation = 2
button2Color = (104, 208, 229)
button2 = Shape('about', 'À propos', button2Width, button2Height, button2Pos, button2Elevation, button2Color, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 100))

bottomBarWidth = current_w
bottomBarHeight = 35
bottomBarPos = (0, current_h-35)
bottomBarElevation = 0
bottomBarColor = (104, 208, 229)
bottom_bar = Shape(None, 'GMC - 2025', bottomBarWidth, bottomBarHeight, bottomBarPos, bottomBarElevation, bottomBarColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 20), False)

# A faire les paramètres
#button_list1 = Shape('settings', 'Paramètres', 250, 50, (current_w/2-125, current_h/2+50), 2, (224, 180, 229), True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

buttonList2Width = 250
buttonList2Height = 50
buttonList2Pos = (current_w/2-125, current_h/2+106)
buttonList2Elevation = 2
buttonList2Color = (184, 180, 229)
button_list2 = Shape('versus', 'Versus', buttonList2Width, buttonList2Height, buttonList2Pos, buttonList2Elevation, buttonList2Color, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

buttonList3Width = 250
buttonList3Height = 50
buttonList3Pos = (current_w/2-125, current_h/2+212-50)
buttonList3Elevation = 2
buttonList3Color = (144, 180, 229)
button_list3 = Shape('leaderboard', 'Classements', buttonList3Width, buttonList3Height, buttonList3Pos, buttonList3Elevation, buttonList3Color, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

buttonList4Width = 250
buttonList4Height = 50
buttonList4Pos = (current_w/2-125, current_h/2+218)
buttonList4Elevation = 2
buttonList4Color = (104, 180, 229)
button_list4 = Shape('leave', 'Quitter', buttonList4Width, buttonList4Height, buttonList4Pos, buttonList4Elevation, buttonList4Color, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

infosLeftWidth = current_w/3
infosLeftHeight = current_h -current_h/6 -60 -35
infosLeftPos = (current_w/60,30 +current_h/6)
infosLeftElevation = 0
infosLeftColor = (144, 180, 229)
infos_left = Shape(None, '', infosLeftWidth, infosLeftHeight, infosLeftPos, infosLeftElevation, infosLeftColor)

infosRightWidth = current_w/3
infosRightHeight = current_h -current_h/6 -60 -35
infosRightPos = (current_w -current_w/3 -current_w/60, 30 +current_h/6)
infosRightElevation = 0
infosRightColor = (144, 180, 229)
infos_right = Shape(None, '', infosRightWidth, infosRightHeight, infosRightPos, infosRightElevation, infosRightColor)

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
    title.draw()

    dest = button2.draw()
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

    infos_left.draw()
    infos_right.draw()
    screen.blit(icon, (current_w-25-5,current_h-25-5))

    return 'home'
