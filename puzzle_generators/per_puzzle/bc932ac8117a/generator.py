"""Generator for arc_puzzle_bank_next21:H14.

Rule: a hollow rectangle transfers its local hole pattern to a same-size
solid rectangle.

Combinatorial axes (8): grid_h, grid_w, palette_kind, box_h, box_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_solid_twin, size_mismatch, no_hole.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, fill_box, full_grid

GENERATOR_ID = "bc932ac8117a"
VERSION = "1.1.0"
TASK_ID = "bc932ac8117a"
SUMMARY = "A hollow rectangle transfers its local hole pattern to a same-size solid rectangle."

INVARIANTS = [
    "one hollow object has enclosed background cells",
    "one solid object has the same bounding-box dimensions",
    "the two objects are disconnected",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_solid_twin", "size_mismatch", "no_hole")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "box_h":          {"type": "int", "default": "rng 5..7", "valid": "5..8"},
    "box_w":          {"type": "int", "default": "rng 5..7", "valid": "5..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "left_hollow_right_solid",
                       "valid": "left_hollow_right_solid"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "paired", "valid": "paired"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        bh = ctx.draw_int("box_h", 5, 5)
        bw = ctx.draw_int("box_w", 5, 6)
    elif difficulty == "hard":
        bh = ctx.draw_int("box_h", 6, 7)
        bw = ctx.draw_int("box_w", 6, 7)
    else:
        bh = ctx.draw_int("box_h", 5, 7)
        bw = ctx.draw_int("box_w", 5, 7)
    g = full_grid(10, 18, 0)
    draw_frame(g, 1, 1, bh, bw, 2)
    fill_box(g, 1, 10, bh, 9 + bw, 3)
    g[1 + bh // 2][1 + bw // 2] = 0
    if bh >= 6 and bw >= 6 and rng.random() < 0.5:
        g[2][3] = 0
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 18, 0)
    if name == "missing_solid_twin":
        # only the hollow object exists → no twin to carve into
        draw_frame(g, 1, 1, 6, 6, 2)
        g[3][3] = 0
        return g
    if name == "size_mismatch":
        # solid object has different bbox dims → twin matching fails
        draw_frame(g, 1, 1, 6, 6, 2)
        g[3][3] = 0
        fill_box(g, 1, 10, 4, 13, 3)
        return g
    if name == "no_hole":
        # hollow object has no enclosed bg cells → hole pattern is empty, transfer is no-op
        draw_frame(g, 1, 1, 6, 6, 2)
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 2
        fill_box(g, 1, 10, 6, 15, 3)
        return g
    return g
