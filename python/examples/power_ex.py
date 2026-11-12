# -*- coding: utf-8 -*-
"""Exemplo: método das potências (autovalor dominante)."""
from _util import verify_dominant, np
import sys
from pathlib import Path
from matrices import search

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.power_method import power_method



def exec():
    for nome in ['pot_3x3', 'pot_5x5_A', 'pot_5x5_B']:
        ref = search(nome)
        A = ref['A']
        dim = A.shape[0]
        print(f'\n===== {nome} =====')
        print(f'Traço = {np.trace(A):.4f}   '
              f'máx via numpy = {max(np.abs(np.linalg.eigvals(A))):.4f}')

        y = np.ones((dim, 1))
        r = power_method(A, y, 0, [], p=1e-6, k_max=500, dim=dim)

        if 'converged' in r and not r['converged']:
            print(f'[!] não convergiu em {r["iterations"]} iterações')
            print(f'    último autovalor: {r["eigenvalue"]}')
            continue

        verify_dominant(nome, r['eigenvalue'], max(ref['eigenvalues']))
        print(f'  iterações: {r["iterations"]}')
        print(f'  eigenvector: {np.round(r["eigenvector"].ravel(), 4)}')


if __name__ == '__main__':
    exec()