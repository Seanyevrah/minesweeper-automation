import random
import time
import pickle
from collections import deque
from .cell import Cell
from .constants import *
from minesweeper.utils import show_message

class Minesweeper:
    def __init__(self, difficulty='easy'):
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.grid_size = settings['size']
        self.mine_count = settings['mines']
        self.time_limit = settings['time']
        self.start_time = time.time()
        self.elapsed_time = 0
        self.grid = [[Cell(x, y) for y in range(self.grid_size)] for x in range(self.grid_size)]
        self.place_mines()
        self.calculate_adjacent_mines()
        self.revealed_cells = 0
        self.moves = 0
        self.game_over = False
        self.won = False
        self.flags_used = 0
        self.offset_x = (WINDOW_WIDTH - self.grid_size * CELL_SIZE) // 2
        self.offset_y = (WINDOW_HEIGHT - self.grid_size * CELL_SIZE) // 2
        self.first_click = True

    def place_mines(self):
        all_positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        mine_positions = random.sample(all_positions, self.mine_count)
        for x, y in mine_positions:
            self.grid[x][y].is_mine = True

    def calculate_adjacent_mines(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if not self.grid[x][y].is_mine:
                    self.grid[x][y].adjacent_mines = self.count_adjacent_mines(x, y)

    def count_adjacent_mines(self, x, y):
        count = 0
        for i in range(max(0, x - 1), min(self.grid_size, x + 2)):
            for j in range(max(0, y - 1), min(self.grid_size, y + 2)):
                if self.grid[i][j].is_mine:
                    count += 1
        return count

    def reveal_cell(self, x, y, screen, clock):
        if self.grid[x][y].flagged or self.grid[x][y].revealed:
            return

        if self.first_click:
            self.first_click = False

        if self.grid[x][y].is_mine:
            self.game_over = True
            self.reveal_all_mines(screen, clock)
            return

        self.flood_fill(x, y)
        self.moves += 1
        self.check_win()


    def reveal_all_mines(self, screen, clock):
        mines = [(cell.x, cell.y) for row in self.grid for cell in row if cell.is_mine]
        for x, y in mines:
            self.grid[x][y].revealed = True
            self.draw(screen, show_mines=True)  
            pygame.display.flip()
            clock.tick(10)


    def flood_fill(self, x, y):
        queue = deque([(x, y)])
        while queue:
            cx, cy = queue.popleft()
            if self.grid[cx][cy].revealed:
                continue
            self.grid[cx][cy].revealed = True
            self.revealed_cells += 1
            if self.grid[cx][cy].adjacent_mines == 0:
                for nx in range(max(0, cx - 1), min(self.grid_size, cx + 2)):
                    for ny in range(max(0, cy - 1), min(self.grid_size, cy + 2)):
                        if not self.grid[nx][ny].revealed and not self.grid[nx][ny].is_mine:
                            queue.append((nx, ny))

    def toggle_flag(self, x, y):
        if not self.grid[x][y].revealed:
            self.grid[x][y].flagged = not self.grid[x][y].flagged
            self.flags_used += 1 if self.grid[x][y].flagged else -1
            self.moves += 1

    def check_win(self):
        if self.revealed_cells + self.mine_count == self.grid_size ** 2:
            self.won = True
            self.game_over = True

    def get_time_remaining(self):
        current_elapsed = time.time() - self.start_time
        total_elapsed = self.elapsed_time + current_elapsed
        remaining_time = max(0, round(self.time_limit - total_elapsed))
        if remaining_time == 0 and not self.won:
            self.game_over = True
        return remaining_time
    
    def save_game(self, filepath="savegame.pkl"):
        self.elapsed_time += time.time() - self.start_time
        with open(filepath, "wb") as file:
            pickle.dump(self, file)
        print("Game saved successfully!")
    
    @classmethod
    def load_game(cls, filepath="savegame.pkl"):
        with open(filepath, "rb") as file:
            game = pickle.load(file)
        game.start_time = time.time()
        print("Game loaded successfully!")
        return game

    def draw(self, screen, show_mines=False):
        screen.fill(BLACK)
        for row in self.grid:
            for cell in row:
                cell.draw(screen, self.offset_x, self.offset_y, show_mine=show_mines)
        timer_text = FONT.render(f"Time: {int(self.get_time_remaining())}", True, WHITE)
        mines_text = FONT.render(f"Mines Remaining: {self.mine_count - self.flags_used}", True, WHITE)
        moves_text = FONT.render(f"Moves Made: {self.moves}", True, WHITE)
        screen.blit(timer_text, (WINDOW_WIDTH - 320, 120))
        screen.blit(mines_text, (200, WINDOW_HEIGHT - 150))
        screen.blit(moves_text, (200, WINDOW_HEIGHT - 200))
    
    def solve_board(self, screen, clock):
        changes_made = True
        while changes_made and not self.game_over:
            changes_made = False
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    cell = self.grid[x][y]
                    if cell.revealed and cell.adjacent_mines > 0:
                        flagged_count = 0
                        unrevealed_neighbors = []

                        # Gather information about neighboring cells
                        for nx in range(max(0, x - 1), min(self.grid_size, x + 2)):
                            for ny in range(max(0, y - 1), min(self.grid_size, y + 2)):
                                neighbor = self.grid[nx][ny]
                                if neighbor.flagged:
                                    flagged_count += 1
                                elif not neighbor.revealed:
                                    unrevealed_neighbors.append(neighbor)

                        # If all mines are flagged, reveal safe neighbors
                        if flagged_count == cell.adjacent_mines:
                            for neighbor in unrevealed_neighbors:
                                if not neighbor.revealed and not neighbor.flagged:
                                    self.reveal_cell(neighbor.x, neighbor.y, screen, clock)
                                    changes_made = True
                                    self.draw(screen)
                                    pygame.display.flip()
                                    clock.tick(10)

                        # If unrevealed neighbors equal remaining mines, flag them
                        elif len(unrevealed_neighbors) == cell.adjacent_mines - flagged_count:
                            for neighbor in unrevealed_neighbors:
                                if not neighbor.flagged:
                                    neighbor.flagged = True
                                    self.flags_used += 1
                                    changes_made = True
                                    self.draw(screen)
                                    pygame.display.flip()
                                    clock.tick(10)

            # Break the loop if no changes were made
            if not changes_made:
                break

            # Check if the board is solved
            self.check_win()
            if self.game_over:
                break

        # If the solving process is completed but the game isn't over, show a message
        if not self.game_over:
            show_message("Solve Attempt", "Solving attempt finished. Some cells may still need manual intervention.")