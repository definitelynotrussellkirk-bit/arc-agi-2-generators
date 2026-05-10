"""Generator for arc_puzzle_bank_21_set9_s:S9_E2 — fill the bbox of the unique 2-cell color.

Rule: exactly one color appears twice; its two cells define a filled
rectangle.

Combinatorial axes (8): grid_h, grid_w, palette_kind, box_height,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pair, multiple_pairs, collinear_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e282a664f807"
VERSION = "1.1.0"
TASK_ID = "e282a664f807"
SUMMARY = "Exactly one color appears twice; its two cells define a filled rectangle."

INVARIANTS = [
    "background is 0",
    "one selected color appears in exactly two cells",
    "no other nonzero color appears exactly twice",
    "the output is the selected color's bounding box rectangle",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pair", "multiple_pairs", "collinear_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "box_height":     {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "diagonal_pair_with_distractors",
                       "valid": "diagonal_pair_with_distractors"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        box_h = min(ctx.draw_int("box_height", 2, 3), h - 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        box_h = min(ctx.draw_int("box_height", 4, 5), h - 2)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        box_h = min(ctx.draw_int("box_height", 2, 5), h - 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    box_w = rng.randint(2, min(5, w - 2))
    r1 = rng.randint(0, h - box_h)
    c1 = rng.randint(0, w - box_w)
    color = rng.choice([2, 3, 4, 6, 7])
    g[r1][c1] = color
    g[r1 + box_h - 1][c1 + box_w - 1] = color
    dcolor = 9 if color != 9 else 8
    placed = 0
    for rr in range(h - 1, -1, -1):
        for cc in range(w - 1, -1, -1):
            if g[rr][cc] == 0:
                g[rr][cc] = dcolor
                placed += 1
                if placed == 3:
                    return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_pair":
        # singletons only — no color appears exactly twice
        g[1][1] = 4
        g[3][5] = 6
        g[5][8] = 7
        return g
    if name == "multiple_pairs":
        # two different colors each appear twice → ambiguous selection
        g[1][1] = 4; g[3][3] = 4
        g[5][5] = 6; g[6][7] = 6
        return g
    if name == "collinear_pair":
        # 2-cell pair on same row/col → bbox is a line, not a rectangle
        g[2][1] = 4; g[2][8] = 4
        g[7][3] = 9
        return g
    return g
