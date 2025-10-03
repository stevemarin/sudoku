from itertools import product

import numpy as np

easy = """
    0 5 6   4 7 3   2 0 0
    0 2 9   0 0 0   7 8 0
    0 0 0   0 0 2   0 3 6

    7 9 0   0 2 0   0 0 0
    1 0 5   0 0 0   8 6 2
    6 0 0   8 3 0   0 7 1

    0 0 0   3 0 0   4 2 8
    5 7 4   0 0 0   6 0 0
    0 0 3   6 9 4   0 0 0
"""

medium = """
    9 0 0   0 0 0   4 0 6
    0 7 0   0 9 0   0 2 8
    8 0 3   0 0 0   1 0 0

    0 6 0   4 0 0   0 0 0
    0 0 0   0 0 2   0 0 0
    0 0 7   0 0 0   0 0 1

    0 0 5   3 4 0   0 6 0
    0 0 4   6 0 9   0 5 2
    0 0 0   0 5 0   0 0 0
"""


class Puzzle:
    def __init__(self, puzzle: str) -> None:
        self.data = np.array([int(c) for c in puzzle if "0" <= c <= "9"], dtype=np.int8).reshape((9, 9))

    def __str__(self) -> str:
        s = ""
        for row_idx, row in enumerate(self.data):
            for col_idx, v in enumerate(row):
                if col_idx == 2 or col_idx == 5:
                    s += f"{v}   "
                elif col_idx == 8:
                    s += f"{v}\n"
                else:
                    s += f"{v} "
            if row_idx == 2 or row_idx == 5:
                s += "\n"
        return s

    def _row(self, row: int) -> np.ndarray:
        return self.data[row, :]

    def _col(self, col: int) -> np.ndarray:
        return self.data[:, col]

    def _box(self, row: int, col: int) -> np.ndarray:
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        return self.data[start_row : start_row + 3, start_col : start_col + 3]

    def _allowed(self, row: int, col: int) -> set[int]:
        parts = self._row(row), self._col(col), self._box(row, col).flatten()
        not_allowed = {int(v) for sublist in parts for v in sublist if v != 0}
        return set(range(1, 10)) - not_allowed

    def solve_one(self) -> tuple[int, int, int] | None:
        for row, col in product(range(9), range(9)):
            if self.data[row, col] != 0:
                continue
            a = self._allowed(row, col)
            if len(a) == 1:
                return row, col, a.pop()
        else:
            return None

    def solve(self) -> None:
        while True:
            try:
                r, c, v = self.solve_one()
                assert self.data[r, c] == 0
                print(f"({r}, {c}) = {v}")
                self.data[r, c] += v
            except TypeError:
                break


if __name__ == "__main__": 
    puzzle = Puzzle(medium)
    puzzle.solve()
    print(puzzle)
