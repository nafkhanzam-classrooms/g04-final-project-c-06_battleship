import pygame

from shared.constants import SHIPS


def load_font(path, size, fallback="arial"):
    try:
        return pygame.font.Font(path, size)
    except FileNotFoundError:
        return pygame.font.SysFont(fallback, size)


def load_ship_images():
    images = {}

    for ship in SHIPS:
        image_path = ship.get("image")

        if not image_path:
            images[ship["name"]] = None
            continue

        try:
            images[ship["name"]] = pygame.image.load(image_path).convert_alpha()
        except (FileNotFoundError, pygame.error):
            images[ship["name"]] = None

    return images
