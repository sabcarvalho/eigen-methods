# -*- coding: utf-8 -*-
"""Reference tests: validate implementations against known eigenvalues.

Assumes the refactored API from ``src/autovalores``:

* ``principal(a, verbose=False)`` → dict with key ``'autovalores'``.
* ``principal_qr(a, err, verbose=False)`` → list of dicts.
* ``mpot(...)`` → dict with ``'eigenvalue'``, ``'autovetor'``, ``'iteracoes'``.
* ``potencia_inversa(...)`` → dict with ``'eigenvalue'``, ``'autovetor'``.

Run with::

    pytest
    pytest tests/test_reference.py -k qr
    pytest tests/test_reference.py -v
"""
import numpy as np
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.leverrier_newton import leverrier, newton, geraQ
from src.qr_method import main_qr
from reference_data import get
from src.power_method import power_method
from src.eigen_definition import main
from src.inv_power_method import inv_power_method
# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _sorted_real(values, ndigits=3):
    return sorted(round(float(np.real(v)), ndigits) for v in values)


def _assert_eigenvalues_close(obtained, expected):
    a = _sorted_real(obtained)
    b = _sorted_real(expected)
    assert a == b, f'expected {b}, got {a}'


# ---------------------------------------------------------------------------
# symbolic (principal) — SymPy, exact arithmetic
# ---------------------------------------------------------------------------
@pytest.mark.parametrize('name', ['m3x3_A', 'm3x3_B', 'm3x3_IJ', 'm3x3_posto2'])
def test_symbolic_eigenvalues(name):
    ref = get(name)
    result = main(ref['A'], verbose=False)
    _assert_eigenvalues_close(result['eigenvalues'], ref['eigenvalues'])


def test_symbolic_diagonalization_is_valid():
    """P⁻¹ A P must be diagonal, with eigenvalues on the diagonal."""
    ref = get('m3x3_A')
    result = main(ref['A'], verbose=False)
    D = result['D']
    for i in range(D.shape[0]):
        for j in range(D.shape[1]):
            if i != j:
                assert D[i, j] < 1e-6
    diagonal = [D[i, i] for i in range(D.shape[0])]
    _assert_eigenvalues_close(diagonal, ref['eigenvalues'])


# ---------------------------------------------------------------------------
# QR — should recover all eigenvalues of the original matrix
# ---------------------------------------------------------------------------
@pytest.mark.parametrize('name', [
    'm3x3_A', 'm3x3_B', 'm3x3_D',
    'm3x3_diag3_off1', 'm3x3_triangular',
])
def test_qr_eigenvalues(name):
    ref = get(name)
    results = main_qr(ref['A'].copy(), err=1e-9, verbose=False)
    _assert_eigenvalues_close([r['eigenvalue'] for r in results],
                              ref['eigenvalues'])


# ---------------------------------------------------------------------------
# power method — dominant eigenvalue only
# ---------------------------------------------------------------------------
@pytest.mark.parametrize('name,expected', [
    ('m3x3_A', 4.0),       # dominant of [1, 3, 4]
    ('pot_3x3', 3.0),      # dominant of [0, 1, 3]
    ('pot_5x5_A', 15.0117),   # from original comment (#15)
])
def test_power_method_dominant(name, expected):
    A = get(name)['A']
    dim = A.shape[0]
    y = np.ones((dim, 1))
    result = power_method(A, y, 0, [], p=1e-6, k_max=2000, dim=dim)
    assert result.get('converged', True), result
    assert abs(result['eigenvalue'] - expected) < 1e-3


# ---------------------------------------------------------------------------
# inverse power method — smallest eigenvalue (q = 0)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize('name,expected', [
    ('m2x2_A', 0.208712),  # smallest of [0.208712, 4.791288]
    ('m3x3_A', 1.0),       # smallest of [1, 3, 4]
    ('m4x4_A', 2.0),       # smallest of [2, 4, 4, 6]
])
def test_inverse_power_smallest(name, expected):
    A = get(name)['A']
    dim = A.shape[0]
    y = np.ones((dim, 1))
    result = inv_power_method(A, y, p=1e-8, modo='escalar')
    assert result['converged'], result
    assert abs(result['eigenvalue'] - expected) < 1e-4


# ---------------------------------------------------------------------------
# inverse power with shift — eigenvalue closest to q
# ---------------------------------------------------------------------------
@pytest.mark.parametrize('name,q,expected', [
    ('m3x3_A', 2.498, 3.0),   # original mpotDesloc call in picme.py
    ('m3x3_A', -1.0, 1.0),
])
def test_inverse_power_shift(name, q, expected):
    A = get(name)['A']
    y = np.ones((A.shape[0], 1))
    result = inv_power_method(A, y, p=1e-8, q=q, modo='escalar')
    assert result['converged'], result
    assert abs(result['eigenvalue'] - expected) < 1e-3


# ---------------------------------------------------------------------------
# Leverrier — polynomial coefficients must match -np.poly(A)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize('name', ['m3x3_A', 'm3x3_B', 'm3x3_D', 'm4x4_A'])
def test_leverrier_polynomial(name):
    """``leverrier(A)`` returns ``-np.poly(A)`` (negated char. polynomial)."""
    A = get(name)['A']
    p = leverrier(A)
    expected = -np.poly(A)
    assert np.allclose(p, expected, atol=1e-6), (
        f'polynomial mismatch for {name}: got {p}, expected {expected}'
    )


# ---------------------------------------------------------------------------
# Newton + deflation — recover all eigenvalues (distinct roots)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize('name', ['m3x3_A', 'm3x3_B', 'm3x3_D'])
def test_leverrier_newton_roots(name):
    A = get(name)['A'].copy()
    p = leverrier(A)
    roots = []
    for _ in range(len(A)):
        root, _, _ = newton(p, 1.0, 1e-8)
        roots.append(root)
        p = geraQ(p, root)
    _assert_eigenvalues_close(roots, get(name)['eigenvalues'])


def test_leverrier_newton_dominant_7x7():
    """The reference case from the original IC code (p, 3.348, ...)."""
    A = get('corr_7x7')['A'].copy()
    p = leverrier(A)
    root, _, _ = newton(p, 3.348, 1e-9)
    assert abs(root - 3.348) < 1e-4