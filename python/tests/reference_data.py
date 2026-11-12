"""Reference matrices and their eigenvalues (from the original IC code).

Each entry has:
    A            : numpy array
    eigenvalues  : list of floats (order is irrelevant; tests sort)
    source       : 'comment'  → value from the original code comment
                   'computed' → value computed independently
    dominant     : (optional) for power-method tests
    note         : (optional) free-form remark
"""
import numpy as np


REFERENCE_MATRICES = {
    # ------------------ symbolic / QR test set ------------------
    'm3x3_A': {
        'A': np.array([[3, -1, 0], [-1, 2, -1], [0, -1, 3]], dtype=float),
        'eigenvalues': [1.0, 3.0, 4.0],
    },
    'm3x3_B': {
        'A': np.array([[4, -2, -2], [0, 1, 0], [1, 0, 1]], dtype=float),
        'eigenvalues': [1.0, 2.0, 3.0],
    },
    'm3x3_D': {
        'A': np.array([[3, 0, 1], [2, 2, 2], [4, 2, 5]], dtype=float),
        'eigenvalues': [1.0, 2.0, 7.0],
    },
    'm2x2_A': {
        'A': np.array([[0, 1], [-1, 5]], dtype=float),
        'eigenvalues': [0.208712152522080, 4.791287847477919],
    },
    'm3x3_posto2': {
        'A': np.array([[1, 0, 0], [0, 1, 0], [1, 0, 0]], dtype=float),
        'eigenvalues': [0.0, 1.0, 1.0],
    },
    'm3x3_IJ': {
        'A': np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]], dtype=float),
        'eigenvalues': [1.0, 1.0, 4.0],
    },
    'm3x3_diag3_off1': {
        'A': np.array([[3, 1, 1], [1, 3, 1], [1, 1, 3]], dtype=float),
        'eigenvalues': [2.0, 2.0, 5.0],
    },
    'm3x3_triangular': {
        'A': np.array([[1, 1, 1], [0, 2, 1], [0, 0, 3]], dtype=float),
        'eigenvalues': [1.0, 2.0, 3.0],
    },
    'm4x4_A': {
        'A': np.array([[4, -1, -1, 0], [-1, 4, 0, -1],
                       [-1, 0, 4, -1], [0, -1, -1, 4]], dtype=float),
        'eigenvalues': [2.0, 4.0, 4.0, 6.0],
    },

    # ------------------ power method ------------------
    'pot_3x3': {
        'A': np.array([[3, 0, 0], [-4, 6, 2], [16, -15, -5]], dtype=float),
        'eigenvalues': [0.0, 1.0, 3.0],
        'dominant': 3.0,
    },
    'pot_5x5_A': {
        'A': np.array([[1, 2, 5, 3, 2], [1, 3, 7, 3, 4],
                       [0, 5, 2, 2, 1], [1, 3, 0, 1, 2],
                       [0, 6, 7, 4, 7]], dtype=float),
        'eigenvalues': [15.0117],
    },
    'pot_5x5_B': {
        'A': np.array([[25, -10, -4, 10, 16], [-10, 10, 1, 0, 13],
                       [-4, 1, 46, 20, -26], [10, 0, -20, 20, 8],
                       [16, 13, -26, 8, 50]], dtype=float),
        'eigenvalues': [79.009],
    },

    # ------------------ Leverrier + Newton ------------------
    'corr_7x7': {
        'A': np.array([
            [1.0000, 0.7242, 0.7885, 0.6359, -0.3653, 0.3525, 0.0829],
            [0.7242, 1.0000, 0.4741, 0.7334, -0.1404, 0.4788, 0.3336],
            [0.7885, 0.4741, 1.0000, 0.4977, -0.2969, 0.1785, 0.0263],
            [0.6359, 0.7334, 0.4977, 1.0000, -0.2143, 0.5533, 0.2583],
            [-0.3653, -0.1404, -0.2969, -0.2143, 1.0000, 0.4870, 0.6946],
            [0.3525, 0.4788, 0.1785, 0.5533, 0.4870, 1.0000, 0.5497],
            [0.0829, 0.3336, 0.0263, 0.2583, 0.6946, 0.5497, 1.0000],
        ], dtype=float),
        'eigenvalues': [3.348],
    },
}


def get(name):
    """Return the reference entry for ``name`` or raise ``KeyError``."""
    if name not in REFERENCE_MATRICES:
        raise KeyError(f'Unknown reference matrix: {name!r}')
    return REFERENCE_MATRICES[name]