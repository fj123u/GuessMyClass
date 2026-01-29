
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import pygame
from shape_creator import *
from log_in import *
from utils import *

titleWidth = (current_w/4-6)*2+958
titleHeight = current_h/6
titlePos = (current_w/250, 8)
titleElevation = 0
titleColor = (104, 180, 229)
title = Shape(None, 'Bienvenue sur GMC !', titleWidth, titleHeight, titlePos, titleElevation, titleColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 150))

choixWidth = (current_w/4-6)*2+200
choixHeight = current_h/6
choixPos = (current_w/5, 400)
choixElevation = 0
choixColor = (144, 180, 229)
choix = Shape(None, 'Que voulez-vous faire ?', choixWidth, choixHeight, choixPos, choixElevation, choixColor, False, (resource_path('GuessMyClass/font/MightySouly.ttf'), 100))

logInWidth = ((current_w/4-6)*2+58)/1.8
logInHeight = current_h/8
logInPos = (current_w/5, 600)
logInElevation = 2
logInColor = (184, 180, 229)
log_in = Shape('home', 'Se connecter', logInWidth, logInHeight, logInPos, logInElevation, logInColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 70))

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

mdpWidth = (current_w/4-6)*1
mdpHeight = current_h/12
mdpPos = (current_w/2.67, 755)
mdpElevation = 0
mdpColor = (193, 214, 213)
mdp = Shape("home", 'Votre mot de passe est :', mdpWidth, mdpHeight, mdpPos, mdpElevation, mdpColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 50))


# Boucle principale du jeu
def welcome_display(): 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if log_in.top_rect.collidepoint(event.pos):
                dest = log_in_display()
                if dest:
                    return dest 
    choix.draw()
    title.draw()
    sign_in.draw()
    log_in.draw()
    dest = sans_compte.draw()
    if dest is not None:
        with open(resource_path("GuessMyClass/profile/compte.txt"), "w") as f:
            f.write("Invite\ninvit")
            f.close()
        return dest
