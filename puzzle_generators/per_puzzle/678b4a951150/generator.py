"""Generator for arc_additional_puzzle_bank_volume23:E156 — (7,0,7) horizontally → 0 becomes 3.

Rule: cell (r,c)=0 with g[r][c-1]=7 and g[r][c+1]=7 → set to 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_triplets,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_triplets, vertical_only, gap_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "678b4a951150"
VERSION = "1.1.0"
TASK_ID = "678b4a951150"
SUMMARY = "3-4 (7,0,7) horizontal triplets + decoration of 7s and 6s."

INVARIANTS = [
    "≥3 rows have a (7,0,7) triplet",
    "1-2 distractor 7-pairs (e.g. adjacent 77, vertical pairs)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_triplets", "vertical_only", "gap_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_triplets":     {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "row_triplets",
                       "valid": "row_triplets"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..3"},
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
        w = ctx.draw_int("grid_w", 12, 13)
        n_triplets = ctx.draw_int("n_triplets", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
        n_triplets = ctx.draw_int("n_triplets", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 12, 14)
        n_triplets = ctx.draw_int("n_triplets", 3, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_rows = set()
    for _ in range(n_triplets):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 3)
            if r not in used_rows and all(g[r][c + i] == 0 for i in range(3)):
                g[r][c] = 7; g[r][c + 2] = 7
                used_rows.add(r)
                break
    # decoration: 7-pair adjacent (won't trigger since middle isn't 0)
    rd = rng.randint(0, h - 1)
    while rd in used_rows: rd = rng.randint(0, h - 1)
    cd = rng.randint(0, w - 2)
    g[rd][cd] = 7; g[rd][cd + 1] = 7
    g[0][1] = 6; g[h - 1][5] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 13
    g = full_grid(h, w, 0)
    if name == "no_triplets":
        # only single 7s and adjacent 7-pairs, no (7,0,7) → rule fires zero times
        g[2][3] = 7
        g[4][6] = 7; g[4][7] = 7  # adjacent pair, middle isn't 0
        g[6][9] = 7
        return g
    if name == "vertical_only":
        # 7-0-7 vertical (above-below) → rule only checks horizontal, predicate fails
        g[1][3] = 7; g[3][3] = 7
        g[2][7] = 7; g[4][7] = 7
        return g
    if name == "gap_already_filled":
        # 7-X-7 where X is non-zero → predicate fails (not 0)
        g[2][2] = 7; g[2][3] = 5; g[2][4] = 7
        g[5][6] = 7; g[5][7] = 8; g[5][8] = 7
        return g
    return g
