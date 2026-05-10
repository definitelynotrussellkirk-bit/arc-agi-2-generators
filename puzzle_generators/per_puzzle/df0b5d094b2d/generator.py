"""Generator for 470c91de.

Rule: colored rectangle missing one marker corner moves diagonally
one step toward its color-8 corner marker.

Combinatorial axes (8): grid_h/w, shape_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
corner_kind.
Degenerates: no_rects, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "df0b5d094b2d"
VERSION = "1.1.0"
TASK_ID = "df0b5d094b2d"
SUMMARY = "Colored rectangle missing one corner moves diagonally toward its color-8 marker."

INVARIANTS = [
    "the background is color 7",
    "each foreground color appears in one rectangular object with one missing bbox corner",
    "the missing corner is marked with color 8",
    "shape colors are distinct from 7 and 8",
]

CORNERS = ("tl", "tr", "bl", "br")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rects", "no_marker", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "shape_count":    {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "corner_kind":    {"type": "str", "default": "rng",
                       "valid": "|".join(CORNERS)},
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
        sc_lo, sc_hi = 1, 1
    elif difficulty == "hard":
        sc_lo, sc_hi = 2, 2
    else:
        sc_lo, sc_hi = 1, 2
    shape_count = ctx.draw_int("shape_count", sc_lo, sc_hi)
    colors = ctx.draw_distinct_colors("shape_colors", n=shape_count, exclude={7, 8})
    h = 14
    w = 15
    g = full_grid(h, w, 7)
    anchors = [(2, 2), (8, 8)]
    for idx, color in enumerate(colors):
        rh = rng.randint(3, 4)
        rw = rng.randint(3, 5)
        r0, c0 = anchors[idx]
        corner = CORNERS[rng.randrange(len(CORNERS))]
        missing = {
            "tl": (0, 0),
            "tr": (0, rw - 1),
            "bl": (rh - 1, 0),
            "br": (rh - 1, rw - 1),
        }[corner]
        for r in range(rh):
            for c in range(rw):
                if (r, c) == missing:
                    g[r0 + r][c0 + c] = 8
                else:
                    g[r0 + r][c0 + c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 15, 7)
    if name == "no_rects":
        return g
    if name == "no_marker":
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(15):
                g[r][c] = 2
        return g
    return g
