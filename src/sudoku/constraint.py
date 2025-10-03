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

hard = """
    9 5 0  6 0 3  0 0 7
    0 1 0  0 0 0  2 0 0
    7 0 0  0 0 0  0 6 0

    8 9 0  0 6 0  0 0 0
    0 0 0  0 5 0  0 0 0
    5 0 0  0 8 0  1 2 9

    0 3 0  0 1 0  0 0 0
    0 0 0  0 0 0  3 0 0
    0 0 0  7 0 0  0 8 5
"""

empty = " 0 " * 81


def read_puzzle(s: str) -> np.ndarray:
    return np.array([int(c) for c in s if "0" <= c <= "9"], dtype=np.int8).reshape((9, 9))


def to_str(d: np.ndarray) -> str:
    s = ""
    for row in range(9):
        s += f"{d[row][0:3]}  {d[row][3:6]}  {d[row][6:9]}\n"
        if (row + 1) % 3 == 0:
            s += "\n"
    return s

def allowed_to_str(allowed: dict) -> str:
    s = "|" + ("-" * 13 + "|") * 3 + "\n"
    for row in range(9):
        # s += "|" + ("-" * 13 + "|") * 3 + "\n"
        for row_minor in range(3):
            s += "| "
            for col in range(9):
                a = allowed[(row, col)]
                for col_minor in range(3):
                    val = (3 * row_minor) + col_minor + 1
                    if val in a:
                        s += str(val)
                    else:
                        s += " "
                if (col + 1) % 3 == 0:
                    s += " | "
                else:
                    s += " "
            s += "\n"
        if (row + 1) % 3 == 0:
            s += "|" + ("-" * 13 + "|") * 3 + "\n"
        else:
            s += "\n"
    return s 
                    


def get_row(d: np.ndarray, row: int) -> np.ndarray:
    return d[row, :]


def get_col(d: np.ndarray, col: int) -> np.ndarray:
    return d[:, col]


def get_box(d: np.ndarray, row: int, col: int) -> np.ndarray:
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    return d[start_row : start_row + 3, start_col : start_col + 3]


def get_allowed(d: np.ndarray, row: int, col: int) -> set[int]:
    parts = get_row(d, row), get_col(d, col), get_box(d, row, col).flatten()
    not_allowed = {int(v) for sublist in parts for v in sublist if v != 0}
    return set(range(1, 10)) - not_allowed


def is_solved(d: np.ndarray) -> bool:
    return 0 not in d and is_valid(d)


def is_valid(d: np.ndarray) -> bool:
    rows, cols, boxes = [[set() for _ in range(9)] for _ in range(3)]

    for row, col in zip(*d.nonzero()):
        val = d[row, col]
        if val == 0:
            continue
        elif val < 0 or val > 9:
            raise ValueError(f"invalid value at {row},{col}: {val}")

        box = (3 * (row // 3)) + (col // 3)
        if val in rows[row] or val in cols[col] or val in boxes[box]:
            return False

        rows[row].add(val)
        cols[col].add(val)
        boxes[box].add(val)

    return True


if __name__ == "__main__":
    d = read_puzzle(medium)

    allowed = {}
    for row, col in product(range(9), repeat=2):
        allowed[(row, col)] = get_allowed(d, row, col) if d[row, col] == 0 else set()

    for _ in range(30):
        if is_solved(d):
            break

        for (row, col), val in allowed.items():
            if val is None:
                continue
            if len(val) == 1:
                v = val.pop()
                d[(row, col)] = v
                for _row in range(9):
                    allowed[(_row, col)].discard(v)
                for _col in range(9):
                    allowed[(row, _col)].discard(v)
                _row, _col = 3 * (row // 3), 3 * (col // 3)
                for _row, _col in product(range(_row, _row + 3), range(_col, _col + 3)):
                    allowed[(_row, _col)].discard(v)

    print(is_valid(d), is_solved(d))
    print(to_str(d))

    print(allowed_to_str(allowed))