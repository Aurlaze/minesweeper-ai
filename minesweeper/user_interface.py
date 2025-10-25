from minesweeper import core
from minesweeper import sprites
from typing import Callable
import pygame
from pygame.locals import MOUSEBUTTONUP, MOUSEBUTTONDOWN

# --- AI MODIFICATIONS ---
import random
import pygame.time

# Corrected import to match user's folder name 'ai'
from ai.solver import (
    find_safe_move,
    find_simple_moves,
    find_safest_guess,
)  # <-- IMPORT YOUR AI
# --- END AI MODIFICATIONS ---

try:
    from .user_interface_board import UserInterfaceBoard
    from .user_interface_score import UserInterfaceScore
    from .user_interface_face import UserInterfaceFace
    from .user_interface_frame import UserInterfaceFrame
except ImportError:
    from user_interface_board import UserInterfaceBoard
    from user_interface_score import UserInterfaceScore
    from user_interface_face import UserInterfaceFace
    from user_interface_frame import UserInterfaceFrame


class UserInterface:
    def __init__(
        self,
        rows: int,
        cols: int,
        mines: int,
        callback,
        shadow=2,
        grey=5,
        tile_sprite=sprites.TileBuilder(),
        score_sprite=sprites.ScoreBuilder(),
        face_sprite=sprites.FaceBuilder(),
    ):
        frame = UserInterfaceFrame(shadow=shadow, grey=grey)
        self._screen = self.init_screen(rows, cols, frame.offset)
        frame.draw(self._screen, rows * sprites.TileBuilder().build().mine.get_height())
        self._board = core.Board(rows, cols, mines)
        tmp = UserInterfaceBoard(
            self._board, tile_sprite.build(), frame.offset, callback
        )
        self._components = [
            tmp,
            UserInterfaceScore(
                self._board, score_sprite.build(), frame.offset, tmp.flagged
            ),
            UserInterfaceFace(
                self._board, face_sprite.build(), frame.offset, self.game_reset
            ),
        ]

        self.ai_is_solving = False

    # --- THIS IS THE HIJACKED FUNCTION (FASTER & SMARTER AI - FINAL FIX) ---
    def game_reset(self):
        # ... (keep the existing code for resetting, stopping, etc.) ...
        if self._board.is_game_over or self._board.is_game_finished:
            self._board.game_reset()
            [component.game_reset() for component in self._components]
            self.ai_is_solving = False
            return
        if self.ai_is_solving:
            self.ai_is_solving = False
            return

        self.ai_is_solving = True
        board_ui = self._components[0]

        tile_to_num = {
            str(core.BoardTile.one): 1,
            str(core.BoardTile.two): 2,
            str(core.BoardTile.three): 3,
            str(core.BoardTile.four): 4,
            str(core.BoardTile.five): 5,
            str(core.BoardTile.six): 6,
            str(core.BoardTile.seven): 7,
            str(core.BoardTile.eight): 8,
        }

        while self.ai_is_solving and not (
            self._board.is_game_over or self._board.is_game_finished
        ):
            # 1. Get the current board state
            known_clues = {}
            unknown_cells = []
            flagged_cells = []

            for r in range(self._board.rows):
                for c in range(self._board.cols):
                    tile = self._board._tiles[r][c]

                    if tile != core.BoardTile.unopened:
                        num_val = tile_to_num.get(str(tile), 0)
                        if num_val > 0:
                            known_clues[(r, c)] = num_val
                    else:
                        if board_ui._tiles[r][c] == board_ui._sprites.flag:
                            flagged_cells.append((r, c))
                        else:
                            unknown_cells.append((r, c))

            move_to_make = None  # Reset move for this turn

            # --- AI DECISION LOGIC (CORRECTED) ---

            # 2. Try the "Fast Brain" for safe moves
            new_safes, new_mines = find_simple_moves(
                self._board.rows,
                self._board.cols,
                known_clues,
                unknown_cells,
                flagged_cells,
            )

            if new_safes:
                move_to_make = random.choice(list(new_safes))

            # 3. If Fast Brain found no SAFE move, try the "Heavy Brain"
            if not move_to_make:
                safe_move_heavy = find_safe_move(
                    self._board.rows, self._board.cols, known_clues, unknown_cells
                )
                if safe_move_heavy:
                    move_to_make = safe_move_heavy

            # 4. If BOTH brains found no SAFE move, use the "Smart Guesstimator"
            if not move_to_make:
                move_to_make = find_safest_guess(
                    self._board.rows,
                    self._board.cols,
                    known_clues,
                    unknown_cells,
                    flagged_cells,
                    self._board.mines,  # Pass in total mines
                )
            # --- END AI LOGIC ---

            # 5. Make the move
            if move_to_make:
                board_ui.mouse_up_left(move_to_make[0], move_to_make[1])
            else:
                self.ai_is_solving = False  # AI is done (stuck or finished)

            # 6. Update screen and pause
            self.draw()
            pygame.display.flip()
            pygame.time.wait(10)  # Speed up the solving visual

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ai_is_solving = False
                    pygame.quit()
                    return

        # After the loop finishes, check if we won OR lost
        if self._board.is_game_finished:
            # We WON: Find the face and set it to "winner"
            for component in self._components:
                if isinstance(component, UserInterfaceFace):
                    component.img = component._sprites.winner
                    break
        elif self._board.is_game_over:
            # We LOST: Find the face and set it to "dead"
            for component in self._components:
                if isinstance(component, UserInterfaceFace):
                    component.img = component._sprites.dead
                    break

    def event_handler(self, event) -> None:
        if event.type == MOUSEBUTTONDOWN and self.ai_is_solving:
            self.ai_is_solving = False

        for component in self._components:
            if event.type == MOUSEBUTTONDOWN:
                component.mouse_down(event)
            if event.type == MOUSEBUTTONUP:
                component.mouse_up(event)

    def draw(self) -> bool:
        return any([component.draw(self._screen) for component in self._components])

    def init_screen(self, rows: int, cols: int, offset: int):
        rows, cols, offset = int(rows), int(cols), int(offset)
        self._screen = pygame.display.set_mode((10, 10))
        tiles = sprites.TileBuilder().build().eight
        score = sprites.ScoreBuilder().build().eight
        width = cols * tiles.get_width() + offset * 2
        height = rows * tiles.get_height() + score.get_height() + offset * 5
        return pygame.display.set_mode((width, height))
