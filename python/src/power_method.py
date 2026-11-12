"""Power method: dominant eigenvalue and associated eigenvector."""
from numpy import sqrt


def power_method(a, y, k, x, p, k_max, dim):
    """Power method (recursive). Returns a dict containing the eigenvalue, eigenvector, and iterations."""
    z = a @ y
    norm = 0
    for i in range(dim):
        norm += z[i] ** 2
    y2 = (1 / sqrt(norm)) * z

    if k < 1:
        return power_method(a, y2, k + 1, x, p, k_max, dim)

    x2 = []
    for j in range(dim):
        x2.append(z[j] / y[j] if y[j] != 0 else 0)

    if len(x) == 0:
        return power_method(a, y2, k + 1, x2, p, k_max, dim)

    avg = sum(x2) / len(x2)
    for i in range(dim):
        erro = abs(x2[i] - x[i]) / abs(x2[i]) if x2[i] != 0 else abs(x2[i] - x[i])
        if erro <= p and x2[i] >= avg:
            return {'eigenvalue': x2[i], 'eigenvector': y2, 'iterations': k}

    if k >= k_max - 1:
        return {'eigenvalue': x2[0], 'eigenvector': y2, 'iterations': k, 'converged': False}

    return power_method(a, y2, k + 1, x2, p, k_max, dim)