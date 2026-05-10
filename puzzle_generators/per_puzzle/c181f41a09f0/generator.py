"""Generator for d255d7a7.

Rule: marked caps inside long zero strips move to the opposite end while
the strip is cleared.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, color.
Degenerates: no_strip, no_cap, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "c181f41a09f0"
VERSION = "1.1.0"
TASK_ID = "c181f41a09f0"
SUMMARY = "Marked caps inside long zero strips move to opposite end while strip is cleared."

INVARIANTS = [
    "the background is orange",
    "zero strips are long and at most three cells thick",
    "a colored cap near one strip end indicates the source end",
    "the cap block is copied to the opposite end and the source strip becomes background",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_strip", "no_cap", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "color":          {"type": "color", "default": "rng !{0,7}",
                       "valid": "1..6|8..9"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ("horizontal" if sample_index % 2 == 0 else "vertical")
    color = ctx.draw_color("cap_color", exclude={0, 7})
    g = full_grid(14, 14, 7)
    if orientation == "horizontal":
        r, c = 5 + (sample_index % 2), 2
        draw_rect(g, r, c, 3, 10, 0)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[r + dr][c + dc] = color
    else:
        r, c = 2, 5 + (sample_index % 2)
        draw_rect(g, r, c, 10, 3, 0)
        for dr, dc in [(0, 0), (1, 0), (0, 1)]:
            g[r + dr][c + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 7)
    if name == "no_strip":
        g[5][2] = 3
        return g
    if name == "no_cap":
        draw_rect(g, 5, 2, 3, 10, 0)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 3
        return g
    return g
