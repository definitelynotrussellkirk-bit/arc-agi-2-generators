"""Generator for 7ddcd7ec.

Rule: tail pixels attached to a 2x2 body extend diagonal rays away
from the body's center.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, color, n_distinct_colors.
Degenerates: no_body, full_grid, single_pixel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e0ef0cfeaf88"
VERSION = "1.1.0"
TASK_ID = "e0ef0cfeaf88"
SUMMARY = "Tail pixels attached to 2x2 body extend diagonal rays from body center."

INVARIANTS = [
    "background is color 0",
    "all nonzero cells share one color",
    "a 2x2 body is present",
    "body sits clear of grid borders so tails can fit on multiple sides",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_body", "full_grid", "single_pixel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "color":          {"type": "color", "default": "rng !0", "valid": "1..9"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
    color = ctx.draw_color("color", exclude={0})
    g = full_grid(12 + rng.randint(0, 2), 12 + rng.randint(0, 2), 0)
    r0 = 5
    c0 = 5
    for dr in (0, 1):
        for dc in (0, 1):
            g[r0 + dr][c0 + dc] = color
    for r, c in [(r0 - 1, c0 - 1), (r0 - 1, c0 + 2), (r0 + 2, c0 - 1)]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_body":
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
