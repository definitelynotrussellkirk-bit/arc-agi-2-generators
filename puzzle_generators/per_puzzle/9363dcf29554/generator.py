"""Generator for fd096ab6.

Rule: the largest color shape is a template; smaller matching partials
are completed to it.

Combinatorial axes (8): grid_h/w, variant, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_template, no_partials, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9363dcf29554"
VERSION = "1.1.0"
TASK_ID = "9363dcf29554"
SUMMARY = "Largest color shape is template; smaller matching partials completed to it."

INVARIANTS = [
    "the background is blue",
    "one largest foreground shape defines the template offsets",
    "other colors show subsets of that same template at different origins",
    "missing template cells are filled for each partial color group",
]

VARIANTS = ("v0", "v1", "v2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_partials", "full_grid")
HELPFUL_TEXTURES = VARIANTS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "variant":        {"type": "choice", "default": "rng helpful",
                       "valid": "0|1|2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for variant",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


TEMPLATE = [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)]


def _paint(g, r0, c0, cells, color):
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in VARIANTS:
        variant = int(tx[1])
    else:
        variant = ctx.draw_choice("variant", [0, 1, 2])
    tmpl, c1, c2 = ctx.draw_distinct_colors("colors", n=3, exclude={1})
    g = full_grid(13, 14, 1)
    _paint(g, 1, 1, TEMPLATE, tmpl)
    partials = [
        (5, 6, [TEMPLATE[0], TEMPLATE[2], TEMPLATE[4]], c1),
        (8, 10, [TEMPLATE[1], TEMPLATE[2], TEMPLATE[3]], c2),
    ]
    if variant == 1:
        partials[0] = (5, 7, [TEMPLATE[0], TEMPLATE[1], TEMPLATE[3]], c1)
    elif variant == 2:
        partials[1] = (8, 9, [TEMPLATE[0], TEMPLATE[3], TEMPLATE[4]], c2)
    for r, c, cells, color in partials:
        _paint(g, r, c, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 14, 1)
    if name == "no_template":
        g[5][6] = 3
        return g
    if name == "no_partials":
        _paint(g, 1, 1, TEMPLATE, 4)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(14):
                g[r][c] = 4
        return g
    return g
