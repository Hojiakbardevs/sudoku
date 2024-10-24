import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass
import random

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

        self.board = [[None for _ in range(9)] for _ in range(9)]  # Bo'sh tarmoq yaratish
        self.entries = []
        self.create_grid()

        solve_button = tk.Button(self.root, text="Solve Sudoku", command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=3, sticky="nsew")  # Solve button

        random_button = tk.Button(self.root, text="Randomize Board", command=self.randomize_board)
        random_button.grid(row=9, column=3, columnspan=3, sticky="nsew")  # Random button

        clear_button = tk.Button(self.root, text="Clear Board", command=self.clear_board)  # Clear button yaratish
        clear_button.grid(row=9, column=6, columnspan=3, sticky="nsew")  # Clear button joylash

    def create_grid(self):
        """Sudoku tarmog'ini yaratish"""
        for row in range(9):
            entry_row = []
            for col in range(9):
                entry = tk.Entry(self.root, width=5, justify="center")
                entry.grid(row=row, column=col, padx=1, pady=1, ipady=5)
                entry_row.append(entry)
            self.entries.append(entry_row)

    def randomize_board(self):
        """Sudoku tarmog'ini random raqamlar bilan to'ldirish"""
        self.clear_board()  # Oldingi tarmoqni tozalash
        self.fill_board_random()  # To'g'ri random tarmoq yaratish

    def clear_board(self):
        """Tarmoqni tozalash"""
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].config(state="normal")  # Tahrir qilinadigan qilib qo'yish
                self.board[row][col] = None

    def fill_board_random(self):
        """Sudoku tarmog'ini random holda to'g'ri raqamlar bilan to'ldirish"""
        numbers = list(range(1, 10))  # 1 dan 9 gacha bo'lgan raqamlar ro'yxati
        for i in range(9):
            for j in range(9):
                random.shuffle(numbers)  # Har safar ro'yxatni randomlashtiramiz
                for num in numbers:
                    if self.is_safe(Cell(i, j), num):  # Agar raqam xavfsiz bo'lsa, joylashamiz
                        self.board[i][j] = num
                        self.entries[i][j].insert(0, str(num))
                        self.entries[i][j].config(state="readonly")  # O'qiladigan qilib qo'yish
                        break

    def solve(self):
        """Sudoku ni yechish va natija qaytarish"""
        if self.solve_sudoku():
            self.update_grid()
            self.show_result(success=True)
        else:
            self.show_result(success=False)

    def solve_sudoku(self):
        """Sudoku yechish algoritmi"""
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
        """Sudoku qoidasiga mos kelishini tekshirish"""
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
