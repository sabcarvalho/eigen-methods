"""Leverrier's method (characteristic polynomial) + Newton's method (roots)."""
import numpy as np

def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def leverrier(matrix):
    dim = len(matrix)
    sk = np.zeros(dim + 1)
    p = np.zeros(dim + 1)
    sk[1] = trace(matrix)
    p[0] = -1
    p[1] = sk[1]
    ak = matrix
    for k in range(2, dim + 1):
        ak = ak @ matrix
        sk[k] = trace(ak)
        for i in range(1, k):
            p[k] += p[i] * sk[k - i]
        p[k] = (sk[k] - p[k]) / k
    return p


def newton(poly, x, acc):
    n = len(poly) - 1
    plinha = np.zeros(n)
    for i in range(n):
        plinha[i] = poly[i] * (n - i)
    it = 1
    err = 1
    while err > acc and it < 1000:
        px = poly[n]
        pl = 0
        for i in range(n, 0, -1):
            px += x ** i * poly[n - i]
            pl += x ** (i - 1) * plinha[n - i]
        xk = x - px / pl
        err = abs(xk - x)
        x = xk
        it += 1
    return float(xk), it, err


def geraQ(poly, raiz):
    n = len(poly)
    bn = np.zeros(n - 1)
    bn[0] = poly[0]
    for i in range(1, n - 1):
        bn[i] = raiz * bn[i - 1] + poly[i]
    return bn