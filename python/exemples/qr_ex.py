# -*- coding: utf-8 -*-
"""Exemplo: método QR."""
from _util import verify, np
from matrices import search
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.qr_method import main_qr


def executar():
    for nome in ['m3x3_A', 'm3x3_B', 'm3x3_D', 'm3x3_diag3_off1']:
        ref = search(nome)
        A = ref['A']
        print(f'\n===== {nome} =====')

        resultados = main_qr(A.copy(), err=1e-9, verbose=False)
        obtidos = [r['eigenvalue'] for r in resultados]
        verify(nome, obtidos, ref['eigenvalues'])

        for r in resultados:
            v = np.round(r['eigenvector'].ravel(), 4)
            print(f'  λ ≈ {r["eigenvalue"]:+.6f}   v ≈ {v}')


if __name__ == '__main__':
    executar()