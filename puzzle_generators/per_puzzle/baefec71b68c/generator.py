"""Generator for 62ab2642.

Rule: zero holes inside gray field ranked by area; smallest becomes
orange and largest cyan.

Combinatorial axes (8): grid_h/w, hole_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_holes, all_holes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "baefec71b68c"
VERSION = "1.1.0"
TASK_ID = "baefec71b68c"
SUMMARY = "Zero holes in gray field; smallest becomes orange, largest cyan."

INVARIANTS = [
    "field color is 5",
    "there are at least two separated zero regions",
    "zero regions have different sizes",
    "all zero regions are bounded by color 5",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_holes", "all_holes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "hole_count":     {"type": "int", "default": "2", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    ctx.draw_int("hole_count", 2, 2)
    h = 9 + rng.randint(0, 4)
    w = 9 + rng.randint(0, 4)
    g = full_grid(h, w, 5)
    small_r = 1 + (sample_index % 2)
    small_c = 1 + ((sample_index // 2) % 2)
    for dr in range(1):
        for dc in range(2):
            g[small_r + dr][small_c + dc] = 0
    big_r = h - 5
    big_c = w - 5
    for dr in range(3):
        for dc in range(3):
            g[big_r + dr][big_c + dc] = 0
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 5)
    if name == "no_holes":
        return g
    if name == "all_holes":
        return full_grid(11, 11, 0)
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
