"""Inverse power method, with and without a shift."""
import numpy as np


def inv_power_method(a, y, p, q=0.0, modo='vetorial', k_max=1000):
    """Inverse power method (with optional shift). 

    In each iteration, it solves ``(A - qI) z = y`` and estimates ``1/(λ - q)`` using
    the ratios ``z[i]/y[i]``. When ``q = 0``, it reduces to the pure inverse
    power method (finding the eigenvalue with the smallest absolute value). 

    Parameters
    ----------
    a : array-like (n, n)
    Square matrix. 
    y : array-like (n,) or (n, 1)
    Initial approximation of the eigenvector. 
    p : float
    Tolerance for the stopping criterion. 
    q : float, optional
    Shift value. Default is ``0.0`` (pure inverse power method). 
    modo : {'vetorial', 'escalar'}, optional
    * ``'vetorial'``: absolute error per component — returns as soon as
    **any** component ``z[i]/y[i]`` stabilizes (behavior of the legacy
    ``mpotInv``/``mpotDesloc`` functions). 
    * ``'escalar'``: relative error based on the **mean** of the quotients
    ``z[i]/y[i]`` (behavior of the legacy ``mpotInv2``/``mpotDesloc2``
    functions). 
    k_max : int, optional
    Maximum number of iterations. 

    Returns
    -------
    dict
    ``{'eigenvalue', 'eigenvector', 'iterations', 'converged'}``.
    """
    a = np.asarray(a, dtype=float)
    y = np.asarray(y, dtype=float).reshape(-1, 1)
    dim = a.shape[0]

    matA = a - np.identity(dim) * q

    if modo == 'vetorial':
        return _vetorial(matA, y, p, q, k_max, dim)
    elif modo == 'escalar':
        return _escalar(matA, y, p, q, k_max, dim)
    else:
        raise ValueError(f"mode must be 'vector' or 'scalar', not {modo!r}")


def _vetorial(matA, y, p, q, k_max, dim):
    """Original variant of mpotInv/mpotDesloc (error by component)."""
    x = np.zeros((dim, 1))
    x2 = np.zeros((dim, 1))
    y_cur = y.copy()

    for k in range(k_max):
        z = np.linalg.solve(matA, y_cur)
        alpha = np.max(np.abs(z))
        y2 = z / alpha if alpha != 0 else z.copy()

        for i in range(dim):
            x2[i] = z[i, 0] / y_cur[i, 0] if abs(y_cur[i, 0]) > 1e-7 else z[i,0]

        y_cur = y2.copy()

        for i in range(dim):
            err = abs(x2[i] - x[i])
            if err <= p:
                eigenvalue = q + 1.0 / x2[i, 0]
                return {
                    'eigenvalue': eigenvalue,
                    'eigenvector': y2,
                    'iterations': k + 1,
                    'converged': True,
                }

        x = x2.copy()

    return {
        'eigenvalue': q + 1.0 / x2[-1, 0] if abs(x2[-1, 0]) > 1e-12 else np.inf,
        'eigenvector': y_cur,
        'iterations': k_max,
        'converged': False,
    }


def _escalar(matA, y, p, q, k_max, dim):
    """Variante original de mpotInv2/mpotDesloc2 (erro sobre a média)."""
    x = 0.0
    x2 = 0.0
    y_cur = y.copy()

    for k in range(k_max):
        z = np.linalg.solve(matA, y_cur)
        alpha = np.max(np.abs(z))
        y2 = z / alpha if alpha != 0 else z.copy()

        soma = 0.0
        for i in range(dim):
            if abs(y_cur[i, 0]) > 1e-7:
                soma += z[i, 0] / y_cur[i, 0]
            else:
                soma += z[i, 0]
        x2 = soma / dim

        y_cur = y2.copy()

        erro = abs(x2 - x)
        if abs(x2) > 1e-3:          
            erro /= abs(x2)

        if erro <= p:
            return {
                'eigenvalue': q + 1.0 / x2,
                'eigenvector': y2,
                'iterations': k + 1,
                'converged': True,
            }

        x = x2

    return {
        'eigenvalue': q + 1.0 / x2 if abs(x2) > 1e-12 else np.inf,
        'eigenvector': y_cur,
        'iterations': k_max,
        'converged': False,
    }