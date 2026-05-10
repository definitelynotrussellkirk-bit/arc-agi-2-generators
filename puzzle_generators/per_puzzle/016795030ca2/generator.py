"""Generator for 22233c11.

Rule: 8-conn components of color 3 (two diagonally-touching NxN
blocks). For each, project NxN block of 8s past each end of diagonal.

Combinatorial axes (8): grid_h/w, block_size, is_anti, position_bias,
palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: single_block, no_blocks, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "016795030ca2"
VERSION = "1.1.0"
TASK_ID = "016795030ca2"
SUMMARY = "Two NxN color-3 blocks touching diagonally; rule extends 8-cells past both ends."

INVARIANTS = [
    "exactly one 8-conn component of color 3 made of two NxN blocks (N=2 or 3)",
    "the two blocks touch at a corner (anti-diagonal or diagonal)",
    "enough margin past each end for the projected 8-blocks to fit",
]

POSITION_BIASES = ("centered", "scattered", "near_edge", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("single_block", "no_blocks", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "block_size":     {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "is_anti":        {"type": "bool", "default": "rng",
                       "valid": "true|false"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 9, 10
    elif difficulty == "hard":
        h_lo, h_hi = 12, 14
    else:
        h_lo, h_hi = 10, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    bs = int(overrides.get("block_size",
                           rng.choice([2, 2, 3])))
    bs = max(2, min(4, bs))
    margin = int(1.5 * bs) + 1
    is_anti_o = overrides.get("is_anti")
    if is_anti_o is None:
        is_anti = rng.choice([True, False])
    else:
        is_anti = bool(is_anti_o)
    r_min = margin
    r_max = h - margin - 2 * bs
    c_min = margin
    c_max = w - margin - 2 * bs
    if r_min > r_max:
        r_min, r_max = 0, h - 2 * bs - 1
    if c_min > c_max:
        c_min, c_max = 0, w - 2 * bs - 1
    r1 = rng.randint(r_min, r_max)
    c1 = rng.randint(c_min, c_max)
    if is_anti:
        fill_box(g, r1, c1 + bs, r1 + bs - 1, c1 + 2 * bs - 1, 3)
        fill_box(g, r1 + bs, c1, r1 + 2 * bs - 1, c1 + bs - 1, 3)
    else:
        fill_box(g, r1, c1, r1 + bs - 1, c1 + bs - 1, 3)
        fill_box(g, r1 + bs, c1 + bs, r1 + 2 * bs - 1, c1 + 2 * bs - 1, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "single_block":
        fill_box(g, 4, 4, 5, 5, 3)
        return g
    if name == "no_blocks":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
