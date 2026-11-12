"""Matrizes e autovalores de referência — extraídos do código original da IC."""
import numpy as np

REFERENCIAS = [
    # ---- símbolo / principal ----
    {'name': 'm3x3_A',
     'A': np.array([[3, -1, 0], [-1, 2, -1], [0, -1, 3]], dtype=float),
     'eigenvalues': [1.0, 3.0, 4.0]},

    {'name': 'm3x3_B',
     'A': np.array([[4, -2, -2], [0, 1, 0], [1, 0, 1]], dtype=float),
     'eigenvalues': [1.0, 2.0, 3.0]},

    {'name': 'm3x3_C',
     'A': np.array([[2, 0, 1], [0, 1, 0], [1, 0, 1]], dtype=float),
     'eigenvalues': [0.381966, 1.0, 2.618034]},

    {'name': 'm3x3_D',
     'A': np.array([[3, 0, 1], [2, 2, 2], [4, 2, 5]], dtype=float),
     'eigenvalues': [1.0, 2.0, 7.0]},

    {'name': 'm2x2_A',
     'A': np.array([[0, 1], [-1, 5]], dtype=float),
     'eigenvalues': [0.208712, 4.791288]},

    {'name': 'm3x3_triangular', 
     'A': np.array([[1, 1, 1], [0, 2, 1], [0, 0, 3]], dtype=float),
     'eigenvalues': [1.0, 2.0, 3.0]},

    {'name': 'm3x3_diag3_off1', 
     'A': np.array([[3, 1, 1], 
                    [1, 3, 1], 
                    [1, 1, 3]], dtype=float),
     'eigenvalues': [2.0, 2.0, 5.0]},

    {'name': 'm3x3_IJ',
     'A': np.array([[2, 1, 1], 
                    [1, 2, 1], 
                    [1, 1, 2]], dtype=float),
     'eigenvalues': [1.0, 1.0, 4.0]},

    {'name': 'm3x3_posto2',
     'A': np.array([[1, 0, 0], [0, 1, 0], [1, 0, 0]], dtype=float),
     'eigenvalues': [0.0, 1.0, 1.0]},

    {'name': 'm3x3_bloco', 
     'A': np.array([[3, 0, 0], [-4, 6, 2], [16, -15, -5]], dtype=float),
     'eigenvalues': [0.0, 1.0, 3.0]},

    {'name': 'm3x3_233', 
     'A': np.array([[4, 2, -4], [1, 4, -3], [1, 1, 0]], dtype=float),
     'eigenvalues': [2.0, 3.0, 3.0]},

    {'name': 'm4x4_A',
     'A': np.array([[4, -1, -1, 0], [-1, 4, 0, -1],
                    [-1, 0, 4, -1], [0, -1, -1, 4]], dtype=float),
     'eigenvalues': [2.0, 4.0, 4.0, 6.0]},

    # ---- potências (autovalor dominante) ----
    {'name': 'pot_3x3', 
     'A': np.array([[3, 0, 0], [-4, 6, 2], [16, -15, -5]], dtype=float),
     'eigenvalues': [3.0], 'dominante': True},

    {'name': 'pot_5x5_A',
     'A': np.array([[1, 2, 5, 3, 2], [1, 3, 7, 3, 4],
                    [0, 5, 2, 2, 1], [1, 3, 0, 1, 2],
                    [0, 6, 7, 4, 7]], dtype=float),
     'eigenvalues': [15.0117], 'dominante': True},

    {'name': 'pot_5x5_B',
     'A': np.array([[25, -10, -4, 10, 16], 
                    [-10, 10, 1, 0, 13],
                    [-4, 1, 46, 20, -26], 
                    [10, 0, 20, 20, 8],
                    [16, 13, -26, 8, 50]], dtype=float),
     'eigenvalues': [79.009], 'dominante': True},

    # ---- Leverrier / Newton ----
    {'name': 'corr_7x7', 'origem': 'parcial',
     'A': np.array([
         [1.0000, 0.7242, 0.7885, 0.6359, -0.3653, 0.3525, 0.0829],
         [0.7242, 1.0000, 0.4741, 0.7334, -0.1404, 0.4788, 0.3336],
         [0.7885, 0.4741, 1.0000, 0.4977, -0.2969, 0.1785, 0.0263],
         [0.6359, 0.7334, 0.4977, 1.0000, -0.2143, 0.5533, 0.2583],
         [-0.3653, -0.1404, -0.2969, -0.2143, 1.0000, 0.4870, 0.6946],
         [0.3525, 0.4788, 0.1785, 0.5533, 0.4870, 1.0000, 0.5497],
         [0.0829, 0.3336, 0.0263, 0.2583, 0.6946, 0.5497, 1.0000],
     ], dtype=float),
     'eigenvalues': [3.348], 'dominante': True},
]


def search(name):
    for ref in REFERENCIAS:
        if ref['name'] == name:
            return ref
    raise KeyError(name)