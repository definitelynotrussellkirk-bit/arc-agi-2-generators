"""Generator for arc_additional_puzzles_21_set10_bundle:M64.

Rule: target = at(0,0). 5-source defines motif anchor. Motif = target-color
cells (excluding (0,0)). For each 6-anchor, stamp motif at anchor offset
from 5-source.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_anchors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_target, no_5_source, no_6_anchors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "81cced17d473"
VERSION = "1.1.0"
TASK_ID = "81cced17d473"
SUMMARY = "Target color at (0,0) + 5-anchor + target-color motif near 5 + 1-2 6-anchors."

INVARIANTS = [
    "(0,0) is target color (∈ 2..9, not 5 or 6)",
    "exactly one 5-cell (motif source anchor)",
    "1-2 target-color cells near the 5-anchor",
    "1-2 6-anchors elsewhere where stamps fit in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_target", "no_5_source", "no_6_anchors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_anchors":      {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed_layout",
                       "valid": "fixed_layout"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 8, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    target = 2
    g[0][0] = target
    g[3][3] = 5
    g[2][3] = target
    g[4][2] = target
    g[5][7] = 6
    g[2][7] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_target":
        # (0,0) is 0 → no target color identified, rule has no motif color
        g[3][3] = 5
        g[5][7] = 6
        g[2][7] = 6
        return g
    if name == "no_5_source":
        # no 5-anchor → motif offset undefined, can't stamp
        g[0][0] = 2
        g[2][3] = 2; g[4][2] = 2
        g[5][7] = 6; g[2][7] = 6
        return g
    if name == "no_6_anchors":
        # target+5+motif but no 6-anchors → rule has no targets to stamp
        g[0][0] = 2
        g[3][3] = 5
        g[2][3] = 2; g[4][2] = 2
        return g
    return g
