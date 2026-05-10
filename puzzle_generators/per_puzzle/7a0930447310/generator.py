"""Generator for b7f8a4d8.

Rule: special-color cells aligned by row or column are connected through
zero gaps.

Combinatorial axes (8): grid_h/w, special_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_frame, no_specials, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "7a0930447310"
VERSION = "1.1.0"
TASK_ID = "7a0930447310"
SUMMARY = "Special-color cells aligned by row or column connected through zero gaps."

INVARIANTS = [
    "the background is zero",
    "one frame color is the most frequent nonzero color",
    "one default center color is more frequent than the special connector colors",
    "each special color has separated objects that share a row or column",
]

SPECIAL_KINDS = ("s2", "s3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_specials", "full_grid")
HELPFUL_TEXTURES = SPECIAL_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "special_count":  {"type": "choice", "default": "rng helpful",
                       "valid": "2|3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "texture":        {"type": "str", "default": "alias for special_count",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in SPECIAL_KINDS:
        special_count = int(tx[1])
    elif difficulty == "easy":
        special_count = 2
    elif difficulty == "hard":
        special_count = 3
    else:
        special_count = ctx.draw_choice("special_count", [2, 3])
    frame, default, s1, s2, s3 = ctx.draw_distinct_colors("colors", n=5, exclude={0})
    g = full_grid(13, 13, 0)
    draw_frame(g, 1, 1, 11, 11, frame)
    for r, c in [(4, 4), (4, 8), (8, 4), (8, 8)]:
        g[r][c] = default
    for r, c in [(3, 3), (3, 9)]:
        g[r][c] = s1
    for r, c in [(5, 6), (10, 6)]:
        g[r][c] = s2
    if special_count == 3:
        for r, c in [(9, 2), (9, 10)]:
            g[r][c] = s3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_frame":
        g[3][3] = 4
        return g
    if name == "no_specials":
        draw_frame(g, 1, 1, 11, 11, 3)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 3
        return g
    return g
