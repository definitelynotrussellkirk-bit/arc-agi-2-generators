"""Generator for 9f41bd9c.

Rule: color-5 patch slides to far side; rows above and below color-6
boundary filled.

Combinatorial axes (8): grid_h/w, side, boundary_row, palette_kind,
patch_position, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_patch, no_boundary, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "ad4e576b99c4"
VERSION = "1.1.0"
TASK_ID = "ad4e576b99c4"
SUMMARY = "Color-5 patch slides to the far side; rows are filled around the color-6 boundary."

INVARIANTS = [
    "a compact color-5 patch defines the copied width",
    "a color-6 marker row defines the boundary row",
    "patches starting left of center move right; right-of-center patches move left",
    "the output background is split into colors 1, 9, and 6 around that boundary",
]

PATCH = [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)]
SIDES = ("left", "right")
DEGENERATE_TEXTURES = ("no_patch", "no_boundary", "full_grid")
HELPFUL_TEXTURES = SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "side":           {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SIDES)},
    "boundary_row":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "patch_position": {"type": "str", "default": "rng",
                       "valid": "near|far|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for side",
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
        h_lo, h_hi = 8, 9
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 9, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 4)
    side = (overrides.get("texture") if overrides.get("texture") in SIDES else None) or \
           overrides.get("side") or \
           ctx.draw_choice("side", list(SIDES))
    g = full_grid(h, w, 0)
    br = int(overrides.get("boundary_row",
                           ctx.draw_int("boundary_row", 1, 2)))
    br = max(1, min(3, br))
    g[br][0] = 6
    r0 = br + 2
    if r0 + 2 >= h:
        r0 = max(2, h - 4)
    c0 = 1 if side == "left" else max(1, w - 4)
    paint_at(g, r0, c0, PATCH, 5)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_patch":
        g[1][0] = 6
        return g
    if name == "no_boundary":
        paint_at(g, 3, 3, PATCH, 5)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
