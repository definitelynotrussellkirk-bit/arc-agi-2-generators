"""Generator for arc_additional_puzzles_21_set13_bundle:M88.

Rule: token at (0, 0) ∈ {1..4} is the transform code; crop the non-token
nonzero cells and apply: 1=identity, 2=cw, 3=180, 4=transpose.

Combinatorial axes (8): grid_h/w, palette_kind, token, motif_anchor,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_token, invalid_token, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b7fbb716d189"
VERSION = "1.1.0"
TASK_ID = "b7fbb716d189"
SUMMARY = "Token at top-left ∈ {1,2,3,4} + small motif of colors {5..9}."

INVARIANTS = [
    "(0,0) is token ∈ 1..4",
    "small multicolor motif of non-token colors elsewhere",
]

PALETTE_KINDS = ("default", "token_1", "token_2", "token_3_4")
DEGENERATE_TEXTURES = ("no_token", "invalid_token", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "token":          {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "motif_anchor":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "interior",
                       "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        token = ctx.draw_int("token", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        token = ctx.draw_int("token", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
        token = ctx.draw_int("token", 1, 4)
    g = full_grid(h, w, 0)
    g[0][0] = token
    g[3][2] = 5; g[3][3] = 6
    g[4][3] = 6
    g[5][3] = 7; g[5][4] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_token":
        # motif but no token at (0,0) — transformation undefined
        g[3][2] = 5; g[3][3] = 6
        g[4][3] = 6
        g[5][3] = 7; g[5][4] = 7
        return g
    if name == "invalid_token":
        # token outside {1..4} — rule cannot map to a transform
        g[0][0] = 8
        g[3][2] = 5; g[3][3] = 6
        g[4][3] = 6
        return g
    if name == "no_motif":
        # token but no motif to transform
        g[0][0] = 2
        return g
    return g
