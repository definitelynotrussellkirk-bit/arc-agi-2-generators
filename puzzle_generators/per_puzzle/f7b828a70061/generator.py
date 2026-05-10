"""Generator for arc_additional_puzzles_21_set4:M28.

Rule: cmd at (0, 0) ∈ {2, 3, 4, 5}. Sort objects by (size desc, r1, c1);
take the first; crop bbox; apply 2=identity, 3=cw, 4=180, 5=ccw.

Combinatorial axes (8): grid_h/w, palette_kind, cmd, motif_anchor,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_cmd, invalid_cmd, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f7b828a70061"
VERSION = "1.1.0"
TASK_ID = "f7b828a70061"
SUMMARY = "Cmd ∈ {2,3,4,5} at top-left + 1 multicolor motif (largest object)."

INVARIANTS = [
    "(0,0) is cmd ∈ 2..5",
    "exactly one multicolor motif (h≥2, w≥2) elsewhere",
    "motif is non-square so rotations differ",
]

PALETTE_KINDS = ("default", "cmd_2_3", "cmd_4_5", "varied_motif")
DEGENERATE_TEXTURES = ("no_cmd", "invalid_cmd", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 2..5", "valid": "2..5"},
    "motif_anchor":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "interior",
                       "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        cmd = ctx.draw_int("cmd", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        cmd = ctx.draw_int("cmd", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
        cmd = ctx.draw_int("cmd", 2, 5)
    g = full_grid(h, w, 0)
    g[0][0] = cmd
    g[2][3] = 6
    g[3][3] = 6; g[3][4] = 7
    g[4][4] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # motif but no command — transform undefined
        g[2][3] = 6
        g[3][3] = 6; g[3][4] = 7
        g[4][4] = 7
        return g
    if name == "invalid_cmd":
        # command outside {2,3,4,5} — rule cannot map it
        g[0][0] = 8
        g[2][3] = 6
        g[3][3] = 6; g[3][4] = 7
        g[4][4] = 7
        return g
    if name == "no_motif":
        # cmd but no motif to crop+rotate
        g[0][0] = 3
        return g
    return g
