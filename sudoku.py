# The MIT License (MIT)

# Copyright (c) 2025 Bachi Peachy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import random

import toga
from toga.colors import RED, BLACK, rgba, GREEN
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from travertino.constants import PURPLE


class SudokuApp(toga.App):
    def startup(self):
        self.editable_mask = [[False] * 9 for _ in range(9)]
        self.solution_board = [[0] * 9 for _ in range(9)]
        self.selected_cell = None

        self.main_box = toga.Box(style=Pack(direction=ROW, margin=10, align_items=CENTER))

        self.difficulty_select = toga.Selection(items=["Easy", "Medium", "Hard"],
                                                style=Pack(width=120, margin=(0, 0, 10, 0)))
        self.new_game_btn = toga.Button("New Game", on_press=self.new_game, style=Pack(margin=5, width=120))
        self.solve_btn = toga.Button("Check Solution", on_press=self.check_solution, style=Pack(margin=5, width=120))
        self.reveal_btn = toga.Button("Show Solution", on_press=self.show_solution, style=Pack(margin=5, width=120))
        control_row = toga.Box(style=Pack(direction=ROW, margin=5))
        for w in [self.difficulty_select, self.new_game_btn, self.solve_btn, self.reveal_btn]:
            w.style.margin = 6
            control_row.add(w)
        left_controls = toga.Box(style=Pack(direction=COLUMN, align_items=CENTER, margin_top=20, margin_right=20))
        for w in [self.difficulty_select, self.new_game_btn, self.solve_btn, self.reveal_btn]:
            w.style.margin = 6
            left_controls.add(w)
        main_controls = toga.Box(style=Pack(direction=ROW, margin=10, align_items=CENTER))
        main_controls.add(left_controls)

        self.grid = []
        grid_box = toga.Box(style=Pack(direction=COLUMN, margin=10, align_items=CENTER))
        for r in range(9):
            row_box = toga.Box(style=Pack(direction=ROW))
            row = []
            for c in range(9):
                cell = toga.TextInput(
                    placeholder="",
                    on_change=self.handle_change,
                    style=Pack(width=40, height=40, font_size=20, text_align=CENTER, margin=0)
                )
                block_id = (r // 3) * 3 + (c // 3)
                bg_color = rgba(245, 245, 245, 1.0) if block_id % 2 == 0 else rgba(225, 225, 225, 1.0)
                cell.style.background_color = bg_color
                cell.style.color = BLACK
                if c % 3 == 0:
                    cell.style.border_left = ("3px", BLACK)
                else:
                    cell.style.border_left = ("1px", rgba(100, 100, 100, 0.3))
                if r % 3 == 0:
                    cell.style.border_top = ("3px", BLACK)
                else:
                    cell.style.border_top = ("1px", rgba(100, 100, 100, 0.3))
                if c == 8:
                    cell.style.border_right = ("3px", BLACK)
                if r == 8:
                    cell.style.border_bottom = ("3px", BLACK)
                row.append(cell)
                row_box.add(cell)
            self.grid.append(row)
            grid_box.add(row_box)

        self.status_label = toga.Label("Ready. Press New Game", style=Pack(font_size=12, margin_top=20))
        main_split = toga.Box(style=Pack(direction=ROW, align_items=CENTER))
        left_column = toga.Box(style=Pack(direction=COLUMN, margin_right=20, align_items="start"))
        for w in [self.difficulty_select, self.new_game_btn, self.solve_btn, self.reveal_btn]:
            w.style.margin = 6
            left_column.add(w)
        main_split.add(left_column)
        main_split.add(grid_box)
        self.main_box.add(main_split)
        left_column.add(self.status_label)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()
        self.difficulty_select.value = "Easy"
        self.new_game_btn.on_press()

    def handle_change(self, widget):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == widget:
                    self.selected_cell = (r, c)
                    if not self.editable_mask[r][c]:
                        widget.value = str(self.grid[r][c].value)  # reject edit on protected cell
                        self.beep()
                        return
                    old_val = self.grid[r][c].value.strip()
                    val = widget.value.strip()
                    if val and (not val.isdigit() or not 1 <= int(val) <= 9):
                        widget.value = ""
                        self.beep()
                        return

    def beep(self):
        print("\a")

    def new_game(self, widget):
        difficulty = self.difficulty_select.value
        full_board = self.generate_full_solution()
        self.solution_board = [row[:] for row in full_board]

        puzzle = self.mask_board(full_board, difficulty)
        count = []
        for r in range(9):
            for c in range(9):
                val = puzzle[r][c]
                self.grid[r][c].on_change = None
                self.grid[r][c].value = str(val) if val != 0 else ""
                self.editable_mask[r][c] = (val == 0)
                self.grid[r][c].style.color = RED if val != 0 else BLACK
                self.grid[r][c].on_change = self.handle_change
        self.selected_cell = None
        self.status_label.text = f"New {difficulty} puzzle loaded."

    def generate_full_solution(self):
        board = [[0] * 9 for _ in range(9)]

        def is_valid(r, c, n):
            row = board[r]
            col = [board[i][c] for i in range(9)]
            block = [board[i][j] for i in range((r // 3) * 3, (r // 3) * 3 + 3) for j in
                     range((c // 3) * 3, (c // 3) * 3 + 3)]
            return n not in row and n not in col and n not in block

        def solve():
            for r in range(9):
                for c in range(9):
                    if board[r][c] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for n in nums:
                            if is_valid(r, c, n):
                                board[r][c] = n
                                if solve():
                                    return True
                                board[r][c] = 0
                        return False
            return True

        solve()
        return board

    def mask_board(self, board, difficulty):
        puzzle = [row[:] for row in board]
        clues = {
            "Easy": random.randint(40, 48),
            "Medium": random.randint(32, 40),
            "Hard": random.randint(24, 32),
        }.get(difficulty, 36)

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        while len(cells) > clues:
            r, c = cells.pop()
            puzzle[r][c] = 0
        return puzzle

    def check_solution(self, widget):
        errors = []
        incomplete = False

        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]
                user_val = cell.value.strip()

                if user_val == "":
                    incomplete = True
                    continue

                if not user_val.isdigit() or int(user_val) != self.solution_board[r][c]:
                    if self.editable_mask[r][c]:
                        cell.style.color = PURPLE
                    errors.append((r + 1, c + 1))
                else:
                    if self.editable_mask[r][c]:
                        cell.style.color = BLACK

        if errors:
            self.status_label.text = f"{len(errors)} incorrect entr{'y' if len(errors) == 1 else 'ies'} in Purple."
        elif incomplete:
            self.status_label.text = "Good progress! Puzzle is incomplete."
        else:
            self.status_label.text = "Congratulations! Puzzle is perfectly solved."

    def show_solution(self, widget):
        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]
                correct_val = str(self.solution_board[r][c])
                cell.on_change = None
                if not self.editable_mask[r][c]:
                    cell.value = correct_val
                    cell.style.color = RED
                else:
                    current_val = cell.value.strip()
                    if current_val != correct_val:
                        cell.value = correct_val
                        cell.style.color = GREEN
                    else:
                        cell.style.color = BLACK
                cell.on_change = self.handle_change
        self.status_label.text = "Solution shown. Green: Corrected Cells."


def main():
    return SudokuApp("Sudoku by Bachi", "com.github.bachipeachy.sudoku")


if __name__ == "__main__":
    app = main()
    app.main_loop()
