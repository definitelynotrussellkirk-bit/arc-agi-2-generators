"""Generator for arc_additional_puzzles_21_set9:H62 — row-0 cyclic color map.

Rule: row 0 has 2-4 distinct color codes that define a cyclic mapping.
For each cell in body, recolor by next-in-cycle.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_codes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_codes, no_body, body_uses_unknown_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1f3d51c86f9f"
VERSION = "1.1.0"
TASK_ID = "1f3d51c86f9f"

SUMMARY = "Row 0 has 2-4 distinct color codes; body has scattered cells in those colors."

INVARIANTS = [
    "background is 0",
    "row 0 has 2-4 distinct non-zero color codes at distinct columns",
    "body has scattered non-zero cells in colors from the row-0 set",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_codes", "no_body", "body_uses_unknown_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_codes":        {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "row0_codes_with_body",
                       "valid": "row0_codes_with_body"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..6"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        n = ctx.draw_int("n_codes", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n_codes", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 9, 11)
        n = ctx.draw_int("n_codes", 2, 4)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    codes = rng.sample([2, 3, 4, 5, 6, 7], n)
    cols = rng.sample(range(w), n)
    for c, color in zip(cols, codes):
        g[0][c] = color
    for _ in range(rng.randint(3, 6)):
        for _t in range(40):
            r = rng.randint(2, h - 1); c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice(codes)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_codes":
        # body cells but row 0 is blank → no cycle defined
        g[2][3] = 4
        g[4][6] = 6
        return g
    if name == "no_body":
        # row-0 codes but body is blank → nothing to recolor
        g[0][2] = 4; g[0][5] = 6; g[0][8] = 7
        return g
    if name == "body_uses_unknown_colors":
        # body has colors NOT in the row-0 cycle → cycle lookup fails
        g[0][2] = 4; g[0][5] = 6
        g[3][3] = 8; g[5][6] = 9
        return g
    return g
