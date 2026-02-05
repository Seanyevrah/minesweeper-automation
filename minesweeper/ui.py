import pygame
from .constants import *

def button(text, position, screen):
    rect = pygame.Rect(position, (180, 40))
    pygame.draw.rect(screen, DARK_GRAY, rect)
    text_surface = FONT_SMALL.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect