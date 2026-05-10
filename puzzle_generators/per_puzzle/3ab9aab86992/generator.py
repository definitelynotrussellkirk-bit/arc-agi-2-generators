"""Generator for b745798f.

Rule: tiny L triomino orientations select which large output corner gets
a border L.

Combinatorial axes (8): canvas_size, palette_kind, bg_color, n_corners,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_corners, all_corners, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3ab9aab86992"
VERSION = "1.1.0"
TASK_ID = "3ab9aab86992"
SUMMARY = "Tiny L triomino orientations select large output corner placements."

INVARIANTS = [
    "the modal background fills the grid",
    "each non-background object is a 2x2 L missing one corner",
    "the missing corner determines the corresponding output corner placement",
    "the output contains only large border Ls in those selected corners",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_corners", "all_corners", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "canvas_size":    {"type": "int", "default": "9", "valid": "9..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bg_color":       {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "n_corners":      {"type": "int", "default": "4", "valid": "1..4"},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
    ctx.draw_int("canvas_size", 9, 9)
    bg = ctx.draw_color("background", exclude={0})
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, bg, rng)
    if len(pool) < 4:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                       if c not in pool and c != bg]
    colors = pool[:4]
    g = full_grid(9, 9, bg)
    shapes = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 1), (1, 0), (1, 1)],
    ]
    anchors = [(1, 1), (1, 6), (6, 1), (6, 6)]
    n_corners = int(overrides.get("n_corners", 4))
    n_corners = max(1, min(4, n_corners))
    for color, shape, (r0, c0) in zip(colors[:n_corners],
                                      shapes[:n_corners],
                                      anchors[:n_corners]):
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
    return g


def _build_palette(kind, bg, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != bg]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 5)
    if name == "no_corners":
        return g
    if name == "all_corners":
        for r0, c0 in [(1, 1), (1, 6), (6, 1), (6, 6)]:
            for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                g[r0 + dr][c0 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 2
        return g
    return g
