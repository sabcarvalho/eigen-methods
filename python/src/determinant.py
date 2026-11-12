"""Determinant calculation (Laplace expansion) with support for symbolic variables."""
from numpy import identity

def determinant(dim, mat):
    """Determinant of an n x n matrix (accepts symbolic inputs)."""
    if dim == 1:
        return mat[0][0]

    mat_aux = identity(dim, dtype='object')
    if dim == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]

    p = 0
    for k in range(dim):
        a = 0
        b = 0
        for c in range(1, dim):
            for d in range(dim):
                if d != k:
                    mat_aux[a][b] = mat[c][d]
                    b += 1
            a += 1
            b = 0
        p = p + (-1) ** k * mat[0][k] * determinant(dim - 1, mat_aux)
    return p