# tests/test_csp.py
from app.services.csp_solver import CSPSolver, WordleConstraints


def test_green_constraint():
    solver = CSPSolver()
    solver.set_valid_words(["apple", "angle", "amble"])

    constraints = WordleConstraints()
    constraints.update({
        "green": {0: "a"},
        "yellow": {},
        "grey": []
    })

    results = solver.filter_candidates(constraints)
    assert "apple" in results
    assert "angle" in results
    assert "amble" in results


def test_yellow_constraint():
    solver = CSPSolver()
    solver.set_valid_words(["apple", "angle", "amble"])

    constraints = WordleConstraints()
    constraints.update({
        "green": {},
        "yellow": {1: {"p"}},
        "grey": []
    })

    results = solver.filter_candidates(constraints)
    assert "apple" not in results
    assert "angle" not in results
    assert "amble" not in results


def test_grey_constraint():
    solver = CSPSolver()
    solver.set_valid_words(["apple", "angle", "amble"])

    constraints = WordleConstraints()
    constraints.update({
        "green": {},
        "yellow": {},
        "grey": ["p"]
    })

    results = solver.filter_candidates(constraints)
    assert "apple" not in results
    assert "angle" in results
    assert "amble" in results


def test_min_letter_count():
    solver = CSPSolver()
    solver.set_valid_words(["apple", "ample", "maple"])

    constraints = WordleConstraints()
    constraints.update({
        "green": {},
        "yellow": {1: {"p"}},
        "grey": []
    })

    results = solver.filter_candidates(constraints)
    assert "apple" in results
    assert "ample" in results
    assert "maple" not in results
