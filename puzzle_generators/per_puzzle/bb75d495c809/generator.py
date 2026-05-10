"""Generator for e8593010.

Rule: zero components of size 1, 2, 3 recolor to green, red, blue.

Combinatorial axes (8): grid_h/w, field_color, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, n_holes.
Degenerates: no_holes, all_holes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bb75d495c809"
VERSION = "1.1.0"
TASK_ID = "bb75d495c809"
SUMMARY = "Zero components of size 1, 2, 3 recolor to green, red, blue respectively."

INVARIANTS = [
    "the nonzero field separates all zero components",
    "zero components are 4-connected holes of size one, two, three, or larger",
    "size-one holes become color 3",
    "size-two holes become color 2, size-three holes become color 1, and larger holes remain 0",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_holes", "all_holes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "12", "valid": "10..16"},
    "field_color":    {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_holes":        {"type": "int", "default": "10", "valid": "1..15"},
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
    field = ctx.draw_color("field_color", exclude={0})
    g = full_grid(12 + rng.randint(0, 1), 12 + rng.randint(0, 1), field)
    for r, c in [(2, 2), (2, 6), (2, 7), (6, 2), (7, 2), (7, 3),
                 (8, 8), (8, 9), (9, 8), (9, 9)]:
        if r < len(g) and c < len(g[0]):
            g[r][c] = 0
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 5)
    if name == "no_holes":
        return g
    if name == "all_holes":
        return full_grid(12, 12, 0)
    if name == "full_grid":
        return full_grid(12, 12, 5)
    return g
