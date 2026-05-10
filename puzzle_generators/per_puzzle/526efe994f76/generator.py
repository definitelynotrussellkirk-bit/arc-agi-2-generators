"""Generator for arc_puzzle_bank_21_set7:easy_g04.

Rule: a gray (5) anchor selects checkerboard parity; nonzeros on the
other parity are erased.

Combinatorial axes (8): grid_h/w, palette_kind, n_cells, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, all_same_parity, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "526efe994f76"
VERSION = "1.1.0"
TASK_ID = "526efe994f76"
SUMMARY = "A gray anchor selects checkerboard parity; nonzeros on the other parity are erased."

INVARIANTS = [
    "exactly one gray anchor",
    "colored cells appear on both parities",
    "background is zero",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_anchor", "all_same_parity", "no_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 6..12", "valid": "2..20"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "1..9"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
    n = ctx.draw_int("n_cells", 6, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    anchor = (rng.randint(0, h - 1), rng.randint(0, w - 1))
    g[anchor[0]][anchor[1]] = 5
    positions = [(r, c) for r in range(h) for c in range(w) if (r, c) != anchor]
    rng.shuffle(positions)
    for r, c in positions[:n]:
        g[r][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # cells but no gray anchor — parity selector undefined
        for r, c, v in [(1, 1, 4), (2, 4, 6), (5, 3, 7)]:
            g[r][c] = v
        return g
    if name == "all_same_parity":
        # all colored cells on anchor parity → rule keeps everything (trivial)
        g[2][2] = 5  # anchor (parity = even)
        # all other cells on even parity (r+c even)
        g[0][0] = 4; g[1][1] = 6; g[3][3] = 7; g[4][0] = 8; g[5][1] = 9
        return g
    if name == "no_cells":
        # only anchor — no other cells to filter
        g[3][3] = 5
        return g
    return g
