"""Generator for arc_puzzle_bank_twentythird21:E160 — header-recolor by col 0.

Rule: column 0 holds a 'header' color per row. Any non-zero cell in row r
(other than (r, 0)) gets recolored to that header (if header != 0).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_headers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_headers, no_payload, payload_in_col0.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "019445e9b5a1"
VERSION = "1.1.0"
TASK_ID = "019445e9b5a1"
SUMMARY = "Column 0 has 1-3 header colors; rest of grid has scattered non-zero cells in other colors."

INVARIANTS = [
    "background is 0",
    "1-3 cells in column 0 are non-zero (the header colors)",
    "rows >=1 cells (in cols >=1) have scattered non-zero cells in any colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_headers", "no_payload", "payload_in_col0")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_headers":      {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "col0_header",
                       "valid": "col0_header"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("n_headers", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_headers", 3, min(3, h))
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 6, 8)
        n = ctx.draw_int("n_headers", 2, min(3, h))
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), n)
    header_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for r, color in zip(rows, header_colors):
        g[r][0] = color
    for _ in range(rng.randint(3, 6)):
        for _t in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(2, w - 1)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 7
    g = full_grid(h, w, 0)
    if name == "no_headers":
        # column 0 all zeros → no recoloring target, payload cells stay as-is
        for r, c, v in [(0, 2, 4), (1, 4, 5), (2, 3, 6), (3, 5, 7)]:
            g[r][c] = v
        return g
    if name == "no_payload":
        # only headers in col 0, no payload elsewhere → rule has no targets, output equals input
        g[0][0] = 3
        g[2][0] = 5
        g[4][0] = 7
        return g
    if name == "payload_in_col0":
        # additional non-zero cells in col 0 confuse "header" identification
        for r in range(h):
            g[r][0] = 1 + (r % 3)
        for r, c in [(1, 3), (2, 5), (3, 4)]:
            g[r][c] = 8
        return g
    return g
