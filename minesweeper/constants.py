import pygame
import base64
from io import BytesIO

# Window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
CELL_SIZE = 30
MARGIN = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fonts
pygame.init()
FONT = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 28)

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {'size': 10, 'mines': 10, 'time': 300},
    'medium': {'size': 15, 'mines': 40, 'time': 180},
    'hard': {'size': 20, 'mines': 99, 'time': 60}
}

# Base64-encoded image strings
MINE_IMAGE_DATA = "iVBORw0KGgoAAAANSUhEUgAAAAsAAAALCAYAAACprHcmAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAD2EAAA9hAag/p2kAAABdSURBVChThY5LDoAwCERRN97/vqbOICWUEnkJ/4FWwEWXGBYjt8Vt2NXeYJxGXHhaJAdsAOYPHWDBvhLFU5jxpl770h5/AvwtqS6KSbVQ/xmWl1lvB3KjqxeKocgLQ4Uc/M2qoB4AAAAASUVORK5CYII"
FLAG_IMAGE_DATA = "iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAPUlEQVR42mP4//8/A7kYr+RbGZX/FGnGZwBRmnEZQLRmbAaQpBndAPrYTP/QHrhEQrJmQlFElM0UZQxCGAArMoZcpiuV4QAAAABJRU5ErkJggg"

# Helper function to add padding
def add_padding(base64_string):
    return base64_string + '=' * (-len(base64_string) % 4)

# Decode and load images from Base64
mine_image_data = BytesIO(base64.b64decode(add_padding(MINE_IMAGE_DATA)))
flag_image_data = BytesIO(base64.b64decode(add_padding(FLAG_IMAGE_DATA)))

MINE_IMAGE = pygame.image.load(mine_image_data)
MINE_IMAGE = pygame.transform.scale(MINE_IMAGE, (CELL_SIZE - MARGIN, CELL_SIZE - MARGIN))

FLAG_IMAGE = pygame.image.load(flag_image_data)
FLAG_IMAGE = pygame.transform.scale(FLAG_IMAGE, (CELL_SIZE - MARGIN, CELL_SIZE - MARGIN))