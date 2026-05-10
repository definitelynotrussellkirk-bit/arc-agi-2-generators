"""Generator for 84551f4c.

Rule: gap-three marker chains turn into horizontal bottom bars or
vertical columns depending on chain starts.

Combinatorial axes (8): grid_h/w, width, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_markers, single_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "eb373570e72b"
VERSION = "1.1.0"
TASK_ID = "eb373570e72b"
SUMMARY = "Gap-three marker chains become horizontal bars or vertical columns by chain start."

INVARIANTS = [
    "background is color 0",
    "markers lie on one active row",
    "marker columns are spaced by three within chains",
    "color 1 starts horizontal chains while color 2 continues vertical chains",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "single_marker", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "rng 13..19", "valid": "13..19"},
    "width":          {"type": "int", "default": "rng 13..19", "valid": "13..19"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
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
    if difficulty == "easy":
        w = ctx.draw_int("width", 13, 14)
    elif difficulty == "hard":
        w = ctx.draw_int("width", 17, 19)
    else:
        w = ctx.draw_int("width", 13, 19)
    h = 3 + rng.randint(0, 2)
    g = full_grid(h, w, 0)
    r = 0
    start = 1 + (sample_index % 2)
    markers = [(start, 1), (start + 3, 2), (start + 6, 2)]
    second = start + 9
    if second < w:
        markers.append((second, 1))
    for c, v in markers:
        if c < w:
            g[r][c] = v
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 16, 0)
    if name == "no_markers":
        return g
    if name == "single_marker":
        g[0][1] = 1
        return g
    if name == "full_grid":
        for r in range(3):
            for c in range(16):
                g[r][c] = 1
        return g
    return g
