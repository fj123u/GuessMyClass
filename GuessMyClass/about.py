
# Importe les bibliothèques nécessaires pour le fonctionnement du code

import pygame
from utils import *
from shape_creator import *

# Crée un bouton pour quitter l'écran "À propos"
leaveButtonWidth = 50
leaveButtonHeight = 50
leaveButtonpos = (10, 10)
leaveButtonElevation = 2
leaveButtonColor = (200, 0, 0)
leave_button = Shape('home', '<', leaveButtonWidth, leaveButtonHeight, leaveButtonpos, leaveButtonElevation, leaveButtonColor, True)

# Fonction pour la partie about du jeu
def about_display():
    # Récupère les informations de l'écran
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Crée une fenêtre de la taille de l'écran
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Chemins des images des membres de l'équipe
    image_paths = [resource_path('GuessMyClass/Images/melvin.jpg'), resource_path('GuessMyClass/Images/colin.png'), resource_path('GuessMyClass/Images/evan.png'), resource_path('GuessMyClass/Images/theo.jpg'), resource_path('GuessMyClass/Images/gabriel.png')]
    descriptions = [
        "Melvin - Le stratège de l'équipe",
        "Colin - Le codeur fou",
        "Evan - L'artiste de la bande",
        "Théo - Le cerveau de l'opération",
        "Gabriel - L'inventeur génial"]

    # Fonction pour arrondir les coins d'une surface
    def round_corners(surface, radius):
        rounded_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(rounded_surface, (255, 255, 255), rounded_surface.get_rect(), border_radius=radius)
        rounded_surface.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return rounded_surface

    # Fonction pour charger et préparer les images avec des coins arrondis
    def load_and_prepare_images(image_paths, radius):
        return [round_corners(pygame.transform.smoothscale(pygame.image.load(path), (frame_width, frame_height)), radius) for path in image_paths]

    # Définit la taille des cadres pour les images
    frame_width = screen_width // 5
    frame_height = screen_height // 2
    images = load_and_prepare_images(image_paths, 30)
    current_index = 0

    # Chemins des images de dégradé
    degrade_path = [resource_path('GuessMyClass/Images/degrade.png'), resource_path('GuessMyClass/Images/degrade_droite.png')]
    degrades = load_and_prepare_images(degrade_path, 0)

    # Fonction pour obtenir les indices des images visibles
    def get_visible_indices(current_index):
        return [(current_index - 1) % len(images), current_index, (current_index + 1) % len(images)]

    visible_indices = get_visible_indices(current_index)

    # Charge une police de caractères personnalisée
    font = pygame.font.Font(resource_path('GuessMyClass/font/MightySouly.ttf'), 20)
    text_color = (255, 255, 255)

    # Définit la taille et la position des flèches
    arrow_size = 50
    arrow_left_rect = pygame.Rect(50, screen_height // 2 - arrow_size // 2, arrow_size, arrow_size)
    arrow_right_rect = pygame.Rect(screen_width - 50 - arrow_size, screen_height // 2 - arrow_size // 2, arrow_size, arrow_size)

    # Variable pour contrôler la boucle principale
    running = True
    while running:
        screen.fill((205, 228, 226))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arrow_left_rect.collidepoint(event.pos):
                    current_index = (current_index - 1) % len(images)
                    visible_indices = get_visible_indices(current_index)
                elif arrow_right_rect.collidepoint(event.pos):
                    current_index = (current_index + 1) % len(images)
                    visible_indices = get_visible_indices(current_index)

        # Positionne les images sur l'écran
        frame_center = images[visible_indices[1]].get_rect(center=(screen_width // 2, screen_height // 2))
        frame_left = images[visible_indices[0]].get_rect(center=(screen_width // 4, screen_height // 2))
        frame_right = images[visible_indices[2]].get_rect(center=(screen_width * 3 // 4, screen_height // 2))

        # Affiche les images sur l'écran
        screen.blit(images[visible_indices[0]], frame_left)
        screen.blit(images[visible_indices[1]], frame_center)
        screen.blit(images[visible_indices[2]], frame_right)

        # Affiche les dégradés sur les côtés des images
        screen.blit(degrades[0], degrades[0].get_rect(center=(screen_width // 4.4, screen_height // 2)))
        screen.blit(degrades[1], degrades[1].get_rect(center=(screen_width * 3 // 3.9, screen_height // 2)))

        # Affiche le bouton pour quitter l'écran "À propos"
        dest = leave_button.draw()
        if dest != None:
            pygame.time.delay(300)
            return dest

        # Affiche la description du membre actuellement sélectionné
        text_surface = font.render(descriptions[current_index], True, text_color)
        screen.blit(text_surface, text_surface.get_rect(center=(screen_width // 2, screen_height * 3 // 4.2)))

        # Dessine les flèches pour naviguer entre les images
        pygame.draw.polygon(screen, (100, 100, 100), [
            (arrow_left_rect.left, arrow_left_rect.centery),
            (arrow_left_rect.right, arrow_left_rect.top),
            (arrow_left_rect.right, arrow_left_rect.bottom)
        ])
        pygame.draw.polygon(screen, (100, 100, 100), [
            (arrow_right_rect.right, arrow_right_rect.centery),
            (arrow_right_rect.left, arrow_right_rect.top),
            (arrow_right_rect.left, arrow_right_rect.bottom)
        ])

        # Met à jour l'affichage
        pygame.display.flip()

    return 'about'