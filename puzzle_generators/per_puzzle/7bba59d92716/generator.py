"""Generator for arc_additional_puzzle_bank_volume23:E155 — Mark middle of vertical 1-line of length 5 with 2.

Rule: each 1-blob that is a vertical line of size 5 → middle cell to 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_lines,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_length5, all_length5, horizontal_lines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7bba59d92716"
VERSION = "1.1.0"
TASK_ID = "7bba59d92716"
SUMMARY = "2 vertical 1-lines of length 5 + a few non-line 1s as decoration."

INVARIANTS = [
    "exactly 2 vertical 1-lines of length 5",
    "1-2 short vertical 1-lines of other lengths (won't qualify)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_length5", "all_length5", "horizontal_lines")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..9", "valid": "8..12"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_lines":        {"type": "int", "default": "2", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "vertical_lines",
                       "valid": "vertical_lines"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols_avail = list(range(w))
    rng.shuffle(cols_avail)
    c1, c2, c3 = cols_avail[0], cols_avail[1], cols_avail[2]
    r1 = rng.randint(0, h - 5)
    r2 = rng.randint(0, h - 5)
    for dr in range(5):
        g[r1 + dr][c1] = 1
        g[r2 + dr][c2] = 1
    rs = rng.randint(0, h - 4)
    for dr in range(rng.randint(2, 3)):
        g[rs + dr][c3] = 1
    g[h - 1][cols_avail[3]] = 6 if w > 3 else 0
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_length5":
        # all vertical 1-lines have other lengths (3, 4) → no qualifying targets, rule no-op
        for dr in range(3):
            g[1 + dr][2] = 1
        for dr in range(4):
            g[1 + dr][6] = 1
        return g
    if name == "all_length5":
        # every column has length-5 → every column gets middle marked, no contrast across blobs
        for c in [1, 4, 7]:
            for dr in range(5):
                g[2 + dr][c] = 1
        return g
    if name == "horizontal_lines":
        # 1-blobs are horizontal not vertical → "vertical line" condition never matches, rule no-op
        for dc in range(5):
            g[2][1 + dc] = 1
        for dc in range(5):
            g[5][3 + dc] = 1
        return g
    return g
