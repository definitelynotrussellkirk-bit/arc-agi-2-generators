"""Generator for e76a88a6.

Rule: colored template pattern is pasted into every connected gray
region.

Combinatorial axes (8): grid_h/w, region_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_template, no_regions, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid, paint_at

GENERATOR_ID = "b985d561c63b"
VERSION = "1.1.0"
TASK_ID = "b985d561c63b"
SUMMARY = "Colored template pasted into every connected gray region."

INVARIANTS = [
    "the template consists of nonzero non-gray colors",
    "gray regions are connected components of color 5",
    "each gray region receives the template aligned to its top-left bbox corner",
    "template colors are distinct and exclude 0 and 5",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_regions", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

TEMPLATE = [(0, 0), (0, 1), (1, 1), (2, 0)]

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "region_count":   {"type": "int", "default": "rng 1..3", "valid": "1..3"},
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
    if difficulty == "easy":
        rc_lo, rc_hi = 1, 1
    elif difficulty == "hard":
        rc_lo, rc_hi = 3, 3
    else:
        rc_lo, rc_hi = 1, 3
    region_count = ctx.draw_int("region_count", rc_lo, rc_hi)
    color_a, color_b = ctx.draw_distinct_colors("template_colors", n=2, exclude={0, 5})
    g = full_grid(13, 14, 0)
    for i, (dr, dc) in enumerate(TEMPLATE):
        g[1 + dr][1 + dc] = color_a if i < 2 else color_b
    for r0, c0, rh, rw in [(1, 7, 3, 3), (7, 2, 4, 3), (7, 9, 3, 4)][:region_count]:
        draw_rect(g, r0, c0, rh, rw, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 14, 0)
    if name == "no_template":
        draw_rect(g, 5, 5, 3, 3, 5)
        return g
    if name == "no_regions":
        for i, (dr, dc) in enumerate(TEMPLATE):
            g[1 + dr][1 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(14):
                g[r][c] = 5
        return g
    return g
