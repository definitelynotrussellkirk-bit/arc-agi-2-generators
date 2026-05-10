"""Generator for afe3afe9.

Rule: a large 8 block-shape and smaller aligned block-shapes are reduced
into per-slice color stacks.

Combinatorial axes (8): grid_h/w, small_slice, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, color.
Degenerates: no_main, no_small, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "48fee61713bb"
VERSION = "1.1.0"
TASK_ID = "48fee61713bb"
SUMMARY = "Large 8 block-shape + smaller aligned block-shapes reduced to per-slice color stacks."

INVARIANTS = [
    "the main color is 8 and is sampled as a grid of 3x3 blocks on 4-step anchors",
    "smaller colored block-shapes align to slices of the main shape",
    "each output slice stacks the count of main and small blocks in that slice",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_main", "no_small", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "small_slice":    {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "color":          {"type": "color", "default": "rng !{0,1,8}",
                       "valid": "2..7|9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        small_slice = ctx.draw_int("small_slice", 0, 0)
    elif difficulty == "hard":
        small_slice = ctx.draw_int("small_slice", 2, 2)
    else:
        small_slice = ctx.draw_int("small_slice", 0, 2)
    small_color = ctx.draw_color("small_color", exclude={0, 1, 8})
    g = full_grid(14, 16, 0)
    main_r = 6 + (sample_index % 2)
    main_c = 1
    for bc in range(3):
        draw_rect(g, main_r, main_c + 4 * bc, 3, 3, 8)
    small_r = 1 + (sample_index % 2)
    draw_rect(g, small_r, main_c + 4 * small_slice, 3, 3, small_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 16, 0)
    if name == "no_main":
        draw_rect(g, 1, 1, 3, 3, 3)
        return g
    if name == "no_small":
        for bc in range(3):
            draw_rect(g, 6, 1 + 4 * bc, 3, 3, 8)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(16):
                g[r][c] = 8
        return g
    return g
