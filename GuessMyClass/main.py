
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import pygame
from home import *
from about import *
from log_in import *
from game import *
from welcome import *
from utils import *

pygame.init()

current_w, current_h = pygame.display.Info().current_w, pygame.display.Info().current_h

font = pygame.font.Font(resource_path('GuessMyClass/font/MightySouly.ttf'), 80)

screen = pygame.display.set_mode((current_w, current_h))
clock = pygame.time.Clock()
running = True

icon = pygame.image.load(resource_path('GuessMyClass/icon/Logo PJB.png'))
pygame.display.set_icon(icon)
icon = pygame.transform.scale(icon, (25, 25))

dest = 'welcome'
mult = None
l = False
v = False
o = False
a = False
s = False
mail_text = ''

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

logInWidth = 350
logInHeight = 50
logInPos = (6, current_h/6 + 6 + 5 + 55)
logInElevation = 2
logInColor = (184, 180, 229)
log_in = Shape('log_in', 'Changer de pseudo', logInWidth, logInHeight, logInPos, logInElevation, logInColor, True, (resource_path('GuessMyClass/font/MightySouly.ttf'), 40))

leaveButtonWidth = 50
leaveButtonHeight = 50
leaveButtonpos = (10, 10)
leaveButtonElevation = 2
leaveButtonColor = (200, 0, 0)
leave_button = Shape('home', '<', leaveButtonWidth, leaveButtonHeight, leaveButtonpos, leaveButtonElevation, leaveButtonColor, True)

# Fonction qui fait une ombre
def shade():
    s = pygame.Surface((current_w, current_h))
    s.set_alpha(175)
    s.fill((255, 255, 255))
    screen.blit(s, (0, 0))

# Programme principal
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
            dest = sign_in.draw()
            if dest == 'sign_in':
                s = True
            dest = log_in.draw()
            if dest is None:
                dest = 'home'
            if s:
                dest = 'sign_in'
                a = False
                s = False

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

    pygame.display.flip()
    clock.tick(3600)

pygame.quit()
