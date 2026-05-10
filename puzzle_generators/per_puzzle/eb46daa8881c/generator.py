"""Generator for arc_puzzle_bank_fourth21:E22.

Rule: each 5-cell plus motif has its center highlighted.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pluses,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pluses, partial_pluses, dense_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "eb46daa8881c"
VERSION = "1.1.0"
TASK_ID = "eb46daa8881c"
SUMMARY = "Place separated same-color plus motifs whose centers are highlighted."

INVARIANTS = [
    "background is 0",
    "each active motif is a five-cell plus",
    "the plus center and four cardinal arms share one non-8 color",
    "motif footprints are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pluses", "partial_pluses", "dense_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pluses":         {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "interior_pluses",
                       "valid": "interior_pluses"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_CARDINAL = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = 1
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("pluses", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("pluses", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        cells = {(r, c)} | {(r + dr, c + dc) for dr, dc in _CARDINAL}
        guard = {
            (rr, cc)
            for cr, cc0 in cells
            for rr in range(max(0, cr - 1), min(h, cr + 2))
            for cc in range(max(0, cc0 - 1), min(w, cc0 + 2))
        }
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
        for rr, cc in cells:
            g[rr][cc] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_pluses":
        # blank grid → no plus motifs to highlight, rule is identity
        return g
    if name == "partial_pluses":
        # T-shape (4 cells, missing one arm) → not a 5-cell plus, rule fails to detect
        # T-up missing bottom arm
        for (r, c) in [(2, 3), (3, 2), (3, 3), (3, 4)]: g[r][c] = 4
        # L-shape (3 cells)
        for (r, c) in [(6, 6), (7, 6), (7, 7)]: g[r][c] = 6
        return g
    if name == "dense_overlap":
        # two pluses overlapping each other → ambiguous which center belongs to which
        # plus 1 centered at (3,3)
        for (r, c) in [(3, 3), (2, 3), (4, 3), (3, 2), (3, 4)]: g[r][c] = 4
        # plus 2 centered at (3,5) — shares col 4 cell
        for (r, c) in [(3, 5), (2, 5), (4, 5), (3, 6)]: g[r][c] = 6
        return g
    return g
