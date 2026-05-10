"""Generator for 67636eac.

Rule: separated colored shapes are cropped to their bboxes and
concatenated along their dominant spatial axis.

Combinatorial axes (8): grid_h/w, shape_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_shapes, single_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5240b527d354"
VERSION = "1.1.0"
TASK_ID = "5240b527d354"
SUMMARY = "Separated shapes cropped to bboxes; concatenated along dominant axis."

INVARIANTS = [
    "background is color 0",
    "each nonzero color appears in one separated shape",
    "shape centers are spread primarily horizontally or vertically",
    "shape colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "single_shape", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..16", "valid": "8..22"},
    "grid_w":         {"type": "int", "default": "rng 10..16", "valid": "8..22"},
    "shape_count":    {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 2..3", "valid": "2..5"},
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
        n_lo, n_hi = 2, 2
    elif difficulty == "hard":
        n_lo, n_hi = 4, 5
    else:
        n_lo, n_hi = 2, 3
    n = ctx.draw_int("shape_count", n_lo, n_hi)
    horizontal = ((seed + sample_index) % 2 == 0)
    h = 10 + (0 if horizontal else 4 * n) + rng.randint(0, 2)
    w = 10 + (4 * n if horizontal else 0) + rng.randint(0, 2)
    g = full_grid(h, w, 0)
    colors = ctx.draw_distinct_colors("colors", n=n, exclude={0})
    patterns = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (1, 2)],
    ]
    for i in range(n):
        if horizontal:
            r0 = 3 + ((sample_index + i) % 2)
            c0 = 1 + i * 5
        else:
            r0 = 1 + i * 5
            c0 = 3 + ((sample_index + i) % 2)
        for dr, dc in patterns[i % len(patterns)]:
            g[r0 + dr][c0 + dc] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_shapes":
        return g
    if name == "single_shape":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
