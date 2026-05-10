"""Generator for arc_puzzle_bank_seventeenth_21_bundle:easy_119_keep_centers_of_odd_squares.

Rule: each filled odd-size square is reduced to its center cell only.

Combinatorial axes (8): grid_h, grid_w, palette_kind, squares,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_squares, even_size_squares, hollow_squares.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "70abd9105769"
VERSION = "1.1.0"
TASK_ID = "70abd9105769"

SUMMARY = "Separated filled odd-size squares reduce to their center cells."

INVARIANTS = [
    "background is 0",
    "each object is a filled odd-sized square",
    "square centers are unique and in bounds",
    "squares are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_squares", "even_size_squares", "hollow_squares")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "squares":        {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_odd_squares",
                       "valid": "spaced_odd_squares"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("squares", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        target = ctx.draw_int("squares", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
        target = ctx.draw_int("squares", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        size = rng.choice([3, 5])
        r0 = rng.randint(0, h - size)
        c0 = rng.randint(0, w - size)
        guard = {
            (r, c)
            for r in range(max(0, r0 - 1), min(h, r0 + size + 1))
            for c in range(max(0, c0 - 1), min(w, c0 + size + 1))
        }
        if guard & reserved:
            continue
        color = colors[placed % len(colors)]
        for r in range(r0, r0 + size):
            for c in range(c0, c0 + size):
                g[r][c] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_squares":
        # blank → no squares to reduce, rule has no effect
        return g
    if name == "even_size_squares":
        # 2x2 and 4x4 squares → no unique center cell, rule undefined
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 4
        for r in range(4):
            for c in range(4): g[3 + r][6 + c] = 6
        return g
    if name == "hollow_squares":
        # ring of color 4 (5x5 outline only) → not a "filled" square, predicate fails
        for r in range(5):
            for c in range(5):
                if r in (0, 4) or c in (0, 4): g[2 + r][2 + c] = 4
        return g
    return g
