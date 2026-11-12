"""Exemplo: diagonalização simbólica (SymPy)."""
from _util import verify
from matrices import search
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.eigen_definition import main



def exec():
    for name in ['m3x3_A', 'm3x3_B', 'm3x3_IJ', 'm3x3_posto2']:
        ref = search(name)
        A = ref['A']
        print(f'\n===== {name} =====')
        r = main(A, verbose=False)
        obtidos = [float(sp.N(x)) for x in r['eigenvalues']]
        verify(name, obtidos, ref['eigenvalues'])
        print(f'Polinômio: {r["poly"]}')
        print(f'P =\n{r["P"]}')
        print(f'D =\n{r["D"]}')


if __name__ == '__main__':
    import sympy as sp
    exec()