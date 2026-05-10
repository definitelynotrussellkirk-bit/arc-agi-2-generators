"""Generator for arc_additional_puzzle_bank_volume9:E63.

Rule: blank centers with red(2) cells in all four cardinal directions become yellow.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_diamonds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_diamonds, partial_diamonds, wrong_arm_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1e99030a2d90"
VERSION = "1.1.0"
TASK_ID = "1e99030a2d90"
SUMMARY = "Blank centers with red cells in all four cardinal directions become yellow."

INVARIANTS = [
    "background is 0",
    "each target center is blank before transformation",
    "target centers have red neighbors above, below, left, and right",
    "diamond patterns are separated enough to avoid accidental extra centers",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_diamonds", "partial_diamonds", "wrong_arm_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_diamonds":     {"type": "int", "default": "rng 2..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_red_diamonds",
                       "valid": "spaced_red_diamonds"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        n_diamonds = ctx.draw_int("n_diamonds", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_diamonds = ctx.draw_int("n_diamonds", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
        n_diamonds = ctx.draw_int("n_diamonds", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    centers = [(r, c) for r in range(1, h - 1, 3) for c in range(1, w - 1, 3)]
    rng.shuffle(centers)
    for r, c in centers[:n_diamonds]:
        for rr, cc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            g[rr][cc] = 2
    if not any(2 in row for row in g):
        g[0][1] = 2
        g[2][1] = 2
        g[1][0] = 2
        g[1][2] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_diamonds":
        # blank → no diamond cavity, rule has no effect
        return g
    if name == "partial_diamonds":
        # only 3 of 4 red arms → predicate fails
        g[1][3] = 2; g[2][2] = 2; g[2][4] = 2  # missing bottom arm
        g[5][6] = 2; g[5][8] = 2; g[6][7] = 2  # missing top arm
        return g
    if name == "wrong_arm_color":
        # arms are color 4 (yellow) instead of 2 (red) → predicate "red arms" fails
        g[1][3] = 4; g[3][3] = 4; g[2][2] = 4; g[2][4] = 4
        g[5][6] = 6; g[7][6] = 6; g[6][5] = 6; g[6][7] = 6
        return g
    return g
