from itertools import product

import numpy as np

"""
https://orca.cardiff.ac.uk/id/eprint/27746/1/LEWIS%20metaheuristics%20can%20solve%20sudoku%20puzzles.pdf
"""

"""
1 2
2 3
3 5
4 7
5 11
6 13
7 17
8 19
9 23
"""

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

numerals = set(range(1, 10))


def read_puzzle(s: str) -> np.ndarray:
    return np.array([int(c) for c in s if "0" <= c <= "9"], dtype=np.int8).reshape((9, 9))


def to_str(d: np.ndarray) -> str:
    s = ""
    for row in range(9):
        s += f"{d[row][0:3]}  {d[row][3:6]}  {d[row][6:9]}\n"
        if (row + 1) % 3 == 0:
            s += "\n"
    return s


def get_fixed(d: np.ndarray) -> set[tuple[int, ...]]:
    return {tuple(map(int, coord)) for coord in zip(*d.nonzero())}


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


def random_fill(d: np.ndarray) -> np.ndarray:
    for row, col in product((0, 3, 6), repeat=2):
        box = d[row : row + 3, col : col + 3].flatten()
        missing = np.array(list(numerals - set(box)))
        np.random.shuffle(missing)
        box[box == 0] = missing
        d[row : row + 3, col : col + 3] = box.reshape((3, 3))
    return d


def get_ml(d: np.ndarray) -> int:
    non_fixed = 81 - int(np.count_nonzero(d))
    return non_fixed * non_fixed


def get_cost(d: np.ndarray) -> int:
    cost = 0
    for row in range(9):
        cost += len(numerals - set(d[row].tolist()))

    for col in range(9):
        cost += len(numerals - set(d[:, col].tolist()))

    return cost


def swap_neighbors(d: np.ndarray, d2: np.ndarray, fixed: set[tuple[int, ...]]) -> None:
    d2[:] = d[:]
    while True:
        row, col, cell = np.random.choice(range(9), size=3, replace=True)
        row_offset = cell // 3
        col_offset = cell - 3 * row_offset
        row2 = 3 * (row // 3) + row_offset
        col2 = 3 * (col // 3) + col_offset
        if (row, col) != (row2, col2) and (row, col) not in fixed and (row2, col2) not in fixed:
            break

    d2[row, col], d2[row2, col2] = d2[row2, col2], d2[row, col]


if __name__ == "__main__":
    d = read_puzzle(empty)
    fixed = get_fixed(d)
    ml = pow(81 - len(fixed), 2)
    d = random_fill(d)
    d2 = np.empty_like(d)

    costs = np.empty(ml)
    for idx in range(ml):
        swap_neighbors(d, d2, fixed)
        costs[idx] = get_cost(d2)
    temperature = float(costs.var())
    t0 = temperature
    alpha = 0.9

    since_update, best_cost = 0, get_cost(d)
    for chain in range(int(1e6)):
        updated = False
        for _ in range(ml):
            swap_neighbors(d, d2, fixed)
            next_cost = get_cost(d2)
            if next_cost < best_cost:
                d[:] = d2[:]
                best_cost = next_cost
                updated = True
            elif np.random.random() < np.exp(-(next_cost - best_cost + 0.01) / temperature):
                # updated = True
                d[:] = d2[:]
                best_cost = next_cost

            if best_cost == 0:
                break
        
        if best_cost == 0:
            break

        if updated:
            since_update = 0
        else:
            since_update += 1

        if since_update >= 20:
            temperature = t0 / 2.0

        temperature *= alpha

        print("a", f"{chain:3}", f"{temperature:0.3f}", f"{best_cost:2}", since_update)

    print(to_str(d))
    print(is_valid(d))

    exit(0)
