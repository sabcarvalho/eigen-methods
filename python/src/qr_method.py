"""QR method with Givens rotations."""
from numpy import identity, zeros, abs
from math import sqrt


def qr(a, dim, err):
    cont = 1
    max_val = 1
    while max_val > err and cont < 10200:
        matr = a.copy()
        matq = identity(dim)
        for i in range(1, dim):
            j = 0
            while j < i:
                if matr[i][j] != 0:
                    p, q = j, i
                    matU = identity(dim)
                    den = sqrt(matr[p][p] ** 2 + matr[q][p] ** 2)
                    coss = matr[p][p] / den
                    seno = matr[q][p] / den
                    matU[p][p] = coss
                    matU[q][q] = coss
                    matU[q][p] = -seno
                    matU[p][q] = seno
                    matr = matU @ matr
                    matq = matq @ matU.T
                j += 1
        a = matr @ matq
        max_val = 0
        for linha in range(1, dim):
            for coluna in range(linha):
                if abs(a[linha][coluna]) > max_val:
                    max_val = abs(a[linha][coluna])
        cont += 1
    return a, cont, max_val


def eigenvector_qr(matA, dim, multiplicity):
    """Eigenvector via Gaussian elimination (numerical)."""
    vet = zeros((dim, 1))
    for k in range(dim - 1):
        if abs(matA[k, k]) < 1e-7:
            for d1 in range(k + 1, dim):
                if abs(matA[d1, k]) > abs(matA[k, k]):
                    matA[[k, d1]] = matA[[d1, k]]
                    break
        for e in range(k + 1, dim):
            if matA[k][k] != 0:
                fator = matA[e][k] / matA[k][k]
                matA[e][k] = 0
                for f in range(k + 1, dim):
                    matA[e][f] -= fator * matA[k][f]

    vet[dim - 1][0] = 1 if abs(matA[dim - 1][dim - 1]) < 1e-5 and multiplicity == 0 else 0

    aux_mult = 1
    for e in range(dim - 2, -1, -1):
        aux = 0
        for f in range(dim - 1, e, -1):
            aux -= vet[f][0] * matA[e][f]
        aux = 1 if abs(matA[e][e]) < 1e-5 else aux / matA[e][e]
        vet[e][0] = aux
        if multiplicity > 0 and aux_mult <= multiplicity:
            vet[dim - aux_mult][0] = 0
            aux_mult += 1
    return vet


def main_qr(a, err, verbose=True):
    """Applies the QR method and returns a list of (eigenvalue, eigenvector) pairs."""
    dim = a.shape[0]
    ak, cont, max_val = qr(a.copy(), dim, err)
    if verbose:
        print(f'Iterations: {cont}')
        print(f'Err: {max_val}')
        print('Eigenvectors:')
        for i in range(dim):
            print(ak[i][i])

    results = []
    for d in range(dim):
        multiplicity = sum(
            1 for j in range(d) if abs(ak[d][d] - ak[j][j]) < 1e-7
        )
        mat_aux = a.astype(float).copy()
        for i in range(dim):
            mat_aux[i][i] = a[i][i] - ak[d][d]
        vet = eigenvector_qr(mat_aux, dim, multiplicity)
        results.append({'eigenvalue': ak[d][d], 'eigenvector': vet})
    return results