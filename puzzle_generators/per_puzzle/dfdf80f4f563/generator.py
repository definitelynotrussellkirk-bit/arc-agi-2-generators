"""Generator for arc_puzzle_bank_fifth21:E30.

Rule: each isolated T-shape's degree-3 center cell is highlighted.

Combinatorial axes (8): grid_h, grid_w, palette_kind, t_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_t_shapes, plus_instead_of_t, t_shapes_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dfdf80f4f563"
VERSION = "1.1.0"
TASK_ID = "dfdf80f4f563"

SUMMARY = "Place isolated T-shapes whose degree-3 centers are highlighted."

INVARIANTS = [
    "background is 0",
    "active objects are isolated same-color T-shapes",
    "each T center has exactly three cardinal same-color neighbors",
    "T footprints do not touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_t_shapes", "plus_instead_of_t", "t_shapes_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "t_shapes":       {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_t_shapes",
                       "valid": "spaced_t_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("t_shapes", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("t_shapes", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("t_shapes", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        missing = rng.choice(_DIRS)
        arms = [d for d in _DIRS if d != missing]
        cells = {(r, c)} | {(r + dr, c + dc) for dr, dc in arms}
        guard = {(rr, cc) for rr in range(r - 2, r + 3) for cc in range(c - 2, c + 3)
                 if 0 <= rr < h and 0 <= cc < w}
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
        for rr, cc in cells:
            g[rr][cc] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_t_shapes":
        # blank → no T-shapes, rule has no center to highlight
        return g
    if name == "plus_instead_of_t":
        # full plus shape (degree-4 center) → predicate "exactly 3 neighbors" fails
        for (r, c) in [(2, 3), (1, 3), (3, 3), (2, 2), (2, 4)]: g[r][c] = 4
        for (r, c) in [(5, 6), (4, 6), (6, 6), (5, 5), (5, 7)]: g[r][c] = 6
        return g
    if name == "t_shapes_touching":
        # adjacent T-shapes → centers have >3 same-color neighbors via merge, predicate fails
        for (r, c) in [(2, 3), (1, 3), (3, 3), (2, 2)]: g[r][c] = 4  # T missing right arm
        for (r, c) in [(2, 4), (1, 4), (3, 4)]: g[r][c] = 4  # second T touching, same color
        return g
    return g
