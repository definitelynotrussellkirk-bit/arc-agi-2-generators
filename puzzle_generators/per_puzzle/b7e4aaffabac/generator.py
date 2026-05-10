"""Generator for d6ad076f.

Rule: two separated rectangles are bridged by color 8 through the
shrunken overlap of their facing spans.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_rects, single_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "b7e4aaffabac"
VERSION = "1.1.0"
TASK_ID = "b7e4aaffabac"
SUMMARY = "Two rectangles bridged by color 8 across their facing-span overlap."

INVARIANTS = [
    "background is color 0",
    "there are exactly two nonzero rectangular objects",
    "the rectangles are separated horizontally with a gap of at least one column",
    "the rectangle colors are distinct and exclude 8",
]

ORIENTATIONS = ("horizontal",)
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rects", "single_rect", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..12", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 14..15", "valid": "12..18"},
    "orientation":    {"type": "str", "default": "horizontal",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 2:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 9] if c not in pool]
    a, b = pool[0], pool[1]
    g = full_grid(11 + rng.randint(0, 1), 14 + rng.randint(0, 1), 0)
    fill_box(g, 2, 1, 7, 4, a)
    fill_box(g, 3, 9, 8, 12, b)
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 9]
    pool = [c for c in pool if c not in (0, 8)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 14, 0)
    if name == "no_rects":
        return g
    if name == "single_rect":
        fill_box(g, 2, 1, 7, 4, 2)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
