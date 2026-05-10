"""Generator for arc_puzzle_bank_seventh21:H44.

Rule: the bottom-left local panel is rotated clockwise and pasted into
the bottom-right panel position.

Combinatorial axes (8): grid_h/w, palette_kind, shape_variant,
palette_size, position_bias, n_distinct_colors, panel_density, texture.
Degenerates: no_motif, motif_in_wrong_panel, motif_90_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5df55418cdc1"
VERSION = "1.1.0"
TASK_ID = "5df55418cdc1"
SUMMARY = "Rotate the lower-left 5x5 panel clockwise into the lower-right panel."

INVARIANTS = [
    "the active source panel is rows 6..10 and columns 0..4",
    "the target paste location starts at row 6 column 6",
    "the source panel contains a nonzero motif",
    "the target panel is initially blank",
]

PALETTE_KINDS = ("default", "L_motif", "T_motif", "Z_motif")
DEGENERATE_TEXTURES = ("no_motif", "motif_in_wrong_panel", "motif_90_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_variant":  {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "lower_left",
                       "valid": "lower_left"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "panel_density":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        idx = ctx.draw_int("shape_variant", 0, 0)
    elif difficulty == "hard":
        idx = ctx.draw_int("shape_variant", 1, 2)
    else:
        idx = ctx.draw_int("shape_variant", 0, len(_SHAPES) - 1)
    shape = _SHAPES[idx]
    color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    g = full_grid(11, 11, 0)
    for dr, dc in shape:
        g[7 + dr][1 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_motif":
        # source panel empty — no rotation to stamp
        return g
    if name == "motif_in_wrong_panel":
        # motif in upper-left panel — invariant violated (source must be lower-left)
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[1 + dr][1 + dc] = 4
        return g
    if name == "motif_90_symmetric":
        # 90°-symmetric motif (2×2 square) → CW rotation is identity
        for r in range(7, 9):
            for c in range(1, 3):
                g[r][c] = 5
        return g
    return g
