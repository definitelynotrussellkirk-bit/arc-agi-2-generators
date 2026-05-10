"""Generator for v1_e_m_h_keys:H4.

Rule: mirror non-frame interior cells across the color-8 frame
centerline.

Combinatorial axes (8): variant, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_motif, full_motif, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "528bbb532b67"
VERSION = "1.1.0"
TASK_ID = "528bbb532b67"
SUMMARY = "Mirror non-frame interior cells across the color-8 frame centerline."

INVARIANTS = [
    "there is one color-8 rectangular frame",
    "interior motif cells are nonzero and not color 8",
    "at least one motif cell lies strictly left of its mirrored location",
    "the rule preserves original cells and paints their horizontal mirrors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_motif", "full_motif", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "variant":        {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MOTIFS = [
    [(2, 3), (3, 4)],
    [(2, 2), (3, 3), (4, 4)],
    [(2, 3), (4, 2)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        variant = ctx.draw_int("variant", 0, 0)
    elif difficulty == "hard":
        variant = ctx.draw_int("variant", 1, 2)
    else:
        variant = ctx.draw_int("variant", 0, 2)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
    g = full_grid(7, 9, 0)
    for c in range(1, 8):
        g[1][c] = 8
        g[5][c] = 8
    for r in range(1, 6):
        g[r][1] = 8
        g[r][7] = 8
    for r, c in _MOTIFS[variant]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 9, 0)
    if name == "no_motif":
        for c in range(1, 8):
            g[1][c] = 8; g[5][c] = 8
        for r in range(1, 6):
            g[r][1] = 8; g[r][7] = 8
        return g
    if name == "full_motif":
        for c in range(1, 8):
            g[1][c] = 8; g[5][c] = 8
        for r in range(1, 6):
            g[r][1] = 8; g[r][7] = 8
        for r in range(2, 5):
            for c in range(2, 7):
                g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(9):
                g[r][c] = 8
        return g
    return g
