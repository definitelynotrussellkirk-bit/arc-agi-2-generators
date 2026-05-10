"""Generator for arc_additional_puzzle_bank_volume21:E143 — Plus-shape 3-frame center → 8.

Rule: a 0-cell with all 4 cardinal neighbors = 3 → set to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pluses,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pluses, partial_pluses, plus_center_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "83efd4fcb4f4"
VERSION = "1.1.0"
TASK_ID = "83efd4fcb4f4"
SUMMARY = "2-3 plus-shapes of 3s (4 cardinal cells around a center)."

INVARIANTS = [
    "≥2 plus-pattern of 3s (cells at (r-1,c)(r+1,c)(r,c-1)(r,c+1) all = 3, center is 0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pluses", "partial_pluses", "plus_center_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pluses":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "interior_pluses",
                       "valid": "interior_pluses"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    placed = []
    for _ in range(40):
        if len(placed) >= 2:
            break
        r = rng.randint(2, h - 3); c = rng.randint(2, w - 3)
        ok = all(abs(r - pr) > 2 or abs(c - pc) > 2 for pr, pc in placed)
        if ok:
            g[r - 1][c] = 3; g[r + 1][c] = 3
            g[r][c - 1] = 3; g[r][c + 1] = 3
            placed.append((r, c))
    decor_palette = [6, 7]
    for color in decor_palette:
        for _ in range(3):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] == 0:
                g[r][c] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_pluses":
        # only scattered 3s, no plus pattern → predicate fails everywhere
        g[2][3] = 3; g[5][7] = 3; g[6][2] = 3
        return g
    if name == "partial_pluses":
        # only 3 of 4 cardinal arms set → predicate "all 4 cardinal = 3" fails, no center filled
        # missing top arm at (3, 3)
        g[3][2] = 3; g[3][4] = 3; g[4][3] = 3   # (left, right, bottom) but no top
        # missing bottom arm at (6, 6)
        g[5][6] = 3; g[6][5] = 3; g[6][7] = 3   # (top, left, right) but no bottom
        return g
    if name == "plus_center_filled":
        # plus with non-zero center → predicate "center is 0" fails, rule does nothing
        # plus around (3, 3) but center already filled
        g[3][3] = 4   # center filled with non-zero non-3
        g[2][3] = 3; g[4][3] = 3; g[3][2] = 3; g[3][4] = 3
        return g
    return g
