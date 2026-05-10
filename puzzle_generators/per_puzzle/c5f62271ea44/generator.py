"""Generator for 94133066.

Rule: a scattered four-corner color key selects a symmetry transform of
a framed panel.

Combinatorial axes (8): grid_h/w, symmetry, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_panel, no_key, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "c5f62271ea44"
VERSION = "1.1.0"
TASK_ID = "c5f62271ea44"
SUMMARY = "Scattered four-corner color key selects a symmetry transform of a framed panel."

INVARIANTS = [
    "color 1 marks the rectangular panel border",
    "the panel has four colored inner-corner cells",
    "four scattered cells outside the panel form a matching corner arrangement",
    "the scattered arrangement determines which symmetry is applied to the panel",
]

SYMMETRIES = ("identity", "flip_lr", "flip_ud", "rot180")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_panel", "no_key", "full_grid")
HELPFUL_TEXTURES = SYMMETRIES

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "symmetry":       {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SYMMETRIES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for symmetry",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    symmetry = (overrides.get("texture") if overrides.get("texture") in SYMMETRIES else None) or \
               overrides.get("symmetry") or \
               ctx.draw_choice("symmetry", list(SYMMETRIES))
    a, b, c, d = ctx.draw_distinct_colors("corner_colors", n=4, exclude={0, 1})
    g = full_grid(11, 12, 0)
    draw_frame(g, 4, 5, 8, 9, 1)
    g[5][6], g[5][8], g[7][6], g[7][8] = a, b, c, d
    arrangements = {
        "identity": (a, b, c, d),
        "flip_lr": (b, a, d, c),
        "flip_ud": (c, d, a, b),
        "rot180": (d, c, b, a),
    }
    tl, tr, bl, br = arrangements[symmetry]
    g[0][0], g[0][2], g[2][0], g[2][2] = tl, tr, bl, br
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 0)
    if name == "no_panel":
        g[0][0] = 3
        return g
    if name == "no_key":
        draw_frame(g, 4, 5, 8, 9, 1)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(12):
                g[r][c] = 1
        return g
    return g
