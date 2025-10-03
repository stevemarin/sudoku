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

numerals = set(range(1, 10))


def to_str(d: np.ndarray) -> str:
    s = ""
    for row in range(9):
        s += f"{d[row][0:3]}  {d[row][3:6]}  {d[row][6:9]}\n"
        if (row + 1) % 3 == 0:
            s += "\n"
    return s


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


def read_puzzle(s: str) -> np.ndarray:
    return np.array([int(c) for c in s if "0" <= c <= "9"], dtype=np.int8).reshape((9, 9))


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
    return numerals - not_allowed


def brute_force(d: np.ndarray, row: int = 0, col: int = 0, backtracks: int = 0):
    if is_solved(d):
        return d, is_solved(d), backtracks

    next_row = row + 1 if row != 8 else 0
    next_col = col if row != 8 else col + 1

    if d[row, col] != 0:
        return brute_force(d, next_row, next_col, backtracks)

    for allowed in get_allowed(d, row, col):
        d[row, col] = allowed
        d, solved, backtracks = brute_force(d, next_row, next_col, backtracks)
        if solved:
            return d, True, backtracks
        d[row, col] = 0

    return d, False, backtracks + 1


if __name__ == "__main__":
    d = read_puzzle(hard)
    d, solved, backtracks = brute_force(d)
    print(backtracks)
    print(to_str(d))
