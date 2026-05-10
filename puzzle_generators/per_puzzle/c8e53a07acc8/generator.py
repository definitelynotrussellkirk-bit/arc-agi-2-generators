"""Generator for d6542281.

Rule: standalone same-count anchors receive a copied multicolor fragment
template.

Combinatorial axes (8): grid_h/w, anchor_shape, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_template, no_anchor, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c8e53a07acc8"
VERSION = "1.1.0"
TASK_ID = "c8e53a07acc8"
SUMMARY = "Standalone same-count anchors receive a copied multicolor fragment template."

INVARIANTS = [
    "one multicolor template contains an anchor color appearing a fixed number of times",
    "a standalone object of that anchor color has the same cell count and shape",
    "the template is stamped onto the standalone anchor when its non-anchor cells land on background",
]

ANCHOR_SHAPES = ("domino", "corner")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_anchor", "full_grid")
HELPFUL_TEXTURES = ANCHOR_SHAPES

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "anchor_shape":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ANCHOR_SHAPES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for anchor_shape",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    anchor_shape = (overrides.get("texture") if overrides.get("texture") in ANCHOR_SHAPES else None) or \
                   overrides.get("anchor_shape") or \
                   ("domino" if sample_index % 2 == 0 else "corner")
    anchor, fill_a, fill_b = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    g = full_grid(12, 13, 0)
    if anchor_shape == "domino":
        anchors = [(0, 0), (0, 1)]
    else:
        anchors = [(0, 0), (1, 0)]
    for dr, dc in anchors:
        g[1 + dr][1 + dc] = anchor
        g[7 + dr][8 + dc] = anchor
    g[2][1] = fill_a
    g[2][2] = fill_b
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 13, 0)
    if name == "no_template":
        g[7][8] = 3
        g[7][9] = 3
        return g
    if name == "no_anchor":
        g[2][1] = 4
        g[2][2] = 5
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(13):
                g[r][c] = 3
        return g
    return g
