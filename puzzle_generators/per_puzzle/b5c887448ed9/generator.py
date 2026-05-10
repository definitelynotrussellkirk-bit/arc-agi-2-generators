"""Generator for 16b:m111 — connect same-color pairs with elbows.

Rule: each color appearing exactly twice gets connected by an L-elbow
path (one horizontal segment + one vertical segment).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_color, aligned_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b5c887448ed9"
VERSION = "1.1.0"
TASK_ID = "b5c887448ed9"
SUMMARY = "2-3 colors each appearing exactly twice, at non-aligned positions."

INVARIANTS = [
    "background is 0",
    "each non-zero color appears exactly twice",
    "the two cells of each color are at strictly different rows AND cols (so elbow is non-trivial)",
    "elbows of different colors don't conflict at start/end cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_color", "aligned_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "non_aligned_pairs",
                       "valid": "non_aligned_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for color in palette:
        for _ in range(40):
            r1 = rng.randint(0, h - 1)
            c1 = rng.randint(0, w - 1)
            r2 = rng.randint(0, h - 1)
            c2 = rng.randint(0, w - 1)
            if r1 == r2 or c1 == c2: continue
            if g[r1][c1] != 0 or g[r2][c2] != 0: continue
            g[r1][c1] = color
            g[r2][c2] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no pairs to connect
        return g
    if name == "single_color":
        # only one cell of color → can't form pair
        g[2][3] = 4
        return g
    if name == "aligned_pair":
        # pair shares a row → no elbow needed (straight line, not L)
        g[3][2] = 4; g[3][7] = 4
        return g
    return g
