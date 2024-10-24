# https://mathspp.com/blog

from dataclasses import dataclass


@dataclass
class Cell:
    """Class that represents a Sudoku board cell."""

    row: int
    col: int

    def __str__(self):
        return f"<{self.__class__.__name__}(row={self.row}, col={self.col})>"


class SudokuBoard:
    """Class that represents a Sudoku board."""

    def __init__(self, board):
        self._board = [row[:] for row in board]

    def __str__(self):
        thin = "│"
        thick = "┃"
        top_row = "┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓\n"
        thin_mid_row = "┠───┼───┼───╂───┼───┼───╂───┼───┼───┨\n"
        thick_mid_row = "┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫\n"
        bottom_row = "┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛\n"
        result = top_row
        for idx, values in enumerate(self._board):
            bot = (
                bottom_row
                if idx == 8
                else thick_mid_row if (idx % 3) == 2 else thin_mid_row
            )
            str_values = [
                f" {value} " if value is not None else "   " for value in values
            ]
            result = (
                result
                + thick
                + thick.join(
                    thin.join(str_values[3 * i : 3 * (i + 1)]) for i in range(3)
                )
                + thick
                + "\n"
                + bot
            )
        return result

    def _get_row_values(self, cell):
        return self._board[cell.row][:]

    def _get_col_values(self, cell):
        return [self._board[row][cell.col] for row in range(9)]

    def _get_square_values(self, cell):
        x = 3 * (cell.col // 3)
        y = 3 * (cell.row // 3)
        return [self._board[y + dy][x + dx] for dy in range(3) for dx in range(3)]

    def _get_competing_values(self, cell):
        return (
            set(filter(None, self._get_row_values(cell)))
            | set(filter(None, self._get_col_values(cell)))
            | set(filter(None, self._get_square_values(cell)))
        )

    def get_possible_values(self, cell):
        """Returns a list of the legal values that could fit in the given cell."""
        return sorted(set(range(1, 10)) - self._get_competing_values(cell))

    def get_vacant_cell(self):
        """Get the position of the first vacant cell or `None` if the board is full."""
        for row_idx, row in enumerate(self._board):
            for col_idx, value in enumerate(row):
                if value is None:
                    return Cell(row_idx, col_idx)
        return None

    def put(self, cell, value):
        """Create a copy of this board with the given value in the given position."""
        board = [row[:] for row in self._board]
        board[cell.row][cell.col] = value
        return SudokuBoard(board)


_board = [
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
sudoku = SudokuBoard(_board)

# print(sudoku)
# print(sudoku.get_vacant_cell())

# cell = sudoku.get_vacant_cell()
# print(sudoku.get_possible_values(cell))


cell = sudoku.get_vacant_cell()
new_sudoku = sudoku.put(cell, 1)
print(new_sudoku)
