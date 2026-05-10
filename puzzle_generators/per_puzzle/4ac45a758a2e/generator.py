"""Generator for arc_additional_puzzle_bank_volume8:H54.

Rule: counts of blue and red controls select rotation and optional
reflection for a magenta template stamped at orange.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rot_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_controls, no_template, no_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4ac45a758a2e"
VERSION = "1.1.0"
TASK_ID = "4ac45a758a2e"
SUMMARY = "Counts of blue and red controls select rotation and optional reflection for a magenta template stamped at orange."

INVARIANTS = [
    "the count of color-1 controls is 1 through 4",
    "the count of color-2 controls is 1 or 2",
    "there is one largest color-6 template",
    "the color-7 anchor leaves room for the transformed cyan stamp",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_controls", "no_template", "no_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "9..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rot_count":      {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "controls_corners",
                       "valid": "controls_corners"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 12, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rot_count = rng.randint(1, 4)
    ref_count = rng.randint(1, 2)
    for i in range(rot_count):
        g[0][w - 1 - i] = 1
    for i in range(ref_count):
        g[h - 1 - i][0] = 2
    for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
        g[2 + dr][1 + dc] = 6
    g[h - 5][w - 6] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 14
    g = full_grid(h, w, 0)
    if name == "no_controls":
        # no blue/red control cells → rotation/reflection counts are undefined (0)
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[2 + dr][1 + dc] = 6
        g[h - 5][w - 6] = 7
        return g
    if name == "no_template":
        # controls and anchor exist but no magenta template → nothing to transform
        g[0][w - 1] = 1
        g[h - 1][0] = 2
        g[h - 5][w - 6] = 7
        return g
    if name == "no_anchor":
        # no color-7 anchor → no stamp position, transformed template has nowhere to go
        g[0][w - 1] = 1; g[0][w - 2] = 1
        g[h - 1][0] = 2
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[2 + dr][1 + dc] = 6
        return g
    return g
