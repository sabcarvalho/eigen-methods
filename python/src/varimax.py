"""Rotação Varimax (Kaiser) para análise fatorial."""
import numpy as np
from scipy.linalg import svd


def varimax(phi, gamma=1.0, q=20, tol=1e-6):
    """Rotação Varimax via SVD (implementação padrão)."""
    k, p = phi.shape
    R = np.eye(p)
    d = 0
    for _ in range(q):
        d_old = d
        lamb = np.dot(phi, R)
        u, s, vh = svd(
            np.dot(phi.T, np.asarray(lamb) ** 3
                   - (gamma / p) * np.dot(lamb, np.diag(np.diag(np.dot(lamb.T, lamb)))))
        )
        R = np.dot(u, vh)
        d = np.sum(s)
        if d_old != 0 and d / d_old < 1 + tol:
            break
    return np.dot(phi, R), R