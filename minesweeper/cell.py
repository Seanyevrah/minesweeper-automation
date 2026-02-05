import pygame
from .constants import *

class Cell:
    def __init__(self, x, y, is_mine=False):
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.revealed = False
        self.flagged = False
        self.adjacent_mines = 0

    def draw(self, screen, offset_x, offset_y, show_mine=False):
        rect = pygame.Rect(
        self.x * CELL_SIZE + offset_x,
        self.y * CELL_SIZE + offset_y,
        CELL_SIZE - MARGIN,
        CELL_SIZE - MARGIN
        )
        color = GRAY if not self.revealed else WHITE
        pygame.draw.rect(screen, color, rect)
    
        # Show mine if revealed, in solution mode, or game over
        if (self.revealed or show_mine) and self.is_mine:
            screen.blit(MINE_IMAGE, rect.topleft)
        elif self.revealed:
        # Display the number of adjacent mines, centered in the cell
            if self.adjacent_mines > 0:
                text_surface = FONT_SMALL.render(str(self.adjacent_mines), True, BLACK)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
        elif self.flagged:
            # Display flag if cell is flagged
            screen.blit(FLAG_IMAGE, rect.topleft)