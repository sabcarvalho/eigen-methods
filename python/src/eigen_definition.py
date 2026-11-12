"""Symbolic calculation of eigenvalues and eigenvectors via SymPy."""
from sympy import Symbol, eye
from numpy import shape
from .determinant import determinant


def eigenvector(d, mat_aux, mat_p, dim):
    """Construct the eigenvector associated with the eigenvalue at index d (using Gaussian elimination)."""
    for k in range(dim - 1):
        if mat_aux[k][k] == 0:
            for d1 in range(k + 1, dim):
                if mat_aux[d1][k] != 0:
                    mat_aux[[k, d1]] = mat_aux[[d1, k]]
                    break
        for e in range(k + 1, dim):
            if mat_aux[k][k] != 0:
                m = mat_aux[e][k] / mat_aux[k][k]
                mat_aux[e][k] = 0
                for f in range(k + 1, dim):
                    mat_aux[e][f] = mat_aux[e][f] - m * mat_aux[k][f]

    if mat_aux[dim - 1][dim - 1].simplify() != 0:
        mat_p[dim - 1, d] = 0
    else:
        mat_p[dim - 1, d] = 1

    for e in range(dim - 2, -1, -1):
        aux = 0
        for f in range(dim - 1, e, -1):
            aux = aux + mat_p[f, d] * mat_aux[e][f]
        if mat_aux[e][e] != 0:
            aux = aux / mat_aux[e][e]
            mat_p[e, d] = -aux.simplify()
        else:
            mat_p[e, d] = 1

def characteristic_polynomial(a):
    """Returns the characteristic polynomial of A in factored form (a SymPy expression)."""
    dim = shape(a)[0]
    mat_aux = a.astype(object).copy()
    lamb = Symbol('x')
    for i in range(dim):
        mat_aux[i][i] -= lamb
    return determinant(dim, mat_aux).factor()

def main(a, verbose=True):
    dim = shape(a)[0]

    poly = characteristic_polynomial(a)
    eigenvalues = poly.as_poly(domain='QQ').all_roots()

    mat_p = eye(dim)
    mat_aux = a.astype(object)
    for d, lamb in enumerate(eigenvalues):
        for i in range(dim):
            for j in range(dim):
                mat_aux[i][j] = a[i][j]
                if i == j:
                    mat_aux[i][j] = a[i][j] - lamb
        eigenvector(d, mat_aux, mat_p, dim)
    try:
        inv = mat_p.inv()
        D = inv * a * mat_p
        for i in range(dim):
            for j in range(dim):
                D[i, j] = D[i, j].simplify()
    
        if verbose:
            print(f'Characteristic polynomial: {poly}')
            print(f'Eigenvalues: {eigenvalues}')
            print('\nP:')
            print(mat_p)
            print('\nP^(-1):')
            print(inv)
            print('\nD = P⁻¹ A P:')
            print(D)
    
        return {
            'poly': poly,
            'eigenvalues': eigenvalues,
            'P': mat_p,
            'D': D,
        }
    except Exception as e:
        return {
            'poly': poly,
            'eigenvalues': eigenvalues,
            'P': [],
            'D': [],
        }
    
    
    