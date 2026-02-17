import pygame
import time
import random
from shape_creator import *
from utils import *
from multiplayer import get_room_info, start_game, leave_room, update_player_color, PLAYER_COLORS
from sql_link import load_local_profile

leave_button_waiting = Shape('multiplayer_menu', '<', 50, 50, (10, 10), 2, (200, 0, 0), True, (resource_path("GuessMyClass/font/MightySouly.ttf"), 40))

room_data          = None
is_host            = False
current_room_code  = None
last_update_time   = 0
start_button_cached = None


# ──────────────────────────────────────────────
# Sélecteur de couleur
# ──────────────────────────────────────────────

SWATCH_SIZE   = 36   # taille d'un carré de couleur
SWATCH_GAP    = 10   # espace entre carrés
SWATCH_COLS   = 5    # 5 couleurs par ligne → 2 lignes pour 10 couleurs

def get_swatches_layout(cx, top_y):
    """
    Retourne la liste des (rect, color) pour la palette.
    cx   : centre horizontal
    top_y: y de départ
    """
    total_w = SWATCH_COLS * SWATCH_SIZE + (SWATCH_COLS - 1) * SWATCH_GAP
    start_x = cx - total_w // 2
    swatches = []
    for i, color in enumerate(PLAYER_COLORS):
        col = i % SWATCH_COLS
        row = i // SWATCH_COLS
        x = start_x + col * (SWATCH_SIZE + SWATCH_GAP)
        y = top_y  + row * (SWATCH_SIZE + SWATCH_GAP)
        rect = pygame.Rect(x, y, SWATCH_SIZE, SWATCH_SIZE)
        swatches.append((rect, color))
    return swatches

def draw_color_picker(screen, swatches, my_color, taken_colors, font_small):
    """
    Dessine la palette de couleurs.
    - my_color    : couleur actuelle du joueur  → entourée en blanc épais
    - taken_colors: couleurs prises par les autres → grisées + croix
    """
    label = font_small.render("Choisissez votre couleur :", True, (50, 50, 50))
    screen.blit(label, (swatches[0][0].x, swatches[0][0].y - 28))

    for rect, color in swatches:
        taken_by_other = any(tuple(c) == tuple(color) for c in taken_colors)

        if taken_by_other:
            # Couleur grisée
            grey = (160, 160, 160)
            pygame.draw.rect(screen, grey, rect, border_radius=6)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2, border_radius=6)
            # Croix rouge par-dessus
            pygame.draw.line(screen, (200, 0, 0), rect.topleft, rect.bottomright, 3)
            pygame.draw.line(screen, (200, 0, 0), rect.topright, rect.bottomleft, 3)
        else:
            pygame.draw.rect(screen, color, rect, border_radius=6)

            if tuple(color) == tuple(my_color):
                # Couleur sélectionnée : double bordure blanche + noire
                pygame.draw.rect(screen, (255, 255, 255), rect.inflate(6, 6), 3, border_radius=8)
                pygame.draw.rect(screen, (0, 0, 0), rect.inflate(10, 10), 2, border_radius=10)
            else:
                # Bordure noire standard
                pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=6)

                # Hover : légère surbrillance
                if rect.collidepoint(pygame.mouse.get_pos()):
                    hover_surf = pygame.Surface((SWATCH_SIZE, SWATCH_SIZE), pygame.SRCALPHA)
                    hover_surf.fill((255, 255, 255, 60))
                    screen.blit(hover_surf, rect.topleft)


# ──────────────────────────────────────────────
# Display principal
# ──────────────────────────────────────────────

def waiting_room_display(room_code, host):
    global room_data, is_host, current_room_code, last_update_time, start_button_cached

    current_room_code = room_code
    is_host = host

    pseudo = load_local_profile()
    font_small = pygame.font.Font(resource_path('GuessMyClass/font/MightySouly.ttf'), 22)

    # ── Polling Supabase (toutes les 1 s) ──────
    current_time = time.time()
    if room_data is None or current_time - last_update_time > 1.0:
        room_data = get_room_info(room_code)
        last_update_time = current_time
        if not room_data:
            return "multiplayer_menu"

    # ── Couleurs ───────────────────────────────
    player_colors = room_data.get("player_colors", {})
    my_color      = tuple(player_colors.get(pseudo, list(PLAYER_COLORS[0])))

    # Couleurs prises par LES AUTRES (pas moi)
    taken_colors  = [
        tuple(c) for p, c in player_colors.items()
        if p != pseudo
    ]

    # Palette positionnée sous la liste de joueurs
    nb_players   = len(room_data["players"])
    palette_top  = 240 + nb_players * 60 + 20   # 20px sous le dernier joueur
    swatches     = get_swatches_layout(current_w // 2, palette_top)

    # ── Shapes UI ─────────────────────────────
    title = Shape(
        None, f'Code: {room_code}', 400, 80,
        (current_w/2 - 200, 50), 0, (0, 200, 0), False,
        (resource_path('GuessMyClass/font/MightySouly.ttf'), 60)
    )
    waiting_text = Shape(
        None, 'Joueurs dans la partie:', 500, 60,
        (current_w/2 - 250, 150), 0, (144, 180, 229), False,
        (resource_path('GuessMyClass/font/MightySouly.ttf'), 40)
    )

    player_shapes = []
    for i, player in enumerate(room_data["players"]):
        label       = f"👑 {player}" if player == room_data["host"] else f"• {player}"
        pcolor      = tuple(player_colors.get(player, list(PLAYER_COLORS[i % len(PLAYER_COLORS)])))

        # Fond de la ligne coloré avec la couleur du joueur (semi-transparent)
        shape = Shape(
            None, label, 400, 50,
            (current_w/2 - 200, 230 + i * 60), 0,
            pcolor, False,
            (resource_path('GuessMyClass/font/MightySouly.ttf'), 35)
        )
        player_shapes.append(shape)

    # ── Gestion des événements (clics palette) ─
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'hell'

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for rect, color in swatches:
                if rect.collidepoint(event.pos):
                    # Ignore si couleur prise
                    if tuple(color) in taken_colors:
                        break
                    # Ignore si déjà ma couleur
                    if tuple(color) == my_color:
                        break
                    # ✅ Met à jour en BDD
                    ok = update_player_color(room_code, pseudo, color)
                    if ok:
                        # Mise à jour locale immédiate (sans attendre le polling)
                        player_colors[pseudo] = list(color)
                        my_color = tuple(color)
                    break

    # ── Dessin ────────────────────────────────
    dest = leave_button_waiting.draw()
    if dest:
        leave_room(room_code, pseudo)
        start_button_cached = None
        room_data = None
        return dest

    title.draw()
    waiting_text.draw()

    # Liste joueurs avec petit carré de leur couleur à gauche
    for i, (shape, player) in enumerate(zip(player_shapes, room_data["players"])):
        pcolor = tuple(player_colors.get(player, list(PLAYER_COLORS[i % len(PLAYER_COLORS)])))
        # Carré de couleur à gauche du nom
        sq_x = current_w // 2 - 230
        sq_y = 230 + i * 60 + 15
        pygame.draw.rect(screen, pcolor, (sq_x, sq_y, 20, 20), border_radius=4)
        pygame.draw.rect(screen, (0, 0, 0), (sq_x, sq_y, 20, 20), 2, border_radius=4)
        shape.draw()

    # ✅ Palette de couleurs
    draw_color_picker(screen, swatches, my_color, taken_colors, font_small)

    # ── Bouton Lancer (host seulement) ────────
    if is_host and len(room_data["players"]) >= 1:
        if start_button_cached is None:
            start_button_cached = Shape(
                'start_game', 'Lancer la partie', 300, 70,
                (current_w/2 - 150, current_h - 100), 3, (0, 200, 0), True,
                (resource_path('GuessMyClass/font/MightySouly.ttf'), 40)
            )

        start_dest = start_button_cached.draw()
        if start_dest == 'start_game':
            from coordonées_salles import coo
            salles    = list(coo.keys())
            first_room = random.choice(salles)
            start_game(room_code, first_room)
            start_button_cached = None
            room_data = None
            pygame.time.delay(500)
            return ('game_multi', room_code)

    # ── Détection démarrage par l'hôte (non-hôtes) ──
    if room_data["status"] == "playing":
        start_button_cached = None
        room_data = None
        return ('game_multi', room_code)

    return ("waiting_room", room_code, is_host)