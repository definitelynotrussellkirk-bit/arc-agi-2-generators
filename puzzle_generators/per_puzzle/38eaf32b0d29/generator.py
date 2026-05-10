"""Generator for 396d80d7.

Rule: bg cells diagonally (not cardinally) adjacent to outer color
become inner color.

Combinatorial axes (8): grid_size, block_size, palette_kind, position_bias,
inner_position, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_outer, no_inner, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "38eaf32b0d29"
VERSION = "1.1.0"
TASK_ID = "38eaf32b0d29"
SUMMARY = "Bg cells diagonally adjacent (not cardinally) to outer block become inner color."

INVARIANTS = [
    "zero is the mode background",
    "the outer color is the most frequent non-background color",
    "an inner color is present but less frequent",
    "only diagonal-only neighbors of outer cells are filled with the inner color",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_outer", "no_inner", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_size":      {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "block_size":     {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "inner_position": {"type": "str", "default": "tr",
                       "valid": "tl|tr|bl|br|center"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
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
        size_lo, size_hi = 7, 9
        bs_lo, bs_hi = 2, 2
    elif difficulty == "hard":
        size_lo, size_hi = 12, 16
        bs_lo, bs_hi = 3, 5
    else:
        size_lo, size_hi = 9, 12
        bs_lo, bs_hi = 2, 3
    block_size = ctx.draw_int("block_size", bs_lo, bs_hi)
    block_size = max(2, min(5, block_size))
    outer, inner = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    size = rng.randint(size_lo, size_hi)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "centered":
        r0 = max(3, (size - block_size) // 2)
        c0 = max(3, (size - block_size) // 2)
    elif bias == "corner":
        r0 = rng.choice([3, max(3, size - block_size - 3)])
        c0 = rng.choice([3, max(3, size - block_size - 3)])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            r0 = rng.choice([3, max(3, size - block_size - 3)])
            c0 = rng.randint(3, max(3, size - block_size - 3))
        else:
            r0 = rng.randint(3, max(3, size - block_size - 3))
            c0 = rng.choice([3, max(3, size - block_size - 3)])
    else:
        r0 = rng.randint(3, max(3, size - block_size - 3))
        c0 = rng.randint(3, max(3, size - block_size - 3))
    g = full_grid(size, size, 0)
    draw_rect(g, r0, c0, block_size, block_size, outer)
    inner_pos = overrides.get("inner_position",
                              ctx.draw_choice("inner_position",
                                              ["tl", "tr", "bl", "br", "center"]))
    if inner_pos == "tl":
        g[1][1] = inner
    elif inner_pos == "tr":
        g[1][size - 2] = inner
    elif inner_pos == "bl":
        g[size - 2][1] = inner
    elif inner_pos == "center":
        g[size // 2][size - 2] = inner
    else:
        g[1][size - 2] = inner
    return g


def _draw_from_degenerate(name, rng):
    size = 10
    g = full_grid(size, size, 0)
    if name == "no_outer":
        g[1][8] = 3
        return g
    if name == "no_inner":
        draw_rect(g, 4, 4, 2, 2, 2)
        return g
    if name == "full_grid":
        for r in range(size):
            for c in range(size):
                g[r][c] = 2
        return g
    return g
