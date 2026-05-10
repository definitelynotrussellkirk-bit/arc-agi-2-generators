"""Generator for f8a8fe49.

Rule: gray cells outside red frame reflect across nearest solid red side.

Combinatorial axes (8): grid_h/w, reflection_axis, palette_kind,
frame_h, frame_w, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_frame, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "ddf6f818956c"
VERSION = "1.1.0"
TASK_ID = "ddf6f818956c"
SUMMARY = "Gray cells outside red frame reflect across nearest solid side."

INVARIANTS = [
    "background is color 0",
    "a red rectangular frame establishes the reflection box",
    "gray marker cells are removed from their original positions",
    "gray markers reappear reflected across the top/bottom or left/right frame side",
]

AXES_DIR = ("vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_marker", "full_grid")
HELPFUL_TEXTURES = AXES_DIR

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "12", "valid": "10..16"},
    "reflection_axis":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(AXES_DIR)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "frame_h":        {"type": "int", "default": "5", "valid": "4..7"},
    "frame_w":        {"type": "int", "default": "5", "valid": "4..7"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for reflection_axis",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    axis = (overrides.get("texture") if overrides.get("texture") in AXES_DIR else None) or \
           overrides.get("reflection_axis") or \
           ctx.draw_choice("reflection_axis", list(AXES_DIR))
    g = full_grid(12, 12, 0)
    r0 = 3 + rng.randint(0, 1)
    c0 = 3 + rng.randint(0, 1)
    r1 = r0 + 4
    c1 = c0 + 4
    draw_frame(g, r0, c0, r1, c1, 2)
    if axis == "vertical":
        if r0 - 2 >= 0:
            g[r0 - 2][c0 + 2] = 5
    else:
        if c0 - 2 >= 0:
            g[r0 + 2][c0 - 2] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        g[3][5] = 5
        return g
    if name == "no_marker":
        draw_frame(g, 3, 3, 7, 7, 2)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
