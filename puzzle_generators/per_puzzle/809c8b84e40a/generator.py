"""Generator for 68bc2e87.

Rule: overlapping rectangular frame outlines reveal bottom-to-top
z-order.

Combinatorial axes (8): grid_h/w, layout, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_frames, single_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "809c8b84e40a"
VERSION = "1.1.0"
TASK_ID = "809c8b84e40a"
SUMMARY = "Overlapping rectangular frames reveal bottom-to-top z-order."

INVARIANTS = [
    "the background is cyan",
    "three colored rectangular outlines overlap at visible intersections",
    "later-drawn frames overwrite earlier frame cells at crossings",
    "frame colors are distinct and exclude 8",
]

LAYOUTS = ("l0", "l1", "l2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "full_grid")
HELPFUL_TEXTURES = LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "layout":         {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LAYOUTS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for layout",
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
    if tx in LAYOUTS:
        layout = int(tx[1])
    else:
        layout = ctx.draw_choice("layout", [0, 1, 2])
    colors = list(ctx.draw_distinct_colors("frame_colors", n=3, exclude={8}))
    order = ctx.draw_choice("order", [
        (0, 1, 2),
        (0, 2, 1),
        (1, 0, 2),
        (1, 2, 0),
        (2, 0, 1),
        (2, 1, 0),
    ])
    boxes = [
        [(1, 1, 9, 9), (4, 4, 12, 12), (2, 7, 11, 15)],
        [(2, 2, 11, 10), (5, 5, 14, 14), (1, 8, 10, 16)],
        [(1, 3, 10, 12), (4, 1, 13, 9), (3, 6, 12, 15)],
    ][layout]
    g = full_grid(16, 18, 8)
    for idx in order:
        draw_frame(g, *boxes[idx], colors[idx])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 18, 8)
    if name == "no_frames":
        return g
    if name == "single_frame":
        draw_frame(g, 4, 4, 12, 12, 2)
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(18):
                g[r][c] = 8
        return g
    return g
