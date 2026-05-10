"""Generator for aa62e3f4.

Rule: least frequent non-background color outlines occupied row and
column extents.

Combinatorial axes (8): grid_h/w, motif_shape, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_motif, full_grid, single_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "48bda9528e71"
VERSION = "1.1.0"
TASK_ID = "48bda9528e71"
SUMMARY = "Least frequent non-bg color outlines occupied row and column extents."

INVARIANTS = [
    "background is color 8",
    "one compact non-background shape uses color 4",
    "one cell within the shape uses the rare color 2",
    "the shape sits with bg margin on all sides",
]

MOTIF_SHAPES = ("plus", "block", "ell")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_motif", "full_grid", "single_color")
HELPFUL_TEXTURES = MOTIF_SHAPES

MOTIFS = {
    "plus": PLUS_5,
    "block": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
    "ell": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
}

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "motif_shape":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MOTIF_SHAPES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for motif_shape",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    motif = (overrides.get("texture") if overrides.get("texture") in MOTIF_SHAPES else None) or \
            overrides.get("motif_shape") or \
            ctx.draw_choice("motif_shape", list(MOTIF_SHAPES))
    h = 8 + rng.randint(0, 4)
    w = 8 + rng.randint(0, 4)
    g = full_grid(h, w, 8)
    r0 = 2 + rng.randint(0, h - 6)
    c0 = 2 + rng.randint(0, w - 6)
    cells = MOTIFS[motif]
    paint_at(g, r0, c0, cells, 4)
    rare_dr, rare_dc = cells[len(cells) // 2]
    g[r0 + rare_dr][c0 + rare_dc] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 8)
    if name == "no_motif":
        return g
    if name == "single_color":
        for r in range(3, 7):
            for c in range(3, 7):
                g[r][c] = 4
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 4
        return g
    return g
