import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass

@dataclass
class Cell:
    row: int
    col: int

class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.result_label = tk.Label(self.root, text="", fg="green", font=("Arial", 14))
        self.result_label.grid(row=10, column=0, columnspan=9)

        self.board = [
            [5, 3, None, None, 7, None, None, None, None],
            [6, None, None, 1, 9, 5, None, None, None],
            [None, 9, 8, None, None, None, None, 6, None],
            [8, None, None, None, 6, None, None, None, 3],
            [4, None, None, 8, None, 3, None, None, 1],
            [7, None, None, None, 2, None, None, None, 6],
            [None, 6, None, None, None, None, 2, 8, None],
            [None, None, None, 4, 1, 9, None, None, 5],
            [None, None, None, None, 8, None, None, 7, 9],
        ]

        self.entries = []
        self.create_grid()

        solve_button = tk.Button(self.root, text="Solve Sudoku", command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=9, sticky="nsew")

    def create_grid(self):
        for row in range(9):
            entry_row = []
            for col in range(9):
                entry = tk.Entry(self.root, width=5, justify="center")
                entry.grid(row=row, column=col, padx=1, pady=1, ipady=5)
                if self.board[row][col] is not None:
                    entry.insert(0, str(self.board[row][col]))
                    entry.config(state="readonly")
                entry_row.append(entry)
            self.entries.append(entry_row)

    def solve(self):
        """Sudoku ni yechish va natija qaytarish"""
        if self.solve_sudoku():
            self.update_grid()
            self.show_result(success=True)
        else:
            self.show_result(success=False)

    def solve_sudoku(self):
        """Bu yerda sizning sudoku yechish algoritmingiz ishlaydi"""
        vacant = self.get_vacant_cell()
        if not vacant:
            return True
        for num in range(1, 10):
            if self.is_safe(vacant, num):
                self.board[vacant.row][vacant.col] = num
                if self.solve_sudoku():
                    return True
                self.board[vacant.row][vacant.col] = None
        return False

    def is_safe(self, cell, num):
        row_vals = self._get_row_values(cell)
        col_vals = self._get_col_values(cell)
        sq_vals = self._get_square_values(cell)
        return num not in row_vals and num not in col_vals and num not in sq_vals

    def _get_row_values(self, cell):
        return self.board[cell.row][:]

    def _get_col_values(self, cell):
        return [self.board[row][cell.col] for row in range(9)]

    def _get_square_values(self, cell):
        x = 3 * (cell.col // 3)
        y = 3 * (cell.row // 3)
        return [self.board[y + dy][x + dx] for dy in range(3) for dx in range(3)]

    def get_vacant_cell(self):
        for row_idx, row in enumerate(self.board):
            for col_idx, value in enumerate(row):
                if value is None:
                    return Cell(row_idx, col_idx)
        return None

    def update_grid(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(self.board[row][col]))

    def show_result(self, success):
        """Yechim natijasini ko'rsatish"""
        if success:
            self.result_label.config(text="Sudoku to'g'ri yechildi!", fg="green")
        else:
            self.result_label.config(text="Sudoku yechilolmadi!", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()
