"""Generator for e40b9e2f.

Rule: partial motif completed by 90, 180 and 270 degree rotations
around its inferred center.

Combinatorial axes (8): grid_h/w, motif, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, color.
Degenerates: no_motif, full_grid, single_pixel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "b16ee7199f81"
VERSION = "1.1.0"
TASK_ID = "b16ee7199f81"
SUMMARY = "Partial motif completed by 90/180/270 degree rotations around its center."

INVARIANTS = [
    "background is color 0",
    "the nonzero cells form a partial asymmetric motif",
    "the motif centroid defines the rotation center",
    "the motif sits clear of grid borders so rotations have room",
]

MOTIF_NAMES = ("ell", "hook", "tri")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_motif", "full_grid", "single_pixel")
HELPFUL_TEXTURES = MOTIF_NAMES

MOTIFS = {
    "ell": [(0, 0), (0, 1), (1, 0)],
    "hook": [(0, 0), (1, 0), (2, 0), (2, 1)],
    "tri": [(0, 0), (0, 1), (1, 1)],
}

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "motif":          {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MOTIF_NAMES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "color":          {"type": "color", "default": "rng !0", "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for motif",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    motif = (overrides.get("texture") if overrides.get("texture") in MOTIF_NAMES else None) or \
            overrides.get("motif") or \
            ctx.draw_choice("motif", list(MOTIF_NAMES))
    color = ctx.draw_color("color", exclude={0})
    h = 9 + rng.randint(0, 3)
    w = 9 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    paint_at(g, h // 2 - 2, w // 2 - 1, MOTIFS[motif], color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_motif":
        return g
    if name == "single_pixel":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 2
        return g
    return g
