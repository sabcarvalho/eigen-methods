# -*- coding: utf-8 -*-
"""Exemplo: potência inversa (com e sem deslocamento)."""
from _util import verify_dominant, np
from matrices import search
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.inv_power_method import inv_power_method



def exec():
    # -------- inversa pura (q = 0) — autovalor de menor módulo --------
    casos = [
        ('m2x2_A', 0.208712, 0.0),
        ('m3x3_A', 1.0, 0.0),
        ('m4x4_A', 2.0, 0.0),
    ]
    for nome, esperado, q in casos:
        A = search(nome)['A']
        y = np.ones((A.shape[0], 1))
        print(f'\n===== {nome}  (q={q}) =====')
        r = inv_power_method(A, y, p=1e-8, q=q, modo='escalar')
        verify_dominant(nome, r['eigenvalue'], esperado, tol=1e-4)
        print(f'  iterações: {r["iterations"]}')
        print(f'  autovetor: {np.round(r["eigenvalue"].ravel(), 4)}')

    # -------- deslocamento: converge para o autovalor mais próximo de q --------
    print('\n===== m3x3_A  (q=2.498 → espera-se 3) =====')
    A = search('m3x3_A')['A']
    y = np.ones((A.shape[0], 1))
    r = inv_power_method(A, y, p=1e-8, q=2.498, modo='escalar')
    verify_dominant('m3x3_A deslocado', r['eigenvalue'], 3.0, tol=1e-4)
    print(f'  iterações: {r["iterations"]}')

    # -------- deslocamento para o menor (q=-1 → próximo de 1) --------
    print('\n===== m3x3_A  (q=-1 → espera-se 1) =====')
    r = inv_power_method(A, y, p=1e-8, q=-1.0, modo='vetorial')
    verify_dominant('m3x3_A deslocado q=-1', r['eigenvalue'], 1.0, tol=1e-4)


if __name__ == '__main__':
    exec()