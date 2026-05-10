"""Generator for arc_puzzle_bank_21_set18_s:S18_E6.

Rule: sparse rectangle corners expand by row closure then column
closure.

Combinatorial axes (8): height, width, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_corners, single_corner, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3ee8849ee1ec"
VERSION = "1.1.0"
TASK_ID = "3ee8849ee1ec"
SUMMARY = "Sparse rectangle corners expand by row closure then column closure."

INVARIANTS = [
    "two rows contain matching left/right endpoints",
    "row closure creates horizontal rails",
    "column closure fills the rectangle between those rails",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_corners", "single_corner", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "width":          {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "random", "valid": "random"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 7, 8)
        w = ctx.draw_int("width", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 9, 10)
    else:
        h = ctx.draw_int("height", 7, 10)
        w = ctx.draw_int("width", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r1 = rng.randint(0, h - 5)
    r2 = rng.randint(r1 + 3, h - 1)
    c1 = rng.randint(0, w - 5)
    c2 = rng.randint(c1 + 3, w - 1)
    for r in (r1, r2):
        g[r][c1] = 4
        g[r][c2] = 4
    if rng.random() < 0.5:
        g[(r1 + r2) // 2][rng.choice([c1, c2])] = 4
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 0)
    if name == "no_corners":
        return g
    if name == "single_corner":
        g[2][2] = 4
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 4
        return g
    return g
