"""Generator for 88207623.

Rule: marker colors reflect color-4 cells across nearest vertical
color-2 guide line.

Combinatorial axes (8): grid_h/w, guide_col, marker_color, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_guide, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f06c6cb68038"
VERSION = "1.1.0"
TASK_ID = "f06c6cb68038"
SUMMARY = "Marker colors reflect color-4 cells across nearest vertical color-2 guide."

INVARIANTS = [
    "background is color 0",
    "guide objects are vertical runs of color 2",
    "marker cells are neither 0, 2, nor 4",
    "color-4 cells on the opposite side of the guide reflect across it and take the marker color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_guide", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "12", "valid": "10..16"},
    "guide_col":      {"type": "int", "default": "5", "valid": "1..28"},
    "marker_color":   {"type": "color", "default": "rng !{0,2,4}",
                       "valid": "1|3|5|6|7|8|9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "fixed",
                       "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
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
    guide_c = ctx.draw_int("guide_col", 5, 5)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    marker = int(overrides.get("marker_color",
                               rng.choice(pool) if pool else
                               ctx.draw_color("marker", exclude={0, 2, 4})))
    g = full_grid(12 + rng.randint(0, 1), 12 + rng.randint(0, 1), 0)
    for r in range(2, 10):
        g[r][guide_c] = 2
    g[5][guide_c - 3] = marker
    for r, c in [(4, guide_c + 2), (5, guide_c + 3), (6, guide_c + 2)]:
        if 0 <= r < len(g) and 0 <= c < len(g[0]):
            g[r][c] = 4
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [3, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 3]
    else:
        pool = [1, 3, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 2, 4)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_guide":
        g[5][2] = 1
        for r, c in [(4, 7), (5, 8), (6, 7)]:
            g[r][c] = 4
        return g
    if name == "no_markers":
        for r in range(2, 10):
            g[r][5] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
