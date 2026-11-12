"""Helpers compartilhados entre os exemplos."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
import numpy as np


def verify(name, obtidos, esperados, tol=1e-3):
    """Compara listas de autovalores ordenados; imprime OK/FALHA."""
    obtidos = sorted(float(np.real(x)) for x in obtidos)
    esperados = sorted(float(x) for x in esperados)
    if len(obtidos) != len(esperados):
        print(f"[FALHA] {name}: esperados {len(esperados)}, obtidos {len(obtidos)}")
        return False
    for o, e in zip(obtidos, esperados):
        if abs(o - e) > tol:
            print(f"[FALHA] {name}: esperado {esperados}, obtido {obtidos}")
            return False
    print(f"[  OK ] {name}: {obtidos}")
    return True


def verify_dominant(name, obtido, esperado, tol=1e-3):
    """Variante p/ autovalor único (dominante)."""
    if isinstance(obtido, np.ndarray): 
        obtido = obtido[0]
    if abs(float(obtido) - float(esperado)) > tol:
        print(f"[FALHA] {name}: esperado {esperado}, obtido {obtido}")
        return False
    print(f"[  OK ] {name}: {obtido}")
    return True