import pygame
import pickle
from minesweeper.game import Minesweeper
from minesweeper.ui import button
from minesweeper.constants import *
from minesweeper.utils import show_message

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Minesweeper")

    game_state = 'start'
    difficulty = 'easy'
    game = None
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)
        
        if game_state == 'start':
            title_text = FONT.render("Minesweeper Puzzle", True, WHITE)
            screen.blit(title_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100))
            start_button = button("Start Game", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 - 50), screen)
            load_button = button("Load Last Game", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2), screen)
            instructions_button = button("Instructions", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 50), screen)
            exit_button = button("Exit", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 100), screen)

        elif game_state == 'instructions':
            instructions_text = [
                "Instructions for Minesweeper:",
                "1. The board contains hidden mines.",
                "2. Click a cell to reveal it.",
                "3. Numbers indicate how many mines are nearby.",
                "4. Right-click to place or remove a flag.",
                "5. Flag all mines to win, or avoid clicking them.",
                "6. You can request a solution or restart anytime.",
                "7. Save your progress and load it later.",
            ]

            y_offset = WINDOW_HEIGHT // 2 - 130
            for line in instructions_text:
                instruction_line = FONT_SMALL.render(line, True, WHITE)
                screen.blit(instruction_line, (WINDOW_WIDTH // 2 - 190, y_offset))
                y_offset += 40

            back_button = button("Back", (WINDOW_WIDTH - 370, WINDOW_HEIGHT - 150), screen)

        elif game_state == 'difficulty':
            difficulty_text = FONT.render("Select Difficulty", True, WHITE)
            screen.blit(difficulty_text, (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 100))
            easy_button = button("Easy", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 - 50), screen)
            medium_button = button("Medium", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2), screen)
            hard_button = button("Hard", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 50), screen)
            back_button = button("Back", (WINDOW_WIDTH - 370, WINDOW_HEIGHT - 150), screen)

        elif game_state == 'game':
            game.draw(screen)
            restart_button = button("Restart", (200, 120), screen)
            save_button = button("Save Game", (390, 120), screen)
            hint_button_y_position = game.offset_y + game.grid_size * CELL_SIZE + 10
            request_solution_button = button("Hint", (870, hint_button_y_position), screen)
            solution_button = button("Request Solution", (870, hint_button_y_position + 50), screen)
            return_button = button("Return Main Menu", (WINDOW_WIDTH - 370, WINDOW_HEIGHT - 150), screen)
            back_button = button("Back", (WINDOW_WIDTH - 370, WINDOW_HEIGHT - 200), screen)

            if game.get_time_remaining() == 0 and not game.won:
                game_state = 'game_over'

            if game.game_over:
                if game.won:
                    game_state = 'win'
                else:
                    game_state = 'game_over'

        elif game_state == 'solution':
            game.draw(screen, show_mines=True)  # Reveals mines in solution mode
            solution_text = FONT.render("Solution View", True, YELLOW)
            solution_text_rect = solution_text.get_rect(
                center=(game.offset_x + game.grid_size * CELL_SIZE // 2, game.offset_y - 50)
            )
            screen.blit(solution_text, solution_text_rect)
            back_button = button("Back", (WINDOW_WIDTH - 370, WINDOW_HEIGHT - 150), screen)

        elif game_state == 'game_over':
            game_over_text = FONT.render("Game Over!", True, RED)
            try_again_button = button("Try Again", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 - 50), screen)
            return_button = button("Return Main Menu", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2), screen)
            screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 55, WINDOW_HEIGHT // 2 - 90))

        elif game_state == 'win':
            win_text = FONT.render("You Win!", True, GREEN)
            screen.blit(win_text, (WINDOW_WIDTH // 2 - 40, WINDOW_HEIGHT // 2 - 90))
            retry_button = button("Retry", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 - 50), screen)
            return_button = button("Return Main Menu", (WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2), screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if game_state == 'start':
                    if start_button.collidepoint(x, y):
                        game_state = 'difficulty'
                    if load_button.collidepoint(x, y):
                        try:
                            game = Minesweeper.load_game()
                            game_state = 'game'
                            show_message("Load Game", "Game loaded successfully!")
                        except (FileNotFoundError, pickle.UnpicklingError):
                            show_message("Load Game", "No saved game found or corrupted save file.")
                    elif instructions_button.collidepoint(x, y):
                        game_state = 'instructions'
                    elif exit_button.collidepoint(x, y):
                        running = False
                elif game_state == 'instructions':
                    if back_button.collidepoint(x, y):
                        game_state = 'start'
                elif game_state == 'difficulty':
                    if easy_button.collidepoint(x, y):
                        difficulty = 'easy'
                        game = Minesweeper(difficulty)
                        game_state = 'game'
                    elif medium_button.collidepoint(x, y):
                        difficulty = 'medium'
                        game = Minesweeper(difficulty)
                        game_state = 'game'
                    elif hard_button.collidepoint(x, y):
                        difficulty = 'hard'
                        game = Minesweeper(difficulty)
                        game_state = 'game'
                    elif back_button.collidepoint(x, y):
                        game_state = 'start'
                elif game_state == 'game':
                    if restart_button.collidepoint(x, y):
                        game = Minesweeper(difficulty)
                    elif save_button.collidepoint(x, y):
                        try:
                            game.save_game()
                            show_message("Save Game", "Game saved successfully!")
                        except Exception as e:
                            show_message("Error", f"Failed to save game: {e}")
                    elif request_solution_button.collidepoint(x, y):
                        game_state = 'solution'
                    elif solution_button.collidepoint(x, y):
                        if game.first_click:
                            show_message("Error", "Reveal a cell first!")
                        else:
                            game.solve_board(screen, clock)
                    elif game.get_time_remaining() == 0 or game.game_over:
                        if not game.won:
                            game.reveal_all_mines(screen, clock)
                            game_state = 'game_over'
                    elif return_button.collidepoint(x, y):
                        game_state = 'start'
                    elif back_button.collidepoint(x, y):
                        game_state = 'difficulty'
                    else:
                        grid_x, grid_y = (x - game.offset_x) // CELL_SIZE, (y - game.offset_y) // CELL_SIZE
                        if 0 <= grid_x < game.grid_size and 0 <= grid_y < game.grid_size:
                            if event.button == 1:
                                game.reveal_cell(grid_x, grid_y, screen, clock)
                            elif event.button == 3:
                                game.toggle_flag(grid_x, grid_y)
                elif game_state == 'solution' and back_button.collidepoint(x, y):
                    game_state = 'game'
                elif game_state == 'game_over':
                    if try_again_button.collidepoint(x, y):
                        game = Minesweeper(difficulty)
                        game_state = 'game'
                    elif return_button.collidepoint(x, y):
                        game_state = 'start'
                elif game_state == 'win':
                    if retry_button.collidepoint(x, y):
                        game = Minesweeper(difficulty)
                        game_state = 'game'
                    elif return_button.collidepoint(x, y):
                        game_state = 'start'

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()