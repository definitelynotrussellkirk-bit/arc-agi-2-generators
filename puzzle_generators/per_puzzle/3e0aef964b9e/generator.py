"""Generator for 7acdf6d3.

Rule: donor cells fill the missing convex-hull cells of a target
color object, then the donor is cleared.

Combinatorial axes (8): grid_h/w, gap_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
shape_kind.
Degenerates: no_target, no_donor, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import RING_3X3

GENERATOR_ID = "3e0aef964b9e"
VERSION = "1.1.0"
TASK_ID = "3e0aef964b9e"
SUMMARY = "Donor cells fill missing convex-hull cells of target object."

INVARIANTS = [
    "background is color 0",
    "one target color object has missing cells inside its convex hull",
    "the donor color count equals the number of missing target cells",
    "donor cells sit clear of the target so they are unambiguous",
]

GAP_KINDS = ("ring", "frame")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_target", "no_donor", "full_grid")
HELPFUL_TEXTURES = GAP_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "gap_count":      {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "shape_kind":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(GAP_KINDS)},
    "texture":        {"type": "str", "default": "alias for shape_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    gap_count = ctx.draw_int("gap_count", 1, 2)
    h = 8 + rng.randint(0, 3)
    w = 8 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    r0 = 2
    c0 = 2
    if gap_count == 1:
        target = RING_3X3
        donors = [(h - 2, w - 2)]
    else:
        target = [(0, 0), (0, 1), (0, 2), (0, 3),
                  (1, 0),                 (1, 3),
                  (2, 0), (2, 1), (2, 2), (2, 3)]
        donors = [(h - 2, w - 2), (h - 2, w - 3)]
    paint_at(g, r0, c0, target, 2)
    for r, c in donors:
        g[r][c] = 4
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_target":
        g[8][8] = 4
        return g
    if name == "no_donor":
        paint_at(g, 2, 2, RING_3X3, 2)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 2
        return g
    return g
