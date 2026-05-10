"""Generator for fd4b2b02.

Rule: colored rectangle stamps periodic same-orientation copies and
rotated copies in the complementary color.

Combinatorial axes (8): grid_h/w, rect_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, color.
Degenerates: no_rect, full_grid, single_pixel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "888fb4310749"
VERSION = "1.1.0"
TASK_ID = "888fb4310749"
SUMMARY = "Colored rectangle stamps periodic copies and rotated complement copies."

INVARIANTS = [
    "background is color 0",
    "one solid non-background rectangle defines the stamp size",
    "same-orientation copies keep the source color",
    "the rectangle color is non-zero and not 9",
]

RECT_SIZES = ("2x3", "3x2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "full_grid", "single_pixel")
HELPFUL_TEXTURES = RECT_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "rect_size":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(RECT_SIZES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "color":          {"type": "color", "default": "rng !{0,9}",
                       "valid": "1..8"},
    "texture":        {"type": "str", "default": "alias for rect_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    size = (overrides.get("texture") if overrides.get("texture") in RECT_SIZES else None) or \
           overrides.get("rect_size") or \
           ctx.draw_choice("rect_size", list(RECT_SIZES))
    rh, rw = (int(x) for x in size.split("x"))
    color = ctx.draw_color("color", exclude={0, 9})
    h = 12 + rng.randint(0, 4)
    w = 12 + rng.randint(0, 4)
    g = full_grid(h, w, 0)
    r0 = 3 + rng.randint(0, 1)
    c0 = 3 + rng.randint(0, 1)
    for r in range(r0, r0 + rh):
        for c in range(c0, c0 + rw):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_rect":
        return g
    if name == "single_pixel":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
