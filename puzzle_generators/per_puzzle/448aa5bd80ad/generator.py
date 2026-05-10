"""Generator for arc_puzzle_bank_21_set11_bundle:medium_k09 — Count-9s row 0 selects transform.

Rule: count = number of 9s in row 0. Clean row 0 to 0; crop to content;
1=rotate-cw, 2=rotate-180, ≥3=transpose.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_nines,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_nines, no_blob, square_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "448aa5bd80ad"
VERSION = "1.1.0"
TASK_ID = "448aa5bd80ad"
SUMMARY = "Row 0 has 1-3 cells of color 9; small blob in interior; output transforms cropped blob by count."

INVARIANTS = [
    "row 0 has between 1 and 3 cells of color 9",
    "exactly one connected blob below row 0",
    "blob is non-square so transform is non-trivial",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_nines", "no_blob", "square_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_nines":        {"type": "int", "default": "rng 1..3",  "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "row0_count_with_blob",
                       "valid": "row0_count_with_blob"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        n_nines = ctx.draw_int("n_nines", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_nines = ctx.draw_int("n_nines", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
        n_nines = ctx.draw_int("n_nines", 1, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = list(range(w)); rng.shuffle(cols)
    for c in cols[:n_nines]:
        g[0][c] = 9
    blob_color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    bh = rng.randint(2, 3); bw = rng.randint(2, 4)
    if bh == bw: bw += 1
    r1 = rng.randint(2, h - bh - 1)
    c1 = rng.randint(0, w - bw)
    for r in range(r1, r1 + bh):
        g[r][c1] = blob_color
    for c in range(c1, c1 + bw):
        g[r1 + bh - 1][c] = blob_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_nines":
        # row 0 has no 9s → count = 0, transform undefined
        for r in range(3, 5):
            g[r][2] = 4
        for c in range(2, 5):
            g[4][c] = 4
        return g
    if name == "no_blob":
        # 9s present in row 0 but no blob below → rule has nothing to crop+transform
        g[0][2] = 9; g[0][5] = 9
        return g
    if name == "square_blob":
        # square blob → transpose looks identical to identity
        g[0][2] = 9; g[0][5] = 9; g[0][7] = 9  # count=3, transpose
        for r in range(3, 6):
            for c in range(3, 6): g[r][c] = 4  # 3x3 solid square
        return g
    return g
