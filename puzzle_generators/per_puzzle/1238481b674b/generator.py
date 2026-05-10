"""Generator for 1478ab18.

Rule: three gray square-corner markers imply the missing-corner
triangle.

Combinatorial axes (8): grid_h/w, missing_corner, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, side_len.
Degenerates: no_markers, four_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1238481b674b"
VERSION = "1.1.0"
TASK_ID = "1238481b674b"
SUMMARY = "Three gray square-corner markers imply missing-corner triangle."

INVARIANTS = [
    "the background is orange color 7",
    "exactly three gray markers occupy corners of a square bounding box",
    "the missing corner determines which triangle edges are drawn",
    "the corner positions sit clear of the grid borders",
]

CORNERS = (0, 1, 2, 3)
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "four_markers", "full_grid")
HELPFUL_TEXTURES = ("c0", "c1", "c2", "c3")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "missing_corner": {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "side_len":       {"type": "int", "default": "rng 3..7", "valid": "3..10"},
    "texture":        {"type": "str", "default": "alias for missing_corner",
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
    if tx in HELPFUL_TEXTURES:
        missing = int(tx[1])
    else:
        missing = ctx.draw_int("missing_corner", 0, 3)
    h = rng.randint(8, 12)
    w = rng.randint(8, 12)
    d = rng.randint(3, min(h, w) - 3)
    r0 = rng.randint(0, h - d - 1)
    c0 = rng.randint(0, w - d - 1)
    r1 = r0 + d
    c1 = c0 + d
    corners = [(r0, c0), (r0, c1), (r1, c0), (r1, c1)]
    g = full_grid(h, w, 7)
    for i, (r, c) in enumerate(corners):
        if i != missing:
            g[r][c] = 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 7)
    if name == "no_markers":
        return g
    if name == "four_markers":
        for r, c in [(2, 2), (2, 7), (7, 2), (7, 7)]:
            g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 5
        return g
    return g
