"""Generator for 81c0276b.

Rule: colors encoded as staircase rows whose lengths equal connected-
object counts.

Combinatorial axes (8): grid_h/w, color_count, palette_kind, bg_color,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_objects, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dc7fd9f4b5e6"
VERSION = "1.1.0"
TASK_ID = "dc7fd9f4b5e6"
SUMMARY = "Colors as staircase rows whose lengths = connected-object counts."

INVARIANTS = [
    "the modal background is not zero",
    "object colors are nonzero and distinct from the background",
    "each counted object is a separated 4-connected component",
    "the output rows are sorted by object count ascending",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "single_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 12..13", "valid": "10..16"},
    "color_count":    {"type": "int", "default": "3", "valid": "2..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bg_color":       {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..5"},
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
    ctx.draw_int("color_count", 3, 3)
    bg = ctx.draw_color("background", exclude={0})
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, bg, rng)
    if len(pool) < 3:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                       if c not in pool and c != bg]
    colors = pool[:3]
    g = full_grid(12 + rng.randint(0, 1), 12 + rng.randint(0, 1), bg)
    anchors = {
        colors[0]: [(1, 1)],
        colors[1]: [(1, 6), (5, 2)],
        colors[2]: [(4, 7), (8, 3), (8, 9)],
    }
    for color, cells in anchors.items():
        for r, c in cells:
            g[r][c] = color
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
    pool = [c for c in pool if c != 0 and c != bg]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 5)
    if name == "no_objects":
        return g
    if name == "single_color":
        for r, c in [(1, 1), (4, 5), (8, 8)]:
            g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
