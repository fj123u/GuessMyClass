import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


import pygame
from shape_creator import *
from sql_link import *


b = 3

leave_button = Shape(
    'home', '<',
    50, 50,
    (10, 10),
    2,
    (200, 0, 0),
    True,
    (resource_path("GuessMyClass/font/MightySouly.ttf"), 40)
)

scoreboards = [
    Shape(
        None, '',
        current_w / b - 15,
        current_h - 130,
        (10, 120),
        0,
        (144, 180, 229)
    )
]

for i in range(1, b):
    scoreboards.append(
        Shape(
            None, '',
            current_w / b - 15,
            current_h - 130,
            (10 * i + 10 + (current_w / b - 10) * i, 120),
            0,
            (144, 180, 229)
        )
    )

big_leaderboard = Shape(
    None, 'Classements',
    current_w / 2 - 190,
    100,
    (current_w / 2 - (current_w / 2 - 190) / 2, 10),
    0,
    (144, 180, 229),
    False,
    (resource_path("GuessMyClass/font/MightySouly.ttf"), 60)
)

best_titles = [
    Shape(None, "Meilleur sur 5", current_w / 4, 50,
          (10 + ((current_w / b - 15) / 2) - (current_w / 4) / 2, 125),
          0, (144, 140, 189), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35)),

    Shape(None, "Meilleur sur 10", current_w / 4, 50,
          (current_w / 2 - current_w / 8, 125),
          0, (144, 140, 189), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35)),

    Shape(None, "Meilleur sur 20", current_w / 4, 50,
          (current_w - (current_w / b - 15) / 2 - 5 - (current_w / 4) / 2, 125),
          0, (144, 140, 189), False, (resource_path("GuessMyClass/font/MightySouly.ttf"), 35))
]


leaderboards = [[], [], []]

try:
    for i, mode in enumerate([5, 10, 20]):
        data = get_leaderboard(mode)
        print(f"Mode {mode}: {len(data)} résultats")
        y = 180
        rank = 1
        for row in data:
            leaderboards[i].append(
                Shape(
                    None,
                    f"{rank} : {row['pseudo']} / {row['score']}",
                    current_w / b - 40,
                    40,
                    (scoreboards[i].top_rect.x + 10, y),
                    0,
                    (224, 180, 229),
                    False,
                    (resource_path("GuessMyClass/font/MightySouly.ttf"), 30)
                )
            )
            y += 44
            rank += 1
    connected = True
except Exception as e:
    print(f"Erreur lors de la récupération du leaderboard: {e}")
    import traceback
    traceback.print_exc()
    connected = False


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
