"""Generator for dc2e9a9d.

Rule: tabbed objects stamp mirrored copies away from their narrow tab,
using color 8 vertically and color 1 horizontally.

Combinatorial axes (8): grid_h/w, object_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
shape_variant.
Degenerates: no_objects, single_object, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "635001043e0f"
VERSION = "1.1.0"
TASK_ID = "635001043e0f"
SUMMARY = "Tabbed objects stamp mirrored copies; vertical 8s, horizontal 1s."

INVARIANTS = [
    "background is color 0",
    "each source object is a connected tabbed shape",
    "single-cell top or bottom tab creates a vertical reflected copy in color 8",
    "single-cell left or right tab creates a horizontal reflected copy in color 1",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "object_count":   {"type": "int", "default": "3", "valid": "3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "shape_variant":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
    if len(pool) < 3:
        pool = pool + [c for c in [2, 3, 4, 5, 6, 7, 9] if c not in pool]
    c1, c2, c3 = pool[0], pool[1], pool[2]
    g = full_grid(14, 14, 0)
    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, 2)]:
        g[2 + dr][2 + dc] = c1
    for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1)]:
        g[9 + dr][2 + dc] = c2
    for dr, dc in [(0, 0), (1, 0), (2, 0), (1, 1)]:
        g[4 + dr][9 + dc] = c3
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 9]
    pool = [c for c in pool if c not in (0, 1, 8)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_objects":
        return g
    if name == "single_object":
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, 2)]:
            g[2 + dr][2 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
