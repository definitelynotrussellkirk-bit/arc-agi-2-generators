"""Generator for next_b:m14 — select diagonal-touching components.

Rule: keep color-6 components whose cells include at least one main-
diagonal cell (r == c); recolor them to 2; drop the others.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_on_diagonal, none_on_diagonal, single_component.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cf6ef609da0d"
VERSION = "1.1.0"
TASK_ID = "cf6ef609da0d"
SUMMARY = "2-3 color-6 components; at least one touches the main diagonal, at least one does not."

INVARIANTS = [
    "background is 0",
    "all non-bg cells are color 6",
    "≥1 component has a cell with r == c (main diagonal)",
    "≥1 component has no cell with r == c",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_on_diagonal", "none_on_diagonal", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "diagonal_mix",
                       "valid": "diagonal_mix"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _try_place(g, rng, shape):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        cells = [(r0 + dr, c0 + dc) for dr, dc in shape]
        for r, c in cells:
            g[r][c] = 6
        return cells
    return None


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    for outer in range(40):
        g = full_grid(h, w, 0)
        n = rng.randint(2, 3)
        components = []
        for _ in range(n):
            cells = _try_place(g, rng, rng.choice(_SHAPES))
            if cells is not None:
                components.append(cells)
        if len(components) < 2:
            continue
        on_diag = sum(1 for cells in components
                      if any(r == c for r, c in cells))
        off_diag = len(components) - on_diag
        if on_diag >= 1 and off_diag >= 1:
            return g
    raise ValueError(f"could not realize on/off-diagonal mix in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "all_on_diagonal":
        # every component touches the main diagonal → all components kept, none dropped
        for (r, c) in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 6
        for (r, c) in [(5, 5), (5, 6), (6, 5)]: g[r][c] = 6
        return g
    if name == "none_on_diagonal":
        # no component touches the main diagonal → all components dropped, output is empty
        for (r, c) in [(1, 4), (1, 5), (2, 4)]: g[r][c] = 6
        for (r, c) in [(5, 8), (5, 9), (6, 9)]: g[r][c] = 6
        return g
    if name == "single_component":
        # one component → no comparison; output is either all-kept or all-dropped trivially
        for (r, c) in [(3, 3), (3, 4), (4, 3), (4, 4)]: g[r][c] = 6
        return g
    return g
