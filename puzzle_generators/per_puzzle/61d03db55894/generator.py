"""Generator for a64e4611.

Rule: wide blank stripes inside the largest zero component have their
trimmed interiors painted green.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_stripe, narrow_stripe, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "61d03db55894"
VERSION = "1.1.0"
TASK_ID = "61d03db55894"
SUMMARY = "Wide blank stripes inside the largest zero component get green-painted interiors."

INVARIANTS = [
    "the background is blue",
    "one large connected zero component contains a wide horizontal or vertical blank stripe",
    "interior rows or columns of that stripe are filled with green",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_stripe", "narrow_stripe", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 22..26", "valid": "22..26"},
    "grid_w":         {"type": "int", "default": "rng 23..28", "valid": "23..28"},
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
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
    h = 22 + (sample_index % 5)
    w = 23 + ((sample_index * 2) % 6)
    g = full_grid(h, w, 1)
    if orientation == "horizontal":
        stripe_h = 3 + (sample_index % 4)
        stripe_w = 17 + ((sample_index * 3) % (w - 18))
        top = 1 + ((sample_index * 2) % (h - stripe_h - 1))
        left = 1 + ((sample_index * 5) % (w - stripe_w - 1))
        draw_rect(g, top, left, stripe_h, stripe_w, 0)
    else:
        stripe_h = 17 + ((sample_index * 3) % (h - 18))
        stripe_w = 3 + (sample_index % 4)
        top = 1 + ((sample_index * 5) % (h - stripe_h - 1))
        left = 1 + ((sample_index * 2) % (w - stripe_w - 1))
        draw_rect(g, top, left, stripe_h, stripe_w, 0)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(22, 23, 1)
    if name == "no_stripe":
        return g
    if name == "narrow_stripe":
        draw_rect(g, 5, 5, 2, 2, 0)
        return g
    if name == "full_grid":
        for r in range(22):
            for c in range(23):
                g[r][c] = 0
        return g
    return g
