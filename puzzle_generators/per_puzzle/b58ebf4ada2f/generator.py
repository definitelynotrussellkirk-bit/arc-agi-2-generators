"""Generator for 7d419a02.

Rule: field of 8s around a 6-block keeps row/column bands and
recolors unsupported diagonals to 4.

Combinatorial axes (8): grid_h/w, block_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_block, no_field, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b58ebf4ada2f"
VERSION = "1.1.0"
TASK_ID = "b58ebf4ada2f"
SUMMARY = "Field of 8s around 6-block; rule keeps bands and recolors diagonals to 4."

INVARIANTS = [
    "the field color is 8",
    "one compact block uses color 6",
    "8 cells aligned with the 6-block row or column span stay 8",
    "the 6-block sits clear of grid borders so bands extend on all sides",
]

BLOCK_SIZES = ("1x2", "2x2", "2x3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_block", "no_field", "full_grid")
HELPFUL_TEXTURES = BLOCK_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "block_size":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(BLOCK_SIZES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for block_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    size = (overrides.get("texture") if overrides.get("texture") in BLOCK_SIZES else None) or \
           overrides.get("block_size") or \
           ctx.draw_choice("block_size", list(BLOCK_SIZES))
    bh, bw = (int(x) for x in size.split("x"))
    h = 8 + rng.randint(0, 3)
    w = 8 + rng.randint(0, 3)
    g = full_grid(h, w, 8)
    r0 = h // 2 - bh // 2
    c0 = w // 2 - bw // 2
    for r in range(r0, r0 + bh):
        for c in range(c0, c0 + bw):
            g[r][c] = 6
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 8)
    if name == "no_block":
        return g
    if name == "no_field":
        g = full_grid(10, 10, 0)
        g[5][5] = 6
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 6
        return g
    return g
