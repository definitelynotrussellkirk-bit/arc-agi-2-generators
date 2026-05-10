"""Generator for arc_additional_puzzles_21_set10_bundle:H65 — infer whole-panel transform.

Rule: 2 full-column color-5 dividers split the grid into 3 square panels A, B, C.
A→B is determined by some code (1=id, 2=cw, 3=180, 4=flip-ud, 5=flip-lr).
Apply same code to C as the output. Codes 2 and 3 require square panels.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "63784d19dd2d"
VERSION = "1.1.0"
TASK_ID = "63784d19dd2d"

SUMMARY = "Three N×N panels separated by 5-divider cols; B = transform(A); C is unrelated."

INVARIANTS = [
    "background is 0",
    "two full-column color-5 dividers split grid into three equal-width N×N panels",
    "panels are square (rows == panel width)",
    "B = transform(A) for one of: identity, rotate-cw, rotate-180, flip-ud, flip-lr",
    "C contains a non-empty shape independent of A",
]

AXES = {
    "panel_n": {"type": "int", "default": "rng 4..6", "valid": "3..7"},
    "transform": {"type": "int", "default": "rng 2..5", "valid": "1..5"},
}


def _xform(cells, t, n):
    if t == 1: return list(cells)
    if t == 2: return [(c, n - 1 - r) for r, c in cells]  # cw
    if t == 3: return [(n - 1 - r, n - 1 - c) for r, c in cells]  # 180
    if t == 4: return [(n - 1 - r, c) for r, c in cells]  # flip-ud
    return [(r, n - 1 - c) for r, c in cells]  # flip-lr


def _random_shape(rng, n, k):
    """Pick k distinct cells in an n×n panel, biased to be asymmetric."""
    cells = []
    seen = set()
    # seed with one cell, then add neighbors so the shape is connected & non-trivial
    r0 = rng.randint(0, n - 1); c0 = rng.randint(0, n - 1)
    cells.append((r0, c0)); seen.add((r0, c0))
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    n = ctx.draw_int("panel_n", 4, 6)
    t = ctx.draw_int("transform", 2, 5)
    rng = ctx.draw_rng("layout")
    h = n
    w = n * 3 + 2
    d1, d2 = n, 2 * n + 1
    color_a, color_c = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)

    for outer in range(40):
        g = full_grid(h, w, 0)
        for r in range(h):
            g[r][d1] = 5
            g[r][d2] = 5
        ka = rng.randint(3, max(3, n))
        kc = rng.randint(3, max(3, n))
        cells_a = _random_shape(rng, n, ka)
        cells_b = _xform(cells_a, t, n)
        # ensure B is genuinely different from A so the inferred transform is informative
        if t != 1 and set(cells_a) == set(cells_b):
            continue
        cells_c = _random_shape(rng, n, kc)
        for r, c in cells_a:
            g[r][c] = color_a
        for r, c in cells_b:
            g[r][d1 + 1 + c] = color_a
        for r, c in cells_c:
            g[r][d2 + 1 + c] = color_c
        return g
    raise ValueError("could not realize panel layout in 40 attempts")
