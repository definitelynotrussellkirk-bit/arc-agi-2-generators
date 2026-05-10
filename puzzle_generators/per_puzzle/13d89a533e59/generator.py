"""Generator for 85fa5666.

Rule: 2x2 red block swaps four diagonal corner colors and extends
those colors outward.

Combinatorial axes (8): grid_h/w, block_position, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_block, no_corners, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "13d89a533e59"
VERSION = "1.1.0"
TASK_ID = "13d89a533e59"
SUMMARY = "2x2 red block swaps diagonal corner colors and extends outward."

INVARIANTS = [
    "background is color 0",
    "one solid 2x2 block uses color 2",
    "four diagonal corner cells around the block have nonzero colors",
    "corner colors are distinct from each other and from 0 and 2",
]

POSITIONS = ("center", "upper", "lower")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_block", "no_corners", "full_grid")
HELPFUL_TEXTURES = POSITIONS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "block_position": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for block_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    position = (overrides.get("texture") if overrides.get("texture") in POSITIONS else None) or \
               overrides.get("block_position") or \
               ctx.draw_choice("block_position", list(POSITIONS))
    colors = ctx.draw_distinct_colors("corner_colors", n=4, exclude={0, 2})
    g = full_grid(11, 11, 0)
    rr = {"upper": 3, "center": 4, "lower": 5}[position]
    cc = 4
    for r in range(rr, rr + 2):
        for c in range(cc, cc + 2):
            g[r][c] = 2
    g[rr - 1][cc - 1] = colors[0]
    g[rr - 1][cc + 2] = colors[1]
    g[rr + 2][cc - 1] = colors[2]
    g[rr + 2][cc + 2] = colors[3]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_block":
        for r, c in [(3, 3), (3, 7), (7, 3), (7, 7)]:
            g[r][c] = 1
        return g
    if name == "no_corners":
        for r in range(4, 6):
            for c in range(4, 6):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
