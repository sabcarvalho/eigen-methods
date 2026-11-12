"""Exemplo: Leverrier (polinômio característico) + Newton (raízes)."""
from _util import verify_dominant, verify, np
from matrices import search
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.leverrier_newton import leverrier, newton, geraQ


def executar():
    # ---- caso pequeno: todos os autovalores conhecidos ----
    for nome in ['m3x3_A', 'm3x3_B', 'm4x4_A']:
        ref = search(nome)
        A = ref['A'].copy()
        p = leverrier(A)
        print(f'\n===== {nome} =====')
        print(f'Polinômio: {p}')

        raizes = []
        for _ in range(len(A)):
            raiz, it, erro = newton(p, 0.0, 1e-8)
            raizes.append(raiz)
            p = geraQ(p, raiz)

        verify(nome, raizes, ref['eigenvalues'], tol=1e-4)

    # ---- caso 7x7: só o dominante é conhecido (~3.348) ----
    print('\n===== corr_7x7 (dominante) =====')
    A = search('corr_7x7')['A'].copy()
    p = leverrier(A)
    raiz, it, erro = newton(p, 3.348, 1e-9)
    verify_dominant('corr_7x7', raiz, 3.348, tol=1e-4)
    print(f'  iterações: {it}   erro: {erro:.2e}')


if __name__ == '__main__':
    executar()