"""Generator for arc_additional_puzzle_bank_volume17:E119.

The middle cell of each 3-cell diagonal magenta triple is recolored yellow.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_triples,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_triples, length_2_diag, axis_aligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "85de426e8683"
VERSION = "1.1.0"
TASK_ID = "85de426e8683"
SUMMARY = "The middle cell of each 3-cell diagonal magenta triple is recolored yellow."

INVARIANTS = [
    "background is 0",
    "each target is an 8-connected diagonal triple of color 5",
    "triples can slope down-left or down-right",
    "triples are separated so 8-connected objects remain size three",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_triples", "length_2_diag", "axis_aligned")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_triples":      {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "diagonal_triples",
                       "valid": "diagonal_triples"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_triples = ctx.draw_int("n_triples", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_triples = ctx.draw_int("n_triples", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_triples = ctx.draw_int("n_triples", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    occupied: set[tuple[int, int]] = set()
    made = 0
    for _ in range(240):
        if made >= n_triples:
            break
        slope = rng.choice([-1, 1])
        r0 = rng.randint(1, h - 4)
        c0 = rng.randint(3, w - 2) if slope == -1 else rng.randint(1, w - 4)
        cells = [(r0 + i, c0 + slope * i) for i in range(3)]
        if any(abs(r - rr) <= 1 and abs(c - cc) <= 1 for r, c in cells for rr, cc in occupied):
            continue
        for r, c in cells:
            g[r][c] = 5
            occupied.add((r, c))
        made += 1
    if not occupied:
        for i in range(3):
            g[1 + i][1 + i] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_triples":
        # blank → no triples to recolor middle
        return g
    if name == "length_2_diag":
        # 2-cell diagonal → not a triple, no middle to recolor
        g[2][2] = 5; g[3][3] = 5
        return g
    if name == "axis_aligned":
        # 3 cells in straight row/col → not diagonal, rule won't fire
        for c in range(2, 5): g[3][c] = 5
        for r in range(5, 8): g[r][6] = 5
        return g
    return g
