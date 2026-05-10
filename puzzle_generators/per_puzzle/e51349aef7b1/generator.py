"""Generator for arc_additional_puzzles_21_set15_bundle:H105 — color+transform analogy.

Rule: full-col color-5 dividers split into 3 NxN panels. Each panel has a
uniform-color shape (single non-bg color). Transform t in {1..6} maps
binary(A) → binary(B); recolor maps A's single color to B's. Output is
t(C) recolored to B's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers (no color-5 columns → rule cannot split
panels); identity_transform (A == B → t = identity, output = C
recolored); no_C_content (panel C empty → rule's input to t is
empty, output empty).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e51349aef7b1"
VERSION = "1.1.0"
TASK_ID = "e51349aef7b1"

SUMMARY = "3 NxN panels split by sep=5; A→B is a transform + uniform recolor; applied to C."

INVARIANTS = [
    "background is 0",
    "two full-height color-5 divider columns split the grid into three equal NxN panels",
    "panels are square so all 6 transforms apply",
    "each panel uses a single non-bg color; A and B related by some transform t",
    "C uses its own color independent of A and B",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "identity_transform", "no_C_content")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_n":           {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "transform":         {"type": "int", "default": "rng 2..6", "valid": "1..6"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "three_panels_with_5_dividers",
                          "valid": "three_panels_with_5_dividers"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _xform(cells, t, n):
    if t == 1: return list(cells)
    if t == 2: return [(c, n - 1 - r) for r, c in cells]
    if t == 3: return [(n - 1 - r, n - 1 - c) for r, c in cells]
    if t == 4: return [(c, r) for r, c in cells]
    if t == 5: return [(r, n - 1 - c) for r, c in cells]
    return [(n - 1 - r, c) for r, c in cells]


def _rand_cells(rng, n, k):
    cells = [(rng.randint(0, n - 1), rng.randint(0, n - 1))]
    seen = set(cells)
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
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n = ctx.draw_int("panel_n", 4, 4)
    elif difficulty == "hard":
        n = ctx.draw_int("panel_n", 5, 5)
    else:
        n = ctx.draw_int("panel_n", 4, 5)
    t = ctx.draw_int("transform", 2, 6)
    rng = ctx.draw_rng("layout")
    h = n
    w = n * 3 + 2
    d1, d2 = n, 2 * n + 1
    color_a, color_b, color_c = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)

    for outer in range(40):
        g = full_grid(h, w, 0)
        for r in range(h):
            g[r][d1] = 5
            g[r][d2] = 5
        ka = rng.randint(3, max(3, n))
        cells_a = _rand_cells(rng, n, ka)
        cells_b = _xform(cells_a, t, n)
        if set(cells_a) == set(cells_b):
            continue
        kc = rng.randint(3, max(3, n))
        cells_c = _rand_cells(rng, n, kc)
        for r, c in cells_a:
            g[r][c] = color_a
        for r, c in cells_b:
            g[r][d1 + 1 + c] = color_b
        for r, c in cells_c:
            g[r][d2 + 1 + c] = color_c
        return g
    raise ValueError("could not realize 3-panel color-transform analogy in 40 attempts")


def _draw_from_degenerate(name, rng):
    n = 4
    h = n
    w = n * 3 + 2
    g = full_grid(h, w, 0)
    if name == "no_dividers":
        # No color-5 dividers — rule cannot split panels.
        for r in range(n):
            for c in range(n):
                if (r + c) % 2 == 0:
                    g[r][c] = 4
        return g
    if name == "identity_transform":
        # A == B same shape — t = identity.
        for r in range(h):
            g[r][n] = 5
            g[r][2 * n + 1] = 5
        for r, c in [(0, 0), (0, 1), (1, 0)]:
            g[r][c] = 4
        for r, c in [(0, 0), (0, 1), (1, 0)]:
            g[r][n + 1 + c] = 6
        for r, c in [(0, 0), (1, 0), (1, 1)]:
            g[r][2 * n + 2 + c] = 7
        return g
    if name == "no_C_content":
        # Panel C empty — rule's input to t is empty.
        for r in range(h):
            g[r][n] = 5
            g[r][2 * n + 1] = 5
        for r, c in [(0, 0), (0, 1), (1, 0)]:
            g[r][c] = 4
        for r, c in [(0, 1), (1, 0), (1, 1)]:
            g[r][n + 1 + c] = 6
        return g
    return g
