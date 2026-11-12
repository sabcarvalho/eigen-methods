"""Householder reduction to tridiagonal form."""
from sympy import zeros, identity
from numpy import sqrt


def householder(a, dim):
    iden = identity(dim, dtype="float")
    for k in range(dim - 1):
        w = zeros((dim, 1), dtype="float")
        somatorio = sum(a[i][k] ** 2 for i in range(k + 1, dim))
        alfa = sqrt(somatorio)
        if a[k + 1][k] == 0:
            alfa = -alfa
        else:
            alfa = -1 * (a[k + 1][k] / abs(a[k + 1][k])) * alfa
        r = 2 * sqrt(alfa ** 2 / 2 - alfa * a[k + 1][k] / 2)
        w[k + 1][0] = (a[k + 1][k] - alfa) / r
        for j in range(k + 2, dim):
            w[j][0] = a[j][k] / r
        p = iden - 2 * (w @ w.T)
        a = p @ a @ p
    return a