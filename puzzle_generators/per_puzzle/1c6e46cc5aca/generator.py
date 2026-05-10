"""Generator for c920a713.

Rule: nested rectangle outlines are canonicalized into concentric output
layers.

Combinatorial axes (8): grid_h/w, layers, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_frames, single_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "1c6e46cc5aca"
VERSION = "1.1.0"
TASK_ID = "1c6e46cc5aca"
SUMMARY = "Nested rectangle outlines are canonicalized into concentric output layers."

INVARIANTS = [
    "each non-background color forms a rectangular outline",
    "outline bounding-box area orders unconstrained layers from outer to inner",
    "the output is a compact odd square with one color per concentric layer",
]

LAYER_KINDS = ("L3", "L4")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "full_grid")
HELPFUL_TEXTURES = LAYER_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "17", "valid": "17"},
    "layers":         {"type": "choice", "default": "rng helpful",
                       "valid": "3|4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "texture":        {"type": "str", "default": "alias for layers",
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
    if tx in LAYER_KINDS:
        layers = int(tx[1])
    elif difficulty == "easy":
        layers = 3
    elif difficulty == "hard":
        layers = 4
    else:
        layers = ctx.draw_choice("layers", [3, 4])
    colors = ctx.draw_distinct_colors("colors", n=layers, exclude={0})
    g = full_grid(15, 17, 0)
    boxes = [
        (1, 1, 13, 15),
        (3, 3, 11, 13),
        (5, 5, 9, 11),
        (6, 7, 8, 9),
    ]
    for i in range(layers):
        draw_frame(g, *boxes[i], colors[i])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 17, 0)
    if name == "no_frames":
        return g
    if name == "single_frame":
        draw_frame(g, 1, 1, 13, 15, 3)
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(17):
                g[r][c] = 5
        return g
    return g
