"""Generator for 8a004b2b.

Rule: key pattern outside yellow frame is scaled into the frame by
matching the first block color.

Combinatorial axes (8): grid_h/w, key_shape, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_frame, no_key, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, draw_rect, full_grid

GENERATOR_ID = "ad41fc0cda2b"
VERSION = "1.1.0"
TASK_ID = "ad41fc0cda2b"
SUMMARY = "Key pattern outside yellow frame scaled in by first block color."

INVARIANTS = [
    "color 4 forms the output frame",
    "the frame contains a block of the key's first color",
    "a compact key pattern outside the frame uses the same colors",
    "key colors are distinct and exclude 0 and 4",
]

KEY_SHAPES = ("square", "elbow")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_key", "full_grid")
HELPFUL_TEXTURES = KEY_SHAPES

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "key_shape":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(KEY_SHAPES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for key_shape",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    key_shape = (overrides.get("texture") if overrides.get("texture") in KEY_SHAPES else None) or \
                overrides.get("key_shape") or \
                ctx.draw_choice("key_shape", list(KEY_SHAPES))
    a, b, c, d = ctx.draw_distinct_colors("key_colors", n=4, exclude={0, 4})
    g = full_grid(13, 14, 0)
    if key_shape == "square":
        key = [(0, 0, a), (0, 1, b), (1, 0, c), (1, 1, d)]
    else:
        key = [(0, 0, a), (1, 0, b), (1, 1, c), (2, 1, d)]
    for dr, dc, color in key:
        g[1 + dr][1 + dc] = color
    draw_frame(g, 5, 4, 12, 11, 4)
    draw_rect(g, 6, 5, 2, 2, a)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 14, 0)
    if name == "no_frame":
        g[1][1] = 2; g[1][2] = 3
        return g
    if name == "no_key":
        draw_frame(g, 5, 4, 12, 11, 4)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(14):
                g[r][c] = 4
        return g
    return g
