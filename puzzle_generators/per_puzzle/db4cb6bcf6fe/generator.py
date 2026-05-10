"""Generator for arc_puzzle_bank_21_set18_s:S18_H7 — same-pose grouping matrix.

Rule: 4 single-cell-pair motifs in distinct colors. Output is N×N where
diagonal = 5, off-diagonal = 8 if they have the same relative pose.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_pair, all_same_pose.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "db4cb6bcf6fe"
VERSION = "1.1.0"
TASK_ID = "db4cb6bcf6fe"

SUMMARY = "4 pairs of same-color cells in 4 distinct colors at distinct positions."

INVARIANTS = [
    "background is 0",
    "exactly 4 pairs of single-cell markers, each pair in a distinct color",
    "the 2 cells in each pair are separated by some offset",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_pair", "all_same_pose")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "4", "valid": "4..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "scattered_color_pairs",
                       "valid": "scattered_color_pairs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 4)
    for color in colors:
        for _t in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            dr = rng.choice([-2, -1, 1, 2])
            dc = rng.choice([-2, -1, 1, 2, 3])
            r2, c2 = r + dr, c + dc
            if not (0 <= r2 < h and 0 <= c2 < w): continue
            if g[r2][c2] != 0: continue
            g[r][c] = color; g[r2][c2] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # singletons only — no pose to compare
        g[1][1] = 4
        g[3][5] = 6
        g[5][8] = 7
        return g
    if name == "single_pair":
        # only one color-pair → 1×1 matrix with just diagonal, no off-diag info
        g[2][2] = 4; g[3][4] = 4
        return g
    if name == "all_same_pose":
        # all 4 pairs share identical relative offset → matrix is all 8s off-diag
        # i.e. no contrast / "no" cells
        g[1][1] = 4; g[2][2] = 4   # offset (1,1)
        g[1][5] = 6; g[2][6] = 6   # offset (1,1)
        g[4][1] = 7; g[5][2] = 7   # offset (1,1)
        g[4][5] = 8; g[5][6] = 8   # offset (1,1)
        return g
    return g
