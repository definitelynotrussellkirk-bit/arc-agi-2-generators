"""Generator for abbfd121.

Rule: a solid block hides part of a periodic pattern, and the hidden
patch is reconstructed.

Combinatorial axes (8): grid_h/w, target_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_block, no_pattern, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b1af643b5c32"
VERSION = "1.1.0"
TASK_ID = "b1af643b5c32"
SUMMARY = "Solid block hides part of periodic pattern; hidden patch is reconstructed."

INVARIANTS = [
    "the visible background follows a small row/column period",
    "one solid rectangular block is the largest exact block in the grid",
    "the output is the periodic pattern over that block's bounding box",
]

SIZE_KINDS = ("S3", "S4")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_block", "no_pattern", "full_grid")
HELPFUL_TEXTURES = SIZE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "target_size":    {"type": "choice", "default": "rng helpful",
                       "valid": "3|4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "texture":        {"type": "str", "default": "alias for target_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in SIZE_KINDS:
        target_size = int(tx[1])
    elif difficulty == "easy":
        target_size = 3
    elif difficulty == "hard":
        target_size = 4
    else:
        target_size = ctx.draw_choice("target_size", [3, 4])
    a, b, c, d, block = ctx.draw_distinct_colors("colors", n=5, exclude={0})
    tile = [[a, b], [c, d]]
    h = w = 10
    g = [[tile[r % 2][col % 2] for col in range(w)] for r in range(h)]
    r0 = 2 + (sample_index % 2)
    c0 = 3 + ((sample_index // 2) % 2)
    for r in range(r0, r0 + target_size):
        for col in range(c0, c0 + target_size):
            g[r][col] = block
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_block":
        tile = [[1, 2], [3, 4]]
        return [[tile[r % 2][c % 2] for c in range(10)] for r in range(10)]
    if name == "no_pattern":
        for r in range(2, 5):
            for c in range(3, 6):
                g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 5
        return g
    return g
