
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import sys, os
import pygame
from pathlib import Path
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

# Definition de toutes les shapes du jeu
leaveButtonWidth = 50
leaveButtonHeight = 50
leaveButtonpos = (10, 10)
leaveButtonElevation = 2
leaveButtonColor = (200, 0, 0)
leave_button = Shape('home', '<', leaveButtonWidth, leaveButtonHeight, leaveButtonpos, leaveButtonElevation, leaveButtonColor, True)

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
home_title = Shape(None, 'GMC', titleWidth, titleHeight, titlePos, titleElevation, titleColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 150))

button2Width = current_w/4-6
button2Height = current_h/6
button2Pos = (current_w-current_w/4, 6)
button2Elevation = 2
button2Color = (104, 208, 229)
home_button2 = Shape('about', 'À propos', button2Width, button2Height, button2Pos, button2Elevation, button2Color, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 100))

bottomBarWidth = current_w
bottomBarHeight = 35
bottomBarPos = (0, current_h-35)
bottomBarElevation = 0
bottomBarColor = (104, 208, 229)
bottom_bar = Shape(None, 'GMC - 2025', bottomBarWidth, bottomBarHeight, bottomBarPos, bottomBarElevation, bottomBarColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 20), False)

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

welcomeTitleWidth = (current_w/4-6)*2+958
welcomeTitleHeight = current_h/6
welcomeTitlePos = (current_w/250, 8)
welcomeTitleElevation = 0
welcomeTitleColor = (104, 180, 229)
welcome_title = Shape(None, 'Bienvenue sur GMC !', welcomeTitleWidth, welcomeTitleHeight, welcomeTitlePos, welcomeTitleElevation, welcomeTitleColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 150))

choixWidth = (current_w/4-6)*2+200
choixHeight = current_h/6
choixPos = (current_w/5, 400)
choixElevation = 0
choixColor = (144, 180, 229)
choix_shape = Shape(None, 'Que voulez-vous faire ?', choixWidth, choixHeight, choixPos, choixElevation, choixColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 100))

logInWelcomeWidth = ((current_w/4-6)*2+58)/1.8
logInWelcomeHeight = current_h/8
logInWelcomePos = (current_w/5, 600)
logInWelcomeElevation = 2
logInWelcomeColor = (184, 180, 229)
log_in_welcome = Shape('home', 'Se connecter', logInWelcomeWidth, logInWelcomeHeight, logInWelcomePos, logInWelcomeElevation, logInWelcomeColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 70))

signInWidth = ((current_w/4-6)*2+58)/1.8
signInHeight = current_h/8
signInPos = (current_w/1.97, 600)
signInElevation = 2
signInColor = (184, 180, 229)
sign_in = Shape('home', 'Créer un compte', signInWidth, signInHeight, signInPos, signInElevation, signInColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 70))

sansCompteWidth = (current_w/4-6)*1
sansCompteHeight = current_h/12
sansComptePos = (current_w/2.67, 755)
sansCompteElevation = 0
sansCompteColor = (193, 214, 213)
sans_compte = Shape("home", 'Jouer sans compte', sansCompteWidth, sansCompteHeight, sansComptePos, sansCompteElevation, sansCompteColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 50))

questionWidth = 1920/3
questionHeight = 100
questionPos = (current_w/2 -1920/6, current_h/2 -200)
questionElevation = 0
questionColor = (220, 0, 0)
game_question = Shape('question', "Combien de round voulez-vous jouer ?", questionWidth, questionHeight, questionPos, questionElevation, questionColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))

nb5Width = 50
nb5Height = 50
nb5Pos = (current_w/2 -125, current_h/2)
nb5Elevation = 2
nb5Color = (255, 128, 0)
nb_5 = Shape(None, "5", nb5Width, nb5Height, nb5Pos, nb5Elevation, nb5Color, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

nb10Width = 50
nb10Height = 50
nb10Pos = (current_w/2-25, current_h/2)
nb10Elevation = 2
nb10Color = (255, 128, 0)
nb_10 = Shape(None, "10", nb10Width, nb10Height, nb10Pos, nb10Elevation, nb10Color, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

nb20Width = 50
nb20Height = 50
nb20Pos = (current_w/2 +75, current_h/2)
nb20Elevation = 2
nb20Color = (255, 128, 0)
nb_20 = Shape(None, "20", nb20Width, nb20Height, nb20Pos, nb20Elevation, nb20Color, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

mapWidth = 100
mapHeight = 100
mapPos = (current_w -100 -5,current_h -100 -5)
mapElevation = 5
mapColor = (206, 206, 206)
game_map = Shape('map', "", mapWidth, mapHeight, mapPos, mapElevation, mapColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

validerWidth = 100
validerHeight = 100
validerPos = (current_w -100 -100 -10, current_h - 100 -5)
validerElevation = 5
validerColor = (0, 220, 0)
game_valider = Shape("valider", "Check", validerWidth, validerHeight, validerPos, validerElevation, validerColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

etageWidth = 100
etageHeight = 100
etagePos = (current_w -100 -5, current_h -100 -100 -10 -5)
etageElevation = 5
etageColor = (0, 0, 0)
game_etage = Shape("etage", "", etageWidth, etageHeight, etagePos, etageElevation, etageColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

bigLeaderboardWidth = current_w / 2 - 190
bigLeaderboardHeight = 100
bigLeaderboardPos = (current_w / 2 - (current_w / 2 - 190) / 2, 10)
bigLeaderboardElevation = 0
bigLeaderboardColor = (144, 180, 229)
big_leaderboard = Shape(None, 'Classements', bigLeaderboardWidth, bigLeaderboardHeight, bigLeaderboardPos, bigLeaderboardElevation, bigLeaderboardColor, False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 60))

popupLeaveWidth = current_w/4 + 100
popupLeaveHeight = 100
popupLeavePos = (current_w/2 - (current_w/4)/2 - 50, current_h/2 - 50)
popupLeaveElevation = 0
popupLeaveColor = (104, 180, 229)
popup_leave = Shape(None, 'Êtes-vous sûr de vouloir quitter ?', popupLeaveWidth, popupLeaveHeight, popupLeavePos, popupLeaveElevation, popupLeaveColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))

popupYesWidth = current_w/20
popupYesHeight = 50
popupYesPos = (current_w/2 - 125, current_h/2 + 100)
popupYesElevation = 2
popupYesColor = (0, 180, 0)
popup_yes = Shape('hell', 'Oui', popupYesWidth, popupYesHeight, popupYesPos, popupYesElevation, popupYesColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))

popupNoWidth = current_w/20
popupNoHeight = 50
popupNoPos = (current_w/2 - 125 + 250 - (current_w/20), current_h/2 + 100)
popupNoElevation = 2
popupNoColor = (180, 0, 0)
popup_no = Shape('paradise', 'Non', popupNoWidth, popupNoHeight, popupNoPos, popupNoElevation, popupNoColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 30))

popupVersus1Width = 350
popupVersus1Height = 350
popupVersus1Pos = (current_w/2 - 175, current_h/2 - 175)
popupVersus1Elevation = 3
popupVersus1Color = (184, 180, 229)
popup_versus1 = Shape('versus_friend', 'Versus friend', popupVersus1Width, popupVersus1Height, popupVersus1Pos, popupVersus1Elevation, popupVersus1Color, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 50))

logInMainWidth = 350
logInMainHeight = 50
logInMainPos = (6, current_h/6 + 6 + 5 + 55)
logInMainElevation = 2
logInMainColor = (184, 180, 229)
log_in_main = Shape('log_in', 'Changer de pseudo', logInMainWidth, logInMainHeight, logInMainPos, logInMainElevation, logInMainColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))