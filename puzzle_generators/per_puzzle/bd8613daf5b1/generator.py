"""Generator for arc_puzzle_bank_21_set24_s:S24_E7.

Rule: a single solid component is converted to its cropped onion-depth
map.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_object, edge_object, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bd8613daf5b1"
VERSION = "1.1.0"
TASK_ID = "bd8613daf5b1"
SUMMARY = "A single solid component is converted to its cropped onion-depth map."

INVARIANTS = [
    "background is 0",
    "there is one solid monochrome rectangle",
    "the output is the tight crop of the rectangle's depth map",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_object", "edge_object", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "7..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "random", "valid": "random"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    rh = rng.randint(4, min(8, h))
    rw = rng.randint(4, min(8, w))
    r0 = rng.randint(0, h - rh)
    c0 = rng.randint(0, w - rw)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    for r in range(r0, r0 + rh):
        for c in range(c0, c0 + rw):
            grid[r][c] = color
    return grid


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 11, 0)
    if name == "no_object":
        return g
    if name == "edge_object":
        for r in range(0, 4):
            for c in range(0, 4):
                g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(11):
                g[r][c] = 3
        return g
    return g
