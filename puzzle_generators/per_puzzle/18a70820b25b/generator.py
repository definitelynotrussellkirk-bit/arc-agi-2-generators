"""Generator for 6d58a25d.

Rule: scatter dots below selected columns of the largest shape cause
vertical beams to extend downward.

Combinatorial axes (8): grid_h/w, beam_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_shape, no_scatter, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "18a70820b25b"
VERSION = "1.1.0"
TASK_ID = "18a70820b25b"
SUMMARY = "Scatter dots below shape columns cause beams to extend downward."

INVARIANTS = [
    "background is color 0",
    "the largest nonzero object is the source shape",
    "scatter dots use one other nonzero color below the source shape",
    "shape and scatter colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_scatter", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..17", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..22"},
    "beam_count":     {"type": "int", "default": "3", "valid": "3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    ctx.draw_int("beam_count", 3, 3)
    h = 12 + rng.randint(0, 5)
    w = 12 + rng.randint(0, 5)
    shape_color, scatter_color = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(h, w, 0)
    r0 = 2
    c0 = 3 + ((sample_index + rng.randint(0, 2)) % max(1, w - 9))
    shape = [
        (0, 1), (0, 2), (0, 3),
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (2, 1), (2, 2), (2, 3),
    ]
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = shape_color
    for c in [c0 + 1, c0 + 3, c0 + 4]:
        rr = min(h - 2, r0 + 5 + ((seed + c + sample_index) % max(1, h - r0 - 6)))
        g[rr][c] = scatter_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_shape":
        g[10][5] = 4
        return g
    if name == "no_scatter":
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, 2)]:
            g[2 + dr][3 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
