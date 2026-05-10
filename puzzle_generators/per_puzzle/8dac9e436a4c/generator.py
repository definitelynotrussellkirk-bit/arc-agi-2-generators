"""Generator for arc_additional_puzzle_bank_volume16:M106.

Rule: for each 6-blob that is exactly the bbox border (hollow rectangle
frame), paint cells strictly inside its bbox to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_size,
solid_size, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_frame, no_solid, both_hollow.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "8dac9e436a4c"
VERSION = "1.1.0"
TASK_ID = "8dac9e436a4c"
SUMMARY = "1 hollow 6-frame + 1 solid 6-rect distractor + decoration."

INVARIANTS = [
    "exactly one hollow 6-frame (h≥3, w≥3)",
    "exactly one solid 6-rect (NOT a frame)",
    "decoration is non-6 cell",
]

PALETTE_KINDS = ("default", "small_frame", "wide_frame", "tall_frame")
DEGENERATE_TEXTURES = ("no_frame", "no_solid", "both_hollow")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_size":     {"type": "str", "default": "4x4", "valid": "4x4"},
    "solid_size":     {"type": "str", "default": "3x2", "valid": "3x2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "split_corners", "valid": "split_corners"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _solid(g, r1, c1, r2, c2, color):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            g[r][c] = color


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
    draw_frame(g, 1, 1, 4, 4, 6)
    _solid(g, 2, 7, 4, 8, 6)
    g[h - 1][0] = 3; g[h - 1][1] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # only solid distractor → no hollow frame to fill
        _solid(g, 2, 7, 4, 8, 6)
        g[h - 1][0] = 3
        return g
    if name == "no_solid":
        # frame only — no distractor, but predicate "exactly 1 frame + 1 solid" fails
        draw_frame(g, 1, 1, 4, 4, 6)
        g[h - 1][0] = 3
        return g
    if name == "both_hollow":
        # two frames, no solid → both qualify ambiguously
        draw_frame(g, 1, 1, 4, 4, 6)
        draw_frame(g, 3, 6, 4, 3, 6)
        g[h - 1][0] = 3
        return g
    return g
