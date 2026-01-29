
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import pygame
from shape_creator import *
from sql_link import *
from utils import *

b = 3

scoreboardWidth = current_w / b - 15
scoreboardHeight = current_h - 130
scoreboardPos = (10, 120)
scoreboardElevation = 0
scoreboardColor = (144, 180, 229)
scoreboards = [Shape(None, '', scoreboardWidth, scoreboardHeight, scoreboardPos, scoreboardElevation, scoreboardColor)]

for i in range(1, b):
    scoreboardPos = (10 * i + 10 + (current_w / b - 10) * i, 120)
    scoreboards.append(Shape(None, '', scoreboardWidth, scoreboardHeight, scoreboardPos, scoreboardElevation, scoreboardColor))

bestTitleWidth = current_w / 4
bestTitleHeight = 50
bestTitleElevation = 0
bestTitleColor = (144, 140, 189)

best_titles = [
    Shape(None, "Meilleur sur 5", bestTitleWidth, bestTitleHeight, (10 + ((current_w / b - 15) / 2) - (current_w / 4) / 2, 125), bestTitleElevation, bestTitleColor, False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35)),
    Shape(None, "Meilleur sur 10", bestTitleWidth, bestTitleHeight, (current_w / 2 - current_w / 8, 125), bestTitleElevation, bestTitleColor, False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35)),
    Shape(None, "Meilleur sur 20", bestTitleWidth, bestTitleHeight, (current_w - (current_w / b - 15) / 2 - 5 - (current_w / 4) / 2, 125), bestTitleElevation, bestTitleColor, False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))]


leaderboards = [[], [], []]

try:
    for i, mode in enumerate([5, 10, 20]):
        data = get_leaderboard(mode)
        y = 180
        rank = 1
        for row in data:
            entryWidth = current_w / b - 40
            entryHeight = 40
            entryPos = (scoreboards[i].top_rect.x + 10, y)
            entryElevation = 0
            entryColor = (224, 180, 229)
            leaderboards[i].append(Shape(None, f"{rank} : {row['pseudo']} / {row['score']}", entryWidth, entryHeight, entryPos, entryElevation, entryColor, False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 30)))
            y += 44
            rank += 1
    connected = True
except Exception as e:
    print(f"Erreur lors de la récupération du leaderboard: {e}")
    import traceback
    traceback.print_exc()
    connected = False

# Fonction pour afficher le leaderboard
def leaderboard_display():
    dest = leave_button.draw()
    if dest is not None:
        pygame.time.delay(300)
        return dest

    for board in scoreboards:
        board.draw()

    big_leaderboard.draw()

    if connected:
        for column in leaderboards:
            for item in column:
                item.draw()

    for title in best_titles:
        title.draw()

    return "leaderboard"
