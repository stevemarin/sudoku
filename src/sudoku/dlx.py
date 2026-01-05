from itertools import product

import numpy as np
import scipy.sparse

ROOT_SIZE = 2
SIZE = ROOT_SIZE * ROOT_SIZE
SIZE_SQUARED = SIZE * SIZE


def build_constraints() -> scipy.sparse.dok_array:
    """build matrix of constraints for exact cover algorithm"""
    num_rows = SIZE_SQUARED * SIZE
    num_cols = SIZE_SQUARED * 4

    mat = scipy.sparse.dok_array((num_rows, num_cols), dtype=np.uint8)
    for idx, (row, col, val) in enumerate(product(range(SIZE), repeat=3)):
        # row and col intersect on a single value
        mat[idx, 0 * SIZE_SQUARED + row * SIZE + col] = 1
        # each row, col, and box can only contain each value once
        mat[idx, 1 * SIZE_SQUARED + val + SIZE * row] = 1
        mat[idx, 2 * SIZE_SQUARED + val + SIZE * col] = 1
        box = (row // ROOT_SIZE) * ROOT_SIZE + col // ROOT_SIZE
        mat[idx, 3 * SIZE_SQUARED + val + SIZE * box] = 1

    assert isinstance(mat, scipy.sparse.dok_array)
    return mat


def row_to_rcv(row: scipy.sparse.csr_array) -> tuple[int, int, int]:
    """converts a row in the constraint matrix to the corresponding puzzle row, col, and value"""
    assert isinstance(row, scipy.sparse.csr_array)
    assert row.sum() == 4

    assert (tmp := row[:SIZE_SQUARED]).sum() == 1
    r, c = divmod(tmp.argmax(), SIZE)

    assert (tmp := row[SIZE_SQUARED : 2 * SIZE_SQUARED]).sum() == 1
    v = tmp.argmax() % SIZE

    return r, c, v


def solve(
    mat: scipy.sparse.dok_array,
    soln: dict[tuple[int, int], int] = {},
    rng: np.random.Generator = np.random.default_rng(),
):
    assert isinstance(mat, scipy.sparse.dok_array)
    assert mat.sum(axis=None) % 4 == 0

    if int(mat.sum(axis=None)) == 0:
        print("solved")
        return True, mat, soln

    row_sums = mat.sum(axis=0)
    min_val = row_sums[row_sums > 0].min()
    col = rng.choice(np.argwhere(row_sums == min_val).squeeze())
    row = rng.choice(mat[:, col].coords[0])

    # import pdb
    # pdb.set_trace()

    assert mat[row, col] == 1
    r, c, v = row_to_rcv(mat[row].tocsr())
    print(row + 1, v + 1, r + 1, c + 1)
    assert (r, c) not in soln
    soln[(r, c)] = v

    
    print(mat[4])


def cover():
    pass


def uncover():
    pass


if __name__ == "__main__":
    mat = build_constraints()
    # solved, mat, soln = solve(mat)
    solve(mat)

    # import matplotlib.pyplot as plt
    # import seaborn as sns

    # sns.heatmap(mat.todense())
    # plt.show()
